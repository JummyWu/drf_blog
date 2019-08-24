from django.contrib import admin
from .models import Category, Tag, Aricle


# Register your models here.


class AricleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category',
        'pv', 'owner', 'add_time'
    ]
    list_filter = ['category']
    search_fields = ['title', 'category']
    ordering = ['add_time']
    save_on_top = True

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True


admin.site.register(Category)

admin.site.register(Tag)

admin.site.register(Aricle, AricleAdmin)
