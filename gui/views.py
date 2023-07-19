import sys
from typing import Any, Dict, Optional
from datetime import datetime

from django import http
from django.db import transaction
from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError

from crawler.crawler import Crawler51

from .forms import SearchForm, SubscribeForm
from .models import SearchCondition, Subscription
from .enums import Platform

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
        
        request.session['search_results'] = search_results
        
        return super().get(request, *args, **kwargs)
    
class SubscribeView(FormView):
    template_name = 'gui/subscribe_form.html'
    form_class = SubscribeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_conditions'] = self.request.session['search_conditions']
        return context
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date >= end_date:
            self.add_error("end_date", "End date must be later than start date")

    def post(self, request, *args, **kwargs):
        form = SubscribeForm(request.POST)
        if form.is_valid():
            search_conditions = self.request.session['search_conditions']
            lowest_price = search_conditions['lowest_price'] if search_conditions['lowest_price'] else 0
            highest_price = search_conditions['highest_price'] if search_conditions['lowest_price'] else sys.maxsize

            email = form.cleaned_data['email']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            interval = form.cleaned_data['interval']
            
            try:
                with transaction.atomic():
                    search_condition_obj = SearchCondition.objects.create(
                        platforms=search_conditions['platforms'],
                        lowest_price=lowest_price,
                        highest_price=highest_price,
                        location=search_conditions['location'],
                        building_types=search_conditions['building_types'],
                        include_water=search_conditions['include_water'],
                        include_hydro=search_conditions['include_hydro'],
                        include_internet=search_conditions['include_internet'],
                        independent_bathroom=search_conditions['independent_bathroom'],
                        independent_kitchen=search_conditions['independent_kitchen']
                    )

                    Subscription.objects.create(
                        search_condition=search_condition_obj,
                        email=email,
                        start_time=datetime.combine(start_date, datetime.min.time()),
                        end_time=datetime.combine(end_date, datetime.min.time()),
                        next_time=datetime.combine(start_date, datetime.min.time()),
                        interval=int(interval)
                    )
            except Exception as e:
                print(str(e))
                return render(request, '500.html')

            return render(request, 'thank_you.html')
        
        return render(request, '500.html')
        