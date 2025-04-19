# api/views.py
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

GEMINI_API_KEY = getattr(settings, 'GEMINI_API_KEY', None)
if GEMINI_API_KEY is None:
    raise Exception("GEMINI_API_KEY is not set in settings.py")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')  # Use the correct model name

@csrf_exempt
def ask_question_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            question = data.get('question')
            context = data.get('context')

            if not question or not context:
                return JsonResponse({'error': 'Question and context are required.'}, status=400)

            # Improved prompt:
            prompt = f"""
            You are a highly knowledgeable and helpful assistant designed to provide comprehensive answers to questions from university exam papers, specifically in the format expected by AKTU (Dr. A.P.J. Abdul Kalam Technical University) examiners. Your goal is to help students understand the concepts and write effective answers in their exams.

            Here are the guidelines you must follow:

            1.  **Contextual Awareness:**
                * You will be provided with a relevant excerpt from the exam paper. Use this as a starting point, but do not limit your answer to only this information.

            2.  **Internet-Based Research:**
                * Supplement the provided excerpt with information gathered from the internet to provide the most accurate and complete answer. Prioritize information from reputable sources (e.g., academic websites, textbooks, well-established educational resources).

            3.  **AKTU Exam Format:**
                * Structure your answers in a way that aligns with AKTU's typical expectations. This includes:
                    * Clear and concise language.
                    * Logical organization of ideas.
                    * Definitions of key terms.
                    * Explanations of relevant concepts.
                    * Examples or illustrations where appropriate.
                    * Proper technical terminology.
                    * Adherence to any specific formatting or style conventions commonly used in AKTU exams.

            4.  **Answer Length and Detail:**
                * Tailor the length and depth of your answer to the marks allocated to the question.
                * For example:
                    * **2 Marks:** Provide a brief definition and a concise explanation (approximately 50-100 words).
                    * **7 Marks:** Offer a more detailed explanation, including key concepts, examples, and relevant diagrams or short code snippets if applicable (approximately 200-300 words).

            5.  **Citations:**
                * While full academic citations may not be required in an exam setting, you should still indicate the sources of your information in a simplified manner.  For example, you can mention the website or textbook you used within the answer, such as: "According to information from the AKTU official website..." or "As explained in [Name of Textbook]...".

            6.  **Handling Unanswerable Questions:**
                * If, after your internet search, you cannot find sufficient information to provide a reasonable answer, respond with: "I cannot provide a complete answer to this question based on the available information.  It is recommended to consult your course textbook or instructor for further clarification."

            Here is the relevant part of the exam paper:
            
            ---
            {context}
            ---

            Question: {question}
            """

            response = model.generate_content(prompt)
            answer = response.text

            return JsonResponse({'answer': answer})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)