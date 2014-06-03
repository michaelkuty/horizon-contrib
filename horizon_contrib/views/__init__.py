# -*- coding: UTF-8 -*-
import inspect
import json
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

def log_action(request, obj, flag=ADDITION, change_message=None):
    """přídavné logovaní"""
    """obj musí mít implementovanou __unicode__ metodu"""
    if request and obj:

        if not change_message:
            change_message = u"action: %s call_from: %s"% (flag, inspect.stack()[2][3])
        else:
            """rozsireni o informaci z kama bylo volano"""
            change_message = u"%s call_from: %s"% (change_message, inspect.stack()[2][3])

        LogEntry.objects.log_action(
                    user_id=request.user.id,
                    content_type_id=ContentType.objects.get_for_model(obj).pk,
                    object_id=obj.pk,
                    object_repr=unicode(obj.__unicode__()),
                    change_message = change_message,
                    action_flag=flag)
        return True
    return None