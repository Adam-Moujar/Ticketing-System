from ticketing.apps import TicketingConfig
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from ticketing.nlp import ml_model_loader


class SearchBarView(View):
    template_name = 'search_bar.html'

    def get(self, request, *args, **kwargs):
        sequence_to_classify = 'How can I improve my critical thinking skills?'
        candidate_labels = [
            'Housing & accomodation support',
            'Fees, funding & money advice',
            'Appeals',
            'Complaints & Misconduct',
            'Administration',
            'Academic Digital Employability Skills',
            'Dignity & Inclusion',
        ]
        print(ml_model_loader.get_data(sequence_to_classify, candidate_labels))
        return render(request, 'search_bar.html')
