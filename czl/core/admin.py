from django.contrib import admin
from .models import Organization, Publication, Document


admin.site.register(Organization)
admin.site.register(Publication)
admin.site.register(Document)
