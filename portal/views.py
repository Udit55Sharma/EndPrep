from django.shortcuts import render, get_object_or_404
from .models import DiscussionThread, Comment
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.http import FileResponse
from django.conf import settings
from .models import QuestionPaper
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
import json


def home(request):
    return render(request,'homepage.html')

def question_papers_list(request):
    papers_by_year = {
        '1st Year': QuestionPaper.objects.filter(year_of_study='1st Year'),
        '2nd Year': QuestionPaper.objects.filter(year_of_study='2nd Year'),
        '3rd Year': QuestionPaper.objects.filter(year_of_study='3rd Year'),
        '4th Year': QuestionPaper.objects.filter(year_of_study='4th Year'),
    }
    return render(request, 'pdfs.html', {'papers_by_year': papers_by_year})

def download_paper(request, pk):
    paper = get_object_or_404(QuestionPaper, pk=pk)
    return FileResponse(paper.file, as_attachment=True)

def papers_view(request):
    year = request.GET.get('year')
    branch = request.GET.get('branch')
    paper_year = request.GET.get('paper_year')
    papers = QuestionPaper.objects.all()
    if year:
        papers = papers.filter(year_of_study=year)
    if branch and year != '1st':
        papers = papers.filter(branch=branch)
    if paper_year:
        papers = papers.filter(paper_year=paper_year)
        
    context = {
        'papers': papers,
        'years': ['1st', '2nd', '3rd', '4th'],
        'branches': ['CSE', 'IT', 'Allied'],
        'paper_years': papers.values_list('paper_year', flat=True).distinct(),
    }
    return render(request, 'papers.html', context)

def get_filtered_papers(request):
    year = request.GET.get('year')
    branch = request.GET.get('branch')
    paper_year = request.GET.get('paper_year')

    papers = QuestionPaper.objects.all()

    if year:
        papers = papers.filter(year_of_study=year)

    if branch and year != "1st": 
        papers = papers.filter(branch=branch)

    if paper_year:
        papers = papers.filter(paper_year=paper_year)

    papers_data = []
    for paper in papers:
        papers_data.append({
            'subject': paper.subject,
            'file_url': paper.file.url,
        })

    return JsonResponse({'papers': papers_data})


def paper_detail(request, paper_id):
    paper = get_object_or_404(QuestionPaper, id=paper_id)
    thread, _ = DiscussionThread.objects.get_or_create(paper=paper)
    return render(request, 'paper_detail.html', {'paper_id': paper_id, 'paper': paper, 'thread': thread,  'current_user': request.user.username})


def get_comments(request, thread_id):
    thread = get_object_or_404(DiscussionThread, id=thread_id)
    comments = thread.comments.filter(parent__isnull=True).order_by('-created_at').select_related('user')
    data = []
    for comment in comments:
        data.append({
            "id": comment.id,
            "content": comment.content,
            "user": comment.user.username,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M"),
            "upvote_count": comment.upvote_count(),
            "can_delete": comment.user == request.user,
            "replies": [
                {
                    "id": reply.id,
                    "content": reply.content,
                    "user": reply.user.username,
                    "created_at": reply.created_at.strftime("%Y-%m-%d %H:%M"),
                    "upvote_count": reply.upvote_count(),
                    "can_delete": comment.user == request.user,
                }
                for reply in comment.replies.all()
            ],
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def post_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        thread = get_object_or_404(DiscussionThread, id=data.get('thread_id'))
        content = data.get('content')
        parent_id = data.get('parent_id')

        if not content:
            return JsonResponse({"error": "Content cannot be empty."}, status=400)

        parent_comment = None
        if parent_id:
            parent_comment = get_object_or_404(Comment, id=parent_id, thread=thread)

        comment = Comment.objects.create(thread=thread, user=request.user, content=content, parent=parent_comment)
        return JsonResponse({"success": True, "comment_id": comment.id})

    return JsonResponse({"error": "Invalid request method."}, status=400)

def is_admin(user):
    return user.is_staff or user.is_superuser

@csrf_exempt
@login_required

def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, user=request.user)
        comment.delete()
        return JsonResponse({'success': True})
    except Comment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Comment not found or permission denied'}, status=404)
    