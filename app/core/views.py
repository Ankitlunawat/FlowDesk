import csv
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import ServiceRequest,Activity
from .forms import RequestForm,TransitionForm
from .services import transition,csv_safe

def accessible(user):
    return ServiceRequest.objects.all() if user.is_staff else ServiceRequest.objects.filter(owner=user)

@login_required
def flow(request):
    base=accessible(request.user)
    rows=base.order_by("-updated_at")
    q=request.GET.get("q","");state=request.GET.get("state","")
    if q:rows=rows.filter(Q(title__icontains=q)|Q(client__icontains=q))
    if state in dict(ServiceRequest.STATES):rows=rows.filter(state=state)
    return render(request,"flow.html",{"items":rows,"q":q,"state":state,"states":ServiceRequest.STATES,"total":base.count(),"active":base.filter(state="active").count(),"review":base.filter(state="review").count(),"overdue":base.exclude(state="done").filter(due__lt=timezone.localdate()).count(),"section":"flow","today":timezone.localdate()})

@login_required
def create_request(request):
    form=RequestForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        item=form.save(commit=False);item.owner=request.user;item.save()
        Activity.objects.create(request=item,actor=request.user,message="Request created")
        messages.success(request,"Request created.");return redirect("detail",pk=item.pk)
    return render(request,"form.html",{"form":form,"section":"flow"})

@login_required
def detail(request,pk):
    item=get_object_or_404(accessible(request.user),pk=pk)
    form=TransitionForm(request.POST or None)
    if request.method=="POST" and form.is_valid():
        try:
            transition(pk,request.user,form.cleaned_data["action"],form.cleaned_data["note"])
            messages.success(request,"Request updated.");return redirect("detail",pk=pk)
        except ValidationError as e:form.add_error(None,e)
    return render(request,"detail.html",{"item":item,"form":form,"section":"flow"})

@login_required
def flow_export(request):
    response=HttpResponse(content_type="text/csv")
    response["Content-Disposition"]='attachment; filename="requests.csv"'
    writer=csv.writer(response);writer.writerow(["ID","Title","Client","Priority","Status","Due"])
    for item in accessible(request.user):writer.writerow([item.pk,csv_safe(item.title),csv_safe(item.client),item.priority,item.state,item.due])
    return response
