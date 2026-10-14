import os
from datetime import timedelta
from django.core.management.base import BaseCommand,CommandError
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import ServiceRequest,Activity
class Command(BaseCommand):
    help="Create a local workspace with illustrative requests. Requires LOCAL_PASSWORD."
    def handle(self,*args,**options):
        password=os.environ.get("LOCAL_PASSWORD")
        if not password:raise CommandError("Set LOCAL_PASSWORD before seeding.")
        owner,created=User.objects.get_or_create(username="workspace")
        if created:owner.set_password(password);owner.is_staff=True;owner.save()
        samples=[("Website onboarding","Harbor Studio","active","high",2),("Monthly reporting automation","Northline Retail","review","normal",4),("Customer portal access","Cedar Services","new","normal",7),("Invoice export workflow","Fieldstone Partners","active","urgent",-2),("Catalogue update","Atlas Collective","done","normal",-1),("Support intake redesign","Juniper Office","review","high",1)]
        for title,client,state,priority,offset in samples:
            item,created=ServiceRequest.objects.get_or_create(owner=owner,title=title,defaults={"client":client,"description":"Coordinate requirements, confirm acceptance criteria and prepare the requested deliverable. Keep communication and approvals in one place.","state":state,"priority":priority,"due":timezone.localdate()+timedelta(days=offset)})
            if created:
                Activity.objects.create(request=item,actor=owner,message="Request created")
                Activity.objects.create(request=item,actor=owner,message="Requirements reviewed and acceptance criteria recorded")
        self.stdout.write("Workspace ready; existing credentials were not changed.")
