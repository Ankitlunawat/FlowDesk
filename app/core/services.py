from django.core.exceptions import PermissionDenied,ValidationError
from django.db import transaction
from .models import ServiceRequest,Activity
TRANSITIONS={"new":{"active"},"active":{"review"},"review":{"done","active"},"done":{"active"}}
@transaction.atomic
def transition(pk,user,action,note=""):
    item=ServiceRequest.objects.select_for_update().get(pk=pk)
    if not user.is_staff and item.owner_id!=user.id:raise PermissionDenied
    if action=="note":
        if not note.strip():raise ValidationError("Enter a note.")
        Activity.objects.create(request=item,actor=user,message=note.strip())
        return item
    target="active" if action=="reopen" else action
    if target not in TRANSITIONS.get(item.state,set()):raise ValidationError("This status change is not allowed.")
    if target=="done" and not user.is_staff:raise PermissionDenied("Approval requires a manager.")
    before=item.get_state_display()
    item.state=target;item.save()
    Activity.objects.create(request=item,actor=user,message=f"{before} → {item.get_state_display()}"+(f": {note.strip()}" if note.strip() else ""))
    return item
def csv_safe(value):
    value=str(value)
    return "'"+value if value.lstrip().startswith(("=","+","-","@")) else value
