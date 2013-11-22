from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.core.urlresolvers import reverse

from braces.views import AjaxResponseMixin, JSONResponseMixin
from live_catalogue.forms import NeedForm, OfferForm, CatalogueFilterForm
from live_catalogue.models import Catalogue, Keyword


class HomeView(View):

    def get(self, request):
        catalogues = Catalogue.objects.filter(draft=False)
        filter_form = CatalogueFilterForm()
        return render(request, 'home.html', {
            'catalogues': catalogues,
            'filter_form': filter_form,
        })

    def post(self, request):
        catalogues = Catalogue.objects.filter(draft=False)
        form = CatalogueFilterForm(request.POST)
        if form.is_valid():
            kind = form.cleaned_data['kind']
            if kind != 'all':
                catalogues = catalogues.filter(kind=kind)
        return render(request, 'home.html', {
            'catalogues': catalogues,
            'filter_form': form,
        })


class CatalogueView(View):

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

    def get(self, request, kind, pk=None):
        catalogue = get_object_or_404(Catalogue, pk=pk, user_id=request.user_id, kind=kind) if pk else None
        if kind == Catalogue.NEED:
            form = NeedForm(instance=catalogue)
        elif kind == Catalogue.OFFER:
            form = OfferForm(instance=catalogue)
        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
        })

    def post(self, request, kind, pk=None):
        catalogue = get_object_or_404(Catalogue, pk=pk, user_id=request.user_id, kind=kind) if pk else None
        is_draft = True if request.POST['save'] == 'draft' else False
        if kind == Catalogue.NEED:
            form = NeedForm(request.POST, instance=catalogue, is_draft=is_draft)
        elif kind == Catalogue.OFFER:
            form = OfferForm(request.POST, instance=catalogue, is_draft=is_draft)
        if form.is_valid():
            catalogue = form.save()
            if is_draft:
                success_msg = '%s saved as draft' % catalogue.kind_verbose
            else:
                success_msg = '%s saved' % catalogue.kind_verbose
            messages.success(request, success_msg)
            return redirect('home')
        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
        })


class CatalogueDelete(JSONResponseMixin, View):

    def delete(self, request, pk, kind):
        catalogue = get_object_or_404(Catalogue, pk=pk, user_id=request.user_id,
                                      kind=kind)
        catalogue.delete()
        messages.success(request,
            '%s was successfully deleted' % catalogue.kind_verbose)
        return self.render_json_response({
           'status': 'success',
           'url': reverse('home')
        })


class MyEntries(View):

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

class ApiKeywords(JSONResponseMixin, AjaxResponseMixin, View):

    def get_ajax(self, request):
        q = request.GET.get('q', '').strip()
        keywords = Keyword.objects.all()
        if q: keywords = keywords.filter(name__contains=q)
        return self.render_json_response({
            'status': 'success',
            'results': [{'id': k.pk, 'text': k.name} for k in keywords]
        })


class CrashMe(View):

    def get(self, request):
        raise Exception()

