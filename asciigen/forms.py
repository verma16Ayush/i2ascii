from django.db import models
from django.db.models.base import Model
from django.forms import ModelForm
from django.db.models import Model
from .models import Query

class QueryForm(ModelForm):
    class Meta:
        model:Model = Query
        fields = '__all__'
        
