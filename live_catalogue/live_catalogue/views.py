import os

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.forms.models import formset_factory
from django.http import Http404
from django.conf import settings

from braces.views import JSONResponseMixin
from live_catalogue.forms import (
    NeedForm,
    OfferForm,
    DocumentForm,
    BaseDocumentFormset,
    CatalogueFilterForm,
)
from live_catalogue.models import Catalogue, Document
from live_catalogue.auth import login_required, edit_permission_required
from notifications.models import catalogue_update_signal


class HomeView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get(self, request):
        catalogues = Catalogue.objects.filter(draft=False)
        form = CatalogueFilterForm(request.GET)
        if form.is_valid():
            kind = form.cleaned_data['kind']
            flis_topic = form.cleaned_data['flis_topic']
            if kind != 'all':
                catalogues = catalogues.filter(kind=kind)
            if flis_topic != 'all':
                catalogues = catalogues.filter(flis_topic=flis_topic)

        return render(request, 'home.html', {
            'catalogues': catalogues,
            'filter_form': form,
        })


class CatalogueView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CatalogueView, self).dispatch(*args, **kwargs)

    def get(self, request, pk, kind):
        catalogue = get_object_or_404(Catalogue, pk=pk)
        if catalogue.kind == catalogue.NEED:
            form = NeedForm(instance=catalogue)
        elif catalogue.kind == catalogue.OFFER:
            form = OfferForm(instance=catalogue)
        return render(request, 'catalogue_view.html', {
            'catalogue': catalogue,
            'form': form,
        })


class CatalogueEdit(View):

    @method_decorator(login_required)
    @method_decorator(edit_permission_required)
    def dispatch(self, request, **kwargs):
        return super(CatalogueEdit, self).dispatch(request, **kwargs)

    def get(self, request, kind, pk=None):
        catalogue = get_object_or_404(Catalogue,
                                      pk=pk,
                                      user_id=request.user_id,
                                      kind=kind) if pk else None

        DocumentFormSet = formset_factory(DocumentForm,
                                          formset=BaseDocumentFormset,
                                          max_num=5)
        Form = NeedForm if kind == Catalogue.NEED else OfferForm
        form = Form(instance=catalogue)
        document_formset = DocumentFormSet()

        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
            'document_formset': document_formset,
        })

    def post(self, request, kind, pk=None):
        catalogue = get_object_or_404(Catalogue,
                                      pk=pk,
                                      user_id=request.user_id,
                                      kind=kind) if pk else None
        event_type = 'added' if pk is None else 'edited'

        save = request.POST.get('save', 'final')
        is_draft = True if save == 'draft' else False

        DocumentFormSet = formset_factory(DocumentForm,
                                          formset=BaseDocumentFormset,
                                          max_num=5)
        Form = NeedForm if kind == Catalogue.NEED else OfferForm
        form = Form(request.POST, instance=catalogue, is_draft=is_draft)
        document_formset = DocumentFormSet(request.POST, request.FILES)

        if form.is_valid() and document_formset.is_valid():
            catalogue = form.save()
            document_formset.save(catalogue)
            if is_draft:
                success_msg = '%s saved as draft' % catalogue.kind_verbose
            else:
                success_msg = '%s saved' % catalogue.kind_verbose
            messages.success(request, success_msg)

            catalogue_update_signal.send(sender=catalogue,
                                         event_type=event_type,
                                         request=request)
            return redirect('home')

        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
            'document_formset': document_formset,
        })


class CatalogueDocumentDelete(JSONResponseMixin, View):

    def delete(self, request, catalogue_id, doc_id):
        catalogue = get_object_or_404(Catalogue, pk=catalogue_id,
                                      user_id=request.user_id)
        try:
            doc = catalogue.documents.get(pk=doc_id)
        except Document.DoesNotExist:
            raise Http404

        doc_name = doc.name.name
        doc.delete()
        handle_delete_document_files([doc_name])
        return self.render_json_response({'status': 'success'})


def handle_delete_document_files(documents):
    for doc in documents:
        full_path = os.path.join(settings.MEDIA_ROOT, doc)
        if os.path.exists(full_path):
            os.remove(full_path)


class CatalogueDelete(JSONResponseMixin, View):

    @method_decorator(login_required)
    @method_decorator(edit_permission_required)
    def dispatch(self, *args, **kwargs):
        return super(CatalogueDelete, self).dispatch(*args, **kwargs)

    def delete(self, request, pk, kind):
        catalogue = get_object_or_404(Catalogue, pk=pk,
                                      user_id=request.user_id,
                                      kind=kind)
        document_names = [d.name.name for d in catalogue.documents.all()]
        handle_delete_document_files(document_names)
        catalogue.documents.all().delete()
        catalogue.delete()
        msg = '%s was successfully deleted' % catalogue.kind_verbose
        messages.success(request, msg)
        return self.render_json_response(
            {
                'status': 'success',
                'url': reverse('home')
            }
        )


class MyEntries(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyEntries, self).dispatch(*args, **kwargs)

    def get(self, request):
        catalogues = Catalogue.objects.filter(user_id=request.user_id)
        form = CatalogueFilterForm()
        return render(request, 'my_entries.html', {
            'catalogues': catalogues,
            'filter_form': form,
        })

    def post(self, request):
        catalogues = Catalogue.objects.filter(user_id=request.user_id)
        form = CatalogueFilterForm(request.POST)
        if form.is_valid():
            kind = form.cleaned_data['kind']
            if kind != 'all':
                catalogues = catalogues.filter(kind=kind)
        return render(request, 'my_entries.html', {
            'catalogues': catalogues,
            'filter_form': form,
        })


class CrashMe(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CrashMe, self).dispatch(*args, **kwargs)

    def get(self, request):
        raise Exception()
