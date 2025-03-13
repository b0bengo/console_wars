from django.shortcuts import render
from django.views import generic

from members.models import UserOption

# Create your views here.

class HomeView(generic.TemplateView):
    template_name = "home/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        options = UserOption.objects.values_list('option', flat=True)
        
        # Initialize option_counts with zero values for each option
        option_counts = {
            'nintendo_switch': 0,
            'xbox': 0,
            'pc': 0,
            'playstation': 0
        }

        # Update option_counts with actual counts from the database
        for option in options:
            option_counts[option] += 1

        context['option_counts'] = option_counts
        return context