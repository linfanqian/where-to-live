from typing import Any, Dict, Optional
from django import http
from django.db import models
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from crawler.crawler import Crawler51

from .forms import SearchForm

from .models import SearchCondition

from .enums import Platform
#from .forms import SubscribeForm

class SearchFormView(FormView):
    template_name = 'gui/search_form.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST)
        platforms = form['platforms'].value()
        lowest_price = form['lowest_price'].value()
        highest_price = form['highest_price'].value()
        location = form['location'].value()
        building_types = form['building_types'].value()
        include_water = form['include_water'].value()
        include_hydro = form['include_hydro'].value()
        include_internet = form['include_internet'].value()
        independent_bathroom = form['independent_bathroom'].value()
        independent_kitchen = form['independent_kitchen'].value()

        platform_str = ', '.join(platforms)
        building_type_str = ', '.join(building_types)

        request.session['search_conditions'] = {
            'platforms': platform_str,
            'lowest_price': lowest_price,
            'highest_price': highest_price,
            'location': location,
            'building_types': building_type_str,
            'include_water': include_water,
            'include_hydro': include_hydro,
            'include_internet': include_internet,
            'independent_bathroom': independent_bathroom,
            'independent_kitchen': independent_kitchen
        }

        return HttpResponseRedirect('result')

class SearchResultView(TemplateView):
    template_name = 'gui/search_result_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_conditions'] = self.request.session['search_conditions']
        context['search_results'] = self.request.session['search_results']
        return context

    def get(self, request, *args, **kwargs):
        search_results = []

        conditions = request.session['search_conditions']
        platforms = conditions['platforms']

        if Platform.HOUSE51 in platforms:
            house51_house_list = Crawler51().get_house_list(conditions)
            search_results += house51_house_list
        
        print(house51_house_list)
        request.session['search_results'] = search_results
        
        return super().get(request, *args, **kwargs)
    

'''
class index(FormView):
    template_name = 
    form_class = SubscribeForm
    success_url = 
'''
