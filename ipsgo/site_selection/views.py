## site_selection
##
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import ListView, DetailView
#from django.utils import timezone

from site_selection.models import Project

class IndexView(ListView):
    model = Project
    def get(self, request, *args, **kwargs):
        return TemplateResponse(request, self.get_template_name(), self.get_context_data())
            
    def get_template_name(self):
        """Returns the name of the template we should render"""
        return "site_selection/index.html"

    def get_context_data(self):
        """Returns the data passed to the template"""
        return {
            "index": self.get_object(),
        }

    def get_object(self):
        """Returns the BlogPost instance that the view displays"""
        return get_object_or_404(Index, pk=self.kwargs.get("pk"))
    
    ##template_name = 'site_selection/index.html'
    ##context_object_name = 'latest_project_list'
   
    ##def get_queryset(self):
    ##    """Return the projects."""
    ##    return Project.objects.order_by('-modify_date')

class DetailView(DetailView):
    model = Project
    template_name = 'site_selection/detail.html'

# class ResultsView(generic.DetailView):
#     model = Project
#     template_name = 'site_selection/results.html'

