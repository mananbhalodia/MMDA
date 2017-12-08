from django.contrib import admin
from .models import Category, Dagr, Relationships, Keyword

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['categoryID', 'categoryName']
    list_filter = ['categoryName']
    list_editable = ['categoryName']

class DagrAdmin(admin.ModelAdmin):
    list_display = ['Guid','Location','RealName','LastModified','CategoryID','AssignedName','Size','Type','DateCreated','Author']
    list_filter = ['DateCreated','LastModified','Size','Type','Author']
    list_editable = ['Location','RealName','LastModified','CategoryID','AssignedName','Size','Type','DateCreated','Author']

class RelationshipsAdmin(admin.ModelAdmin):
    list_filter = ['ParentGUID','DateCreated']
    list_display = ['ParentGUID', 'ChildGUID']

class KeywordAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Dagr,DagrAdmin)
admin.site.register(Relationships, RelationshipsAdmin)
admin.site.register(Keyword, KeywordAdmin)
