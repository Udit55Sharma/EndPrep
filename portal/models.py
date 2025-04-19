import fitz
from django.db import models
from django.contrib.auth.models import User
class QuestionPaper(models.Model):
    YEAR_CHOICES = [
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ]
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science Engineering'),
        ('IT', 'Information Technology'),
        ('Allied', 'Allied Branches'),
    ]
    year_of_study = models.CharField(max_length=10, choices=YEAR_CHOICES)
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES, blank=True, null=True)  # Optional for 1st year
    paper_year = models.CharField(max_length=9)  # e.g., "2018-19"
    subject = models.CharField(max_length=100)
    file = models.FileField(upload_to="papers/")
    text_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.subject} ({self.year_of_study} - {self.paper_year})"
    
    def save(self, *args, **kwargs):
        if self.file and not self.text_content:
            self.text_content = extract_pdf_text(self.file.path)
        super().save(*args, **kwargs)


def extract_pdf_text(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text("text")
    return text

def extract_pdf_questions(pdf_path):
    document = fitz.open(pdf_path)
    questions = []
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text = page.get_text("text")
        questions += extract_questions_from_text(text)
    print(questions)
    return questions

def extract_questions_from_text(text):
    lines = text.split('\n')
    questions = [line for line in lines if line.endswith('?')]
    return questions

class DiscussionThread(models.Model):
    paper = models.OneToOneField('QuestionPaper', on_delete=models.CASCADE, related_name='discussion_thread')

class Comment(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    upvotes = models.ManyToManyField(User, related_name='upvoted_comments', blank=True)

    def upvote_count(self):
        return self.upvotes.count()
    
    

