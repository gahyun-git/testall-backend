from django.contrib import admin
from .models import Category, PastLifeTest, PastLifeResult

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(PastLifeTest)
class PastLifeTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'participant_count', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    list_filter = ('category',)

@admin.register(PastLifeResult)
class PastLifeResultAdmin(admin.ModelAdmin):
    list_display = ('test', 'past_life_name', 'birth_date', 'ad_shown', 'created_at')
    list_filter = ('test', 'ad_shown')
    search_fields = ('past_life_name', 'past_life_story')
    readonly_fields = ('story_response', 'image_response')
