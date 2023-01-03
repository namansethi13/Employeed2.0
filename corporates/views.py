from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site 
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView
from corporates.choices import JobStatusType
from tests.models import TestModel
from tests.forms import TestForm
from .models import CorporateModel, JobModel, SkillModel
from .forms import JobForm
from .tasks import handle_job_post
import logging

logger = logging.getLogger(__name__)


class JobListView(ListView):
    template_name = "corporates/job_list.html"
    def get_queryset(self): 
        queryset = JobModel.objects.filter(owner = self.request.user).prefetch_related('skills')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        for job in context['object_list']:
            test_obj = TestModel.objects.get(job_test = job)
            job.start_date = test_obj.start_date
            job.end_date = test_obj.end_date
        return context

def job_create_view(request):
    if request.method == 'GET':
        job_form = JobForm()
        test_form = TestForm()
        return render(request, 
            'corporates/job_create.html', 
            {'job_form': job_form, 
            'test_form':test_form}
        )
    elif request.method == 'POST':
        job_form = JobForm(request.POST)
        test_form = TestForm(request.POST)

        if job_form.is_valid() and test_form.is_valid():
            corporate_obj = CorporateModel.objects.get(username = request.user.username)

            job_obj = job_form.save(commit=False)
            job_obj.owner = corporate_obj
            job_obj.save()
            for skill in job_form.cleaned_data.get('skills'):
                job_obj.skills.add(skill)
            for course in job_form.cleaned_data.get('eligible_courses'):
                job_obj.eligible_courses.add(course)

            test_obj = test_form.save(commit=False)
            test_obj.job_test = job_obj
            test_obj.owner = corporate_obj
            test_obj.save()
            return redirect(reverse_lazy('question_create', kwargs={'pk': test_obj.id}))

        return render(request, 'corporates/job_create.html', 
        {'job_form': job_form, 
        'test_form':test_form})
    

class JobUpdateView(UpdateView):
    template_name = 'corporates/job_update.html'
    model = JobModel
    success_url = reverse_lazy('job_list')
    form_class = JobForm

class JobDetialView(DetailView):
    template_name = 'corporates/job_detail.html'
    model = JobModel

    def get_context_data(self, **kwargs):
        context = super(JobDetialView, self).get_context_data(**kwargs)
        job_obj = JobModel.objects.filter(id=kwargs['object'].id)[0]
        context['skills'] = job_obj.skills.all()
        context['courses'] = job_obj.eligible_courses.all()
        context['test_obj'] = TestModel.objects.filter(job_test=job_obj)[0]
        return context

def job_delete_view(request, pk):
    try:
        job_obj = JobModel.objects.filter(id=pk, owner=request.user)[0]
        try:
            test_obj = TestModel.objects.filter(job_test = job_obj)[0]
            if test_obj.is_active == False:
                job_obj.delete()
        except:
            job_obj.delete()
    except:
        print(f"Job with id = {pk} not found")

    return redirect(reverse_lazy('job_list'))

def job_post_background(request, pk):
    try:
        if JobModel.objects.filter(id=pk, owner=request.user).exists():
            domain = get_current_site(request).domain
            handle_job_post.delay(pk, domain, request.user.id)
        return redirect(reverse_lazy('job_list'))
    except:
        print("failed")
    return redirect(reverse_lazy('job_list'))