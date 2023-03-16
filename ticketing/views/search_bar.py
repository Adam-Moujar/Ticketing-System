from django.views.generic import TemplateView, ListView
from ticketing.nlp import ml_api
from ticketing.models import Department, FAQ
from ticketing.models.departments import Subsection

class SearchBarView(TemplateView):
    template_name = 'search_bar.html' 

    # handles the data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        department_id = self.request.GET.get('department')
        subsection_id = self.request.GET.get('subsection')
        
        # will return the top departments
        if query and not subsection_id and not department_id:
            department_dict = self.rank_departments(query, result_size=3)
            context['top_departments'] = department_dict
            context['query'] = query

        # will return the top subsections
        if department_id and not subsection_id:
            subsection_dict = self.rank_subsections(query, department_id, result_size=3)
            context['top_subsections'] = subsection_dict
            context['query'] = query

        # will return the top FAQs
        if subsection_id and not department_id:
            faqs = self.rank_faqs(query, subsection_id, result_size=8)
            context['top_FAQs'] = faqs
        return context
    
    # helper functions
    def rank_departments(self, query, result_size: int):
        departments = Department.objects.all()
        department_names = [department.name for department in departments]
        department_dict = {}
        # Split the department names into chunks of size 10
        department_name_chunks = [department_names[i:i+10] for i in range(0, len(department_names), 10)]
        for department_name_chunk in department_name_chunks:
            data = ml_api.get_data(query, department_name_chunk)

            # use the name and scores from zero shot classifier to upddate dictionary
            for i in range (0, len(data['scores'])):
                department_name = data['labels'][i]
                department_dict[department_name] = data['scores'][i]

        # Sort the departments by score and return the top 3, format {department_names : score}
        department_dict = dict(sorted(department_dict.items(), key=lambda x: x[1], reverse=True)[:result_size])
        
        # change values to ids -> department_dict {names : ids}
        department_dict = {key: departments.get(name=key).id for key in department_dict.keys()}
        return department_dict

    def rank_subsections(self, query, department_id : int, result_size : int):
        department_obj = Department.objects.get(id = department_id)
        subsections = Subsection.objects.filter(department=department_obj)
        subsection_names = [subsection.name for subsection in subsections]
        subsection_dict = {}
        # Split the subsections names into chunks of size 10
        subsection_name_chunks = [subsection_names[i:i+10] for i in range(0, len(subsection_names), 10)]
        for subsection_name_chunk in subsection_name_chunks:
            data = ml_api.get_data(query, subsection_name_chunk)
            # use the name and scores from zero shot classifier to upddate dictionary
            for i in range (0, len(data['scores'])):
                subsection_name = data['labels'][i]
                subsection_dict[subsection_name] = data['scores'][i]
        # Sort the subsections by score and return the top 3, format {names : score}        
        subsection_dict = dict(sorted(subsection_dict.items(), key=lambda x: x[1], reverse=True)[:result_size])

        # change values to ids -> subsections_dict {names : ids}
        subsection_dict = {key : subsections.get(name=key).id for key in subsection_dict.keys()}
        return subsection_dict
    
    def rank_faqs(self, query, subsection_id : int, result_size: int):
        faqs = FAQ.objects.filter(subsection_id=subsection_id)
        faq_questions = [faq.questions for faq in faqs]
        faqs_dict = {}
        # Split the faq names into chunks of size 10
        faq_question_chunks = [faq_questions[i:i+10] for i in range(0, len(faq_questions), 10)]
        for faq_question_chunk in faq_question_chunks:
            data = ml_api.get_data(query, faq_question_chunk)
            # use the name and scores from zero shot classifier to upddate dictionary
            for i in range (0, len(data['scores'])):
                faq_question = data['labels'][i]
                faqs_dict[faq_question] = data['scores'][i]

        # Sort the FAQs by score and return the top 5, format {question : score}          
        faqs_dict = dict(sorted(faqs_dict.items(), key=lambda x: x[1], reverse=True)[:result_size])
        
        # change the value to answers -> Faq_dict {question : answer}
        faqs_dict = {questions : faqs.get(questions=questions).answer for questions in faqs_dict.keys() }
        return faqs_dict

