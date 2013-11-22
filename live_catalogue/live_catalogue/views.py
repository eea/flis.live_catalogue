from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages

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
        filter_form = CatalogueFilterForm(request.POST)
        if filter_form.is_valid():
            catalogues = catalogues.filter(kind=filter_form.cleaned_data['kind'])
        return render(request, 'home.html', {
            'catalogues': catalogues,
            'filter_form': filter_form,
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


class NeedEdit(View):

    def get(self, request, pk=None):
        catalogue = get_object_or_404(Catalogue, pk=pk) if pk else None
        form = NeedForm(instance=catalogue)
        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
        })

    def post(self, request, pk=None):
        catalogue = get_object_or_404(Catalogue, pk=pk) if pk else None
        is_draft = True if request.POST['save'] == 'draft' else False
        form = NeedForm(request.POST, instance=catalogue, is_draft=is_draft)
        if form.is_valid():
            form.save()
            if is_draft:
                success_msg = 'Need saved as draft'
            else:
                success_msg = 'Need saved'
            messages.success(request, 'Need saved')
            return redirect('home')
        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
        })


class OfferEdit(View):

    def get(self, request, pk=None):
        catalogue = get_object_or_404(Catalogue, pk=pk) if pk else None
        form = OfferForm(instance=catalogue)
        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
        })

    def post(self, request, pk=None):
        catalogue = get_object_or_404(Catalogue, pk=pk) if pk else None
        is_draft = True if request.POST['save'] == 'draft' else False
        form = OfferForm(request.POST, instance=catalogue, is_draft=is_draft)
        if form.is_valid():
            form.save()
            if is_draft:
                success_msg = 'Offer saved as draft'
            else:
                success_msg = 'Offer saved'
            messages.success(request, 'Need saved')
            return redirect('home')
        return render(request, 'catalogue_form.html', {
            'catalogue': catalogue,
            'form': form,
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

