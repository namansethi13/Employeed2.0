from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy, reverse
from django.forms import modelformset_factory
from django.http import JsonResponse
from corporates.models import CorporateModel, JobModel
from .models import QuestionModel, TestModel, SkillModel
from .consumers import request_for_submit_test
from .forms import TestForm, QuestionForm
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from datetime import datetime, date

class TestListView(ListView):
    template_name = 'mcq_app/test_list.html'
    queryset = TestModel.objects.all()
    paginate_by: 10

    def get_queryset(self):
        return TestModel.objects.filter(owner = self.request.user)

class TestCreateView(CreateView):
    template_name = 'mcq_app/test_create.html'
    model = TestModel
    success_url = reverse_lazy('test_list')
    form_class = TestForm


class TestUpdateView(UpdateView):
    template_name = 'mcq_app/test_update.html'
    model = TestModel
    success_url = reverse_lazy('test_list')
    form_class = TestForm
    
class TestDetailView(DetailView):
    template_name = 'mcq_app/test_detail.html'
    model = TestModel

    def get_context_data(self, **kwargs):
        context = super(TestDetailView, self).get_context_data(**kwargs)
        test_obj = TestModel.objects.get(id=context['object'].id)
        context['questions'] = QuestionModel.objects.filter(test = test_obj)
        context['job_obj'] = test_obj.job_test
        context['courses'] = context['job_obj'].eligible_courses.all()
        context['skills'] = context['job_obj'].skills.all()
        # saving test_obj id in session
        self.request.session['test_id'] = test_obj.id
        return context


def test_delete(request, pk):
    """
    pk : id of a test
    """
    try:
        test_obj = TestModel.objects.get(id=pk)
        if test_obj.is_active == False:
            test_obj.delete()
    except:
        print(f"Test with id = {pk} not found")

    return redirect(reverse_lazy('test_list')) 


## Questions views

def question_create(request, pk):
    """
    pk: id of a test
    add questions to a test
    """
    test_obj = TestModel.objects.get(id=pk)
    question_owner = CorporateModel.objects.filter(username = request.user.username)[0]
    QuestionFormset = modelformset_factory(QuestionModel,
        form=QuestionForm, extra=test_obj.total_questions, max_num=test_obj.total_questions
    )
    formset = QuestionFormset(data=request.POST or None, queryset=QuestionModel.objects.filter(owner= request.user, test = test_obj))
    if request.method == 'POST':
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.owner = question_owner
                instance.save()
                instance.test.add(test_obj)
            return redirect(reverse_lazy('test_detail', kwargs={'pk': pk}))
        else:
            print("errors = ", formset.errors)
            print("non-form errors = ", formset.non_form_errors())

    return render(request, 'mcq_app/question_create.html', {'formset': formset})


def question_delete(request, pk):
    """
    pk: id of a question

    """

    try:
        question_obj = QuestionModel.objects.get(id=pk).delete()
        print("test id = ", request.session['test_id'])
    except:
        print(f"Qusetion with id = {pk} not found")
    return redirect(reverse_lazy('test_detail', kwargs={'pk': request.session['test_id']}))


def launch_test(request, pk):
    """
    pk: id of a test
    test.is_active become true, and notification send to all eligible candidate
    redirect : test detial page
    """
    try:
        test_obj = TestModel.objects.get(id=pk)
        if test_obj.is_active == False:
            test_obj.is_active = True
            test_obj.save()
    except:
        print(f"Test with id = {pk} not found")
    return redirect(reverse_lazy('test_detail', kwargs={'pk': request.session['test_id']}))


def active_test(request):
    """
    return : all test which are active (is_active is True)
    """
    try:
        if request.method == 'GET':
            tests = TestModel.objects.filter(is_active = True)
            context = {
                'tests' : tests,
            }
            return render(request, 'mcq_app/active_test.html', context=context)
    except:
        print("Error with featching active tests")


def get_test_questions(request, pk):
    """
    pk: primary key of a test
    return: all questions belongs to a test
    """
    try:
        test_obj = TestModel.objects.filter(id=pk)[0]
        questions = QuestionModel.objects.filter(test = test_obj.id)

        # Saving max tab switch in the session
        request.session['warningLeft'] = 3                              

        # addign index to all questions
        i = 1                                                           
        for question in questions:
            question.index = i
            i += 1

        # setting the background task for test submission
        username = request.user.username
        task_id = request_for_submit_test.apply_async(kwargs={'username': username}, countdown=(test_obj.duration * 60))
        # print(">>>  task_id = ", task_id)
        return render(request, 'mcq_app/test_questions.html', {'questions': questions})
    except:
        print("Error with get_test_questions")
        return redirect(reverse('student_dashboard'))

def handle_questionlog(data):
    """
    Frontend sending options choosen for each questions
    will save for temporary in session database
    """
    # print("GET = ", json.dumps(request.GET))
    # get_data = request.headers.get('Getdata')
    # print("get_data = ", get_data)

    # if get_data == 'true':
    #     if request.session['questionlog']: 
    #         data = request.session['questionlog']
    # else:
        #   request.session['questionlog'] =
    #     data = {}
    # return JsonResponse(data)

    print(data)

def handle_tab_switch(request):
    """
    Run consumer for submitting the test from frontend, 
    when tabswiches warning is 0 or less
    """ 
    request.session['warningLeft'] -= 1

    if request.session['warningLeft'] < 0:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            request.user.username,
            {
                'type' : 'submitTest',
                'messages' : 'submit the test'
            }
        )
    data = {
        'warningType' : 'tab switched',
        'warningLeft' : request.session['warningLeft']
    }
    return JsonResponse(data)

def handle_submit_test(request):
    """
    handling submission of answered question in the database
    """
    group_name = request.POST.get('group_name', None)

    if not group_name:
        print("Error in submitting the test with POST request")

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type' : 'submitTest',
            'messages' : 'submit the test'
        }
    )
    return JsonResponse(data = {'status':200})