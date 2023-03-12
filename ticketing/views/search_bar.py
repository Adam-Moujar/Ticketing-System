from django.shortcuts import render
from django.views.generic import ListView
from ticketing.nlp import ml_api
from ticketing.models import Department, FAQ
 
#  TODO
    # what happens if there are less than three departments 
    # do a regex to stop speciliast creating subsections with underscore
    # return every FAQ but rank them.

class SearchBarView(ListView):
    template_name = 'search_bar.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'search_bar.html', context)
    
    def post(self, request):
        context = {}
        department_id = self.request.POST.get('department')
        if department_id != 0 and department_id != None:
            department_name = Department.objects.get(id = department_id)
            context['sub_sections_dict'] = self.get_subsections(department_name = department_name)
            
        sub_section_with_underscore = self.request.POST.get('sub_section')
        if sub_section_with_underscore != "" and sub_section_with_underscore != None: 
            sub_section_name = sub_section_with_underscore.replace('_', ' ')
            filtered_FAQs = self.get_filtered_FAQs(sub_section_name = sub_section_name)
            self.rank_FAQs(context, filtered_FAQs = filtered_FAQs)
        return render(request, 'search_bar.html', context)
    
    def get_queryset(self):
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = {}
        query = self.request.GET.get('query')
        self.INITIAL_QUERY = query
        if self.check_query_not_none_or_empty(query = query): 
            return context
        context, weights = self.rank_departments(query = query, context = context)
        if weights[0] > 0.5 and weights[1] > 0.5:
            context['low_score'] = True
        return context
    
    def check_query_not_none_or_empty(self, query):
        if query == None or query == "": 
            return True

    def chunk_creator(self, list):
        result = []
        count = 0
        mid = []
        for i in range(0, len(list)):
            if(count == 10):
                count = 0
                result.append(mid)
                mid = []
            mid.append(list[i])
            count = count + 1
        result.append(mid)
        return result
    
    # department functions
    def rank_departments(self, query, context):
        department_chunks = self.department_chunk_creator()
        total_dict = {}
        for chunk in department_chunks:
            candidate_labels = chunk
            data = ml_api.get_data(query, candidate_labels)
            department_list = data['labels']
            values = data['scores']
            for i in range(0, len(department_list)):
                total_dict[values[i]] = department_list[i]            
        weights = list(total_dict.keys())
        weights.sort(reverse = True)
        # name : id
        context['top_departments'] = {total_dict[weights[0]] : self.get_department_id(total_dict[weights[0]]),
                                      total_dict[weights[1]] : self.get_department_id(total_dict[weights[1]]),
                                      total_dict[weights[2]] : self.get_department_id(total_dict[weights[2]])
                                      }
        return context, weights
    
    def get_department_id(self, department_name):
        return Department.objects.get(name = department_name).id
    
    def department_chunk_creator(self):
        department_list = Department.objects.all().values_list("name", flat = True)
        return self.chunk_creator(department_list)

    # subsection functions
    def get_subsections(self, department_name):
        department = Department.objects.get(name = department_name)
        subsections_set = set(list(FAQ.objects.filter(department = department).values_list("subsection", flat=True)))  
        subsections_dict = {}
        # {subsections_name : subsections_underscore}
        for subsection in subsections_set: 
            subsections_dict[subsection] = subsection.replace(' ', '_')
        return subsections_dict     
    
    # FAQ functions
    def rank_FAQs(self, context, filtered_FAQs): 
        FAQ_chunks = self.FAQs_chunk_creator(filtered_FAQs=filtered_FAQs)
        total_dict = {}
        query = self.request.GET.get('query')
        for chunk in FAQ_chunks:
            candidate_labels = chunk
            data = ml_api.get_data(query , candidate_labels)
            FAQ_list = data['labels']
            values = data['scores']
            for i in range(0, len(FAQ_list)):
                total_dict[values[i]] = FAQ_list[i]            
        weights = list(total_dict.keys())
        weights.sort(reverse = True)
        context['top_FAQs'] = [total_dict[weights[0]], total_dict[weights[1]], total_dict[weights[2]]]
        return context, weights
    
    def FAQs_chunk_creator(self, filtered_FAQs):
        FAQ_list = filtered_FAQs.values_list("questions", flat = True)
        print(self.chunk_creator(FAQ_list))
        return self.chunk_creator(FAQ_list)  
        
    def get_filtered_FAQs(self, sub_section_name):

        return FAQ.objects.filter(subsection = sub_section_name)
    
