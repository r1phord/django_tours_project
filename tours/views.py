from random import sample

from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.shortcuts import render
from django.views import View

from tours.data import tours, departures

MAIN_PAGE_TOURS_COUNT = 6


def custom_handler404(request, exception):
    return HttpResponseNotFound('Страница не найдена.')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка сервера.')


def context_processor(request):
    return {
        'available_departures': departures
    }


class MainView(View):
    def get(self, request):
        random_keys = sample(tours.keys(), MAIN_PAGE_TOURS_COUNT)
        random_tours = {key: tours.get(key) for key in random_keys}
        return render(
            request, 'tours/index.html', context={
                'tours': random_tours
            }
        )


class DepartureView(View):
    def get(self, request, departure):
        if departure not in departures:
            return HttpResponse('Данного направления нет в базе')

        departure_tours = {}
        prices = []
        nights = []

        for idx, tour in tours.items():
            if tour['departure'] == departure:
                departure_tours[idx] = tour
                prices.append(int(tour['price']))
                nights.append(int(tour['nights']))

        min_max_prices = {'min': min(prices), 'max': max(prices)}
        min_max_nights = {'min': min(nights), 'max': max(nights)}

        return render(
            request, 'tours/departure.html', context={
                'departure': departures.get(departure),
                'tours': departure_tours,
                'min_max_prices': min_max_prices,
                'min_max_nights': min_max_nights,
            }
        )


class TourView(View):
    def get(self, request, id):
        if id not in tours:
            return HttpResponse('Тур не найден')
        tour = tours.get(id)
        return render(
            request, 'tours/tour.html', context={
                'id': id,
                'tour': tour,
                'stars': '★' * int(tour['stars']),
                'dep': departures.get(tour['departure'])
            }
        )
