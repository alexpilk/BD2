from django.contrib import admin
from django.db.models import Model
from . import models
import inspect


for _, model in models.__dict__.items():
    print(type(model))
    if inspect.isclass(model) and issubclass(model, Model):
        print(model)
        admin.site.register(model)
