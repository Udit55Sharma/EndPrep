from django.contrib import admin
from .models import QuestionPaper

@admin.register(QuestionPaper)
class QuestionPaperAdmin(admin.ModelAdmin):
    list_display = ('subject', 'year_of_study', 'branch', 'paper_year')
    list_filter = ('year_of_study', 'branch', 'paper_year')
