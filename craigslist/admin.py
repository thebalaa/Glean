from django.contrib import admin
from craigslist.models import *

class cl_GleanResultAdmin(admin.ModelAdmin):
    date_hierarchy = 'posted'
    list_display = ('title', 'posted', 'location')
    ordering = ('-posted',)
class cl_GleanQueryAdmin(admin.ModelAdmin):
    list_display = ('search_term', 'active', 'number_Of_Results')
admin.site.register(cl_Site)
admin.site.register(cl_Site_subSite)
admin.site.register(cl_Category)
admin.site.register(cl_Category_subCat)
admin.site.register(cl_GleanQuery, cl_GleanQueryAdmin)
admin.site.register(cl_GleanResult, cl_GleanResultAdmin)
