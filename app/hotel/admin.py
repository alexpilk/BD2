from django.contrib import admin
from django.db.models import Model
from . import models
import inspect


for _, model in models.__dict__.items():
    if inspect.isclass(model) and issubclass(model, Model):
        admin.site.register(model)
