from ..models import UserModel
from ..extension import db

def is_exist(model, **kwargs):
    if model.objects.get(**kwargs):
        return True
    else:
        return False