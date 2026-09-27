from django.contrib import admin

from .models import Company, KBEntry, QueryLog


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'role', 'api_key', 'created_at']
    list_filter = ['role']
    search_fields = ['company_name', 'user__username']


@admin.register(KBEntry)
class KBEntryAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['question', 'answer']


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = ['company', 'search_term', 'results_count', 'queried_at']
    list_filter = ['company']
    search_fields = ['search_term']
