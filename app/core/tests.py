from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied,ValidationError
from datetime import date
from .models import ServiceRequest,Activity
from .services import transition,csv_safe

class WorkflowTests(TestCase):
    def setUp(self):
        self.owner=User.objects.create_user("owner",password="test-only")
        self.other=User.objects.create_user("other",password="test-only")
        self.manager=User.objects.create_user("manager",password="test-only",is_staff=True)
        self.item=ServiceRequest.objects.create(owner=self.owner,title="Request",client="Test",description="Scope",due=date(2026,10,20))
    def test_lifecycle_and_manager_approval(self):
        transition(self.item.pk,self.owner,"active")
        transition(self.item.pk,self.owner,"review")
        with self.assertRaises(PermissionDenied):transition(self.item.pk,self.owner,"done")
        transition(self.item.pk,self.manager,"done")
        self.item.refresh_from_db();self.assertEqual(self.item.state,"done")
        self.assertEqual(Activity.objects.count(),3)
    def test_invalid_transition_rolls_back(self):
        with self.assertRaises(ValidationError):transition(self.item.pk,self.owner,"done")
        self.assertEqual(Activity.objects.count(),0)
    def test_ownership_and_auth(self):
        self.assertEqual(self.client.get("/flowdesk/").status_code,302)
        self.client.force_login(self.other)
        self.assertEqual(self.client.get(f"/flowdesk/{self.item.pk}/").status_code,404)
        with self.assertRaises(PermissionDenied):transition(self.item.pk,self.other,"active")
    def test_create_validation_and_export(self):
        self.client.force_login(self.owner)
        before=ServiceRequest.objects.count()
        r=self.client.post("/flowdesk/create/",{"title":"X","client":"C","description":"S","due":"bad","priority":"normal"})
        self.assertEqual(r.status_code,200);self.assertEqual(ServiceRequest.objects.count(),before)
        self.assertContains(self.client.get("/flowdesk/export/"),"Request")
        self.assertEqual(csv_safe("=1+1"),"'=1+1")
