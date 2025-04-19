from django.core.management.base import BaseCommand
from portal.models import QuestionPaper
from PyPDF2 import PdfReader
import os

class Command(BaseCommand):
    help = 'Populate text_content field for existing QuestionPaper records'

    def handle(self, *args, **kwargs):
        papers = QuestionPaper.objects.all()

        for paper in papers:
            if paper.file and not paper.text_content:
                try:
                    # Extract text from PDF
                    text = self.extract_text_from_pdf(paper.file.path)
                    paper.text_content = text
                    paper.save()
                    self.stdout.write(self.style.SUCCESS(f"Processed {paper.subject}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to process {paper.subject}: {e}"))

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            for page in reader.pages:
                text += page.extract_text()
        return text
