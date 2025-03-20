from django.shortcuts import render
from django.views import generic
from django.db.models import Count
from members.models import UserOption
from blog.models import Post

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

         # Query the most liked post for each category
        most_liked_posts = {
            'nintendo_switch': Post.objects.filter(author__useroption__option='nintendo_switch')
                                           .annotate(like_count=Count('likes'))
                                           .order_by('-like_count')
                                           .first(),
            'xbox': Post.objects.filter(author__useroption__option='xbox')
                                 .annotate(like_count=Count('likes'))
                                 .order_by('-like_count')
                                 .first(),
            'pc': Post.objects.filter(author__useroption__option='pc')
                               .annotate(like_count=Count('likes'))
                               .order_by('-like_count')
                               .first(),
            'playstation': Post.objects.filter(author__useroption__option='playstation')
                                       .annotate(like_count=Count('likes'))
                                       .order_by('-like_count')
                                       .first(),
        }

        context['option_counts'] = option_counts
        context['most_liked_posts'] = most_liked_posts
        return context