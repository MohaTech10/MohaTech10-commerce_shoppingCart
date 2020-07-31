from django.contrib import admin
from .models import *
admin.site.register(Tags)
admin.site.register(Items)
admin.site.register(OrderedItems)
admin.site.register(Orders)