import os
import time

from django.views.generic import View, ListView, CreateView, UpdateView, \
    DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse
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
    CategoryForm,
    ThemeForm,
    TopicForm
)
from live_catalogue.models import (
    Catalogue,
    Document,
    Category,
    FlisTopic,
    Theme
)
from live_catalogue.auth import PermissionRequiredMixin
from notifications.models import catalogue_update_signal
from notifications.utils import get_user_data

from live_catalogue.definitions import (
    VIEW_ROLES,
    EDIT_ROLES,
    ADMIN_ROLES,
    VIEW_GROUPS,
    EDIT_GROUPS,
    ADMIN_GROUPS,
    ALL_ROLES,
    ALL_GROUPS,
)


class HomeView(PermissionRequiredMixin,
               View):

    roles_required = ALL_ROLES
    groups_required = ALL_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)

    def get(self, request, show):
        if show == 'open':
            catalogues = Catalogue.objects.filter(status=Catalogue.OPEN)
            request.session['open_last_viewed'] = time.time()
        else:
            catalogues = Catalogue.objects.filter(
                status__in=(Catalogue.CLOSED, Catalogue.SOLVED))
            request.session['closed_last_viewed'] = time.time()
        form = CatalogueFilterForm(request.GET)
        if form.is_valid():
            kind = form.cleaned_data['kind']
            if kind != 'all':
                catalogues = catalogues.filter(kind=kind)
        return render(request, 'home.html', {
            'catalogues': catalogues,
            'filter_form': form,
        })


class CatalogueView(PermissionRequiredMixin,
                    View):

    roles_required = ALL_ROLES
    groups_required = ALL_GROUPS

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


class CatalogueEdit(PermissionRequiredMixin,
                    View):

    roles_required = EDIT_ROLES
    groups_required = EDIT_GROUPS

    def dispatch(self, request, **kwargs):
        return super(CatalogueEdit, self).dispatch(request, **kwargs)

    def get(self, request, kind, pk=None):
        catalogue = get_object_or_404(Catalogue,
                                      pk=pk,
                                      user_id=request.user_id,
                                      kind=kind) if pk else None
        if pk is None:
            user_data = get_user_data(request.user_id)
            initial_user_data = {
                'contact_person': user_data.get('cn', [''])[0],
                'email': user_data.get('mail', [''])[0],
                'phone_number': user_data.get('telephoneNumber', [''])[0],
                'institution': user_data.get('o', [''])[0],
                'address': user_data.get('postalAddress', [''])[0]
            }
        else:
            initial_user_data = {}

        DocumentFormSet = formset_factory(DocumentForm,
                                          formset=BaseDocumentFormset,
                                          max_num=5)
        Form = NeedForm if kind == Catalogue.NEED else OfferForm
        form = Form(instance=catalogue, initial=initial_user_data)
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
        event_type = 'published' if pk is None else 'updated'

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

            if is_draft is False:
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


class CatalogueDelete(PermissionRequiredMixin, JSONResponseMixin, View):

    roles_required = EDIT_ROLES
    groups_required = EDIT_GROUPS

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


class MyEntries(PermissionRequiredMixin, View):

    roles_required = ALL_ROLES
    groups_required = ALL_GROUPS

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


class SettingsCategoriesView(PermissionRequiredMixin,
                             ListView):

    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS
    model = Category
    template_name = 'settings/setting_view.html'

    def dispatch(self, *args, **kwargs):
        return super(SettingsCategoriesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SettingsCategoriesView, self).get_context_data(**kwargs)
        context['page_title'] = "Categories"
        context['add_url'] = reverse('settings:categories_add')
        context['add_label'] = "New category"
        context['edit_route_name'] = 'settings:categories_edit'
        return context


class SettingsCategoriesAddView(PermissionRequiredMixin,
                                SuccessMessageMixin,
                                CreateView):

    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS
    model = Category
    template_name = 'settings/setting_edit.html'
    form_class = CategoryForm
    success_message = "New category created"

    def dispatch(self, *args, **kwargs):
        return super(SettingsCategoriesAddView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('settings:categories')

    def get_context_data(self, **kwargs):
        context = super(SettingsCategoriesAddView, self).get_context_data(
            **kwargs)
        context['add_page_title'] = "New category"
        context['cancel_url'] = reverse('settings:categories')
        return context


class SettingsCategoriesEditView(PermissionRequiredMixin,
                                 SuccessMessageMixin,
                                 UpdateView):

    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS
    model = Category
    template_name = 'settings/setting_edit.html'
    form_class = CategoryForm
    success_message = "Category updated successfully"

    def dispatch(self, *args, **kwargs):
        return super(SettingsCategoriesEditView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('settings:categories')

    def get_context_data(self, **kwargs):
        context = super(SettingsCategoriesEditView, self).get_context_data(
            **kwargs)
        context['delete_url'] = reverse('settings:categories_delete',
                                        kwargs={'pk': self.object.handle})
        context['cancel_url'] = reverse('settings:categories')
        return context


class SettingsCategoriesDeleteView(PermissionRequiredMixin,
                                   DeleteView):

    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS
    model = Category
    template_name = 'settings/setting_confirm_delete.html'

    def dispatch(self, *args, **kwargs):
        return super(SettingsCategoriesDeleteView, self).dispatch(*args,
                                                                  **kwargs)

    def post(self, request, *args, **kwargs):
        msg = 'Category "%s" was successfully deleted' % self.get_object()
        messages.success(request, msg)
        return super(SettingsCategoriesDeleteView, self).post(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('settings:categories')

    def get_context_data(self, **kwargs):
        context = super(SettingsCategoriesDeleteView, self).get_context_data(
            **kwargs)
        context['edit_url'] = reverse('settings:categories_edit',
                                      kwargs={'pk': self.object.handle})
        return context


class SettingsTopicsView(PermissionRequiredMixin,
                         ListView):

    model = FlisTopic
    template_name = 'settings/setting_view.html'
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsTopicsView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SettingsTopicsView, self).get_context_data(**kwargs)
        context['page_title'] = "Flis Topics"
        context['add_url'] = reverse('settings:topics_add')
        context['add_label'] = "New flis topic"
        context['edit_route_name'] = 'settings:topics_edit'
        return context


class SettingsTopicsAddView(PermissionRequiredMixin,
                            SuccessMessageMixin,
                            CreateView):

    model = FlisTopic
    template_name = 'settings/setting_edit.html'
    form_class = TopicForm
    success_message = "New flis topic created"
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsTopicsAddView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('settings:topics')

    def get_context_data(self, **kwargs):
        context = super(SettingsTopicsAddView, self).get_context_data(
            **kwargs)
        context['add_page_title'] = "New flis topic"
        context['cancel_url'] = reverse('settings:topics')
        return context


class SettingsTopicsEditView(PermissionRequiredMixin,
                             SuccessMessageMixin,
                             UpdateView):

    model = FlisTopic
    template_name = 'settings/setting_edit.html'
    form_class = TopicForm
    success_message = "Flis topic updated successfully"
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsTopicsEditView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('settings:topics')

    def get_context_data(self, **kwargs):
        context = super(SettingsTopicsEditView, self).get_context_data(
            **kwargs)
        context['delete_url'] = reverse('settings:topics_delete',
                                        kwargs={'pk': self.object.handle})
        context['cancel_url'] = reverse('settings:topics')
        return context


class SettingsTopicsDeleteView(PermissionRequiredMixin,
                               DeleteView):

    model = FlisTopic
    template_name = 'settings/setting_confirm_delete.html'
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsTopicsDeleteView, self).dispatch(*args,
                                                              **kwargs)

    def post(self, request, *args, **kwargs):
        msg = 'Flis topic "%s" was successfully deleted' % self.get_object()
        messages.success(request, msg)
        return super(SettingsTopicsDeleteView, self).post(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('settings:topics')

    def get_context_data(self, **kwargs):
        context = super(SettingsTopicsDeleteView, self).get_context_data(
            **kwargs)
        context['edit_url'] = reverse('settings:topics_edit',
                                      kwargs={'pk': self.object.handle})
        return context


class SettingsThemesView(PermissionRequiredMixin,
                         ListView):

    model = Theme
    template_name = 'settings/setting_view.html'
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsThemesView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SettingsThemesView, self).get_context_data(**kwargs)
        context['page_title'] = "Topics"
        context['add_url'] = reverse('settings:themes_add')
        context['add_label'] = "New topic"
        context['edit_route_name'] = 'settings:themes_edit'
        return context


class SettingsThemesAddView(PermissionRequiredMixin,
                            SuccessMessageMixin,
                            CreateView):

    model = Theme
    template_name = 'settings/setting_edit.html'
    form_class = ThemeForm
    success_message = "New topic created"
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsThemesAddView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('settings:themes')

    def get_context_data(self, **kwargs):
        context = super(SettingsThemesAddView, self).get_context_data(
            **kwargs)
        context['add_page_title'] = "New topic"
        context['cancel_url'] = reverse('settings:themes')
        return context


class SettingsThemesEditView(PermissionRequiredMixin,
                             SuccessMessageMixin,
                             UpdateView):

    model = Theme
    template_name = 'settings/setting_edit.html'
    form_class = ThemeForm
    success_message = "Topic updated successfully"
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsThemesEditView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('settings:themes')

    def get_context_data(self, **kwargs):
        context = super(SettingsThemesEditView, self).get_context_data(
            **kwargs)
        context['delete_url'] = reverse('settings:themes_delete',
                                        kwargs={'pk': self.object.handle})
        context['cancel_url'] = reverse('settings:themes')
        return context


class SettingsThemesDeleteView(PermissionRequiredMixin, DeleteView):

    model = Theme
    template_name = 'settings/setting_confirm_delete.html'
    roles_required = ADMIN_ROLES
    groups_required = ADMIN_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(SettingsThemesDeleteView, self).dispatch(*args,
                                                              **kwargs)

    def post(self, request, *args, **kwargs):
        msg = 'Topic "%s" was successfully deleted' % self.get_object()
        messages.success(request, msg)
        return super(SettingsThemesDeleteView, self).post(
            request, *args, **kwargs)

    def get_success_url(self):
        return reverse('settings:themes')

    def get_context_data(self, **kwargs):
        context = super(SettingsThemesDeleteView, self).get_context_data(
            **kwargs)
        context['edit_url'] = reverse('settings:themes_edit',
                                      kwargs={'pk': self.object.handle})
        return context


class CrashMe(PermissionRequiredMixin, View):

    roles_required = ALL_ROLES
    groups_required = ALL_GROUPS

    def dispatch(self, *args, **kwargs):
        return super(CrashMe, self).dispatch(*args, **kwargs)

    def get(self, request):
        raise Exception()
