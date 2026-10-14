from django.urls import path,include
from django.shortcuts import redirect
from core import views
urlpatterns=[path("accounts/",include("django.contrib.auth.urls")),path("",lambda request:redirect("flow")),path("flowdesk/",views.flow,name="flow"),path("flowdesk/create/",views.create_request,name="create"),path("flowdesk/<int:pk>/",views.detail,name="detail"),path("flowdesk/export/",views.flow_export,name="flow_export")]
