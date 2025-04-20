# api/views.py
from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from .utils import format_code_blocks

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
                    * 2 Marks: Provide a brief definition and a concise explanation (approximately 50-100 words).
                    * 5 Marks: Offer a more detailed explanation, including key concepts, examples, and relevant diagrams or short code snippets if applicable (approximately 200-300 words).
                    * 10 Marks: Provide a comprehensive and in-depth answer, covering all aspects of the topic, including definitions, detailed explanations, examples, diagrams, code snippets (if relevant), and potential applications or implications. Aim for a well-structured essay-style response (approximately 400-600 words).

            5.  **Handling Specific Question Types:**
                * **Graphs:** If the question requires drawing or explaining a graph:
                    * Provide a clear and accurate description of the graph.
                    * Label all axes and key points in your description.
                    * Explain the relationship between the variables represented in the graph.
                    * Describe any significant trends or patterns.
                    * If possible, provide the data in a table format as well.
                    * Focus on explaining the graph in words, as if you were describing it to someone verbally. Do not try to draw the graph using text characters.
                * **Numericals and Mathematical Solutions:** If the question involves numerical calculations or mathematical solutions:
                    * Show all steps involved in the solution process in a clear, step-by-step manner.
                    * Explain the formulas and concepts used in plain language.
                    * Provide the final answer with appropriate units.
                    * Represent mathematical expressions as clearly as possible using standard text-based conventions.
                        * Use parentheses to avoid ambiguity (e.g., (a + b) / c instead of a + b / c).
                        * Use exponents in the form a^b (e.g., x^2 for x squared).
                        * Represent fractions as a/b (e.g., 1/2 for one-half).
                        * Use sqrt(x) for the square root of x.
                        * Use summation and integration symbols where possible, with clear limits (e.g., sum from i=1 to n of i). If the symbols are not available, describe them in words (e.g., "Summation of i from 1 to n").
                        * Use proper units.
                    * When answering questions involving numerical calculations or mathematical solutions, use LaTeX to format all mathematical expressions.  Enclose LaTeX code for displayed equations in  \[ ... \]  and for inline equations use \( ... \).  For example:
                        * The area of a circle is given by the formula  \(A = \pi r^2\).
                        * To solve for x in the equation \(ax + b = c\), we first subtract b from both sides: \[ax = c - b\].
                        * The integral of x^2 is \(\int x^2 dx = \frac(x^3)(3) + C\)  
                        * Break down complex problems into smaller, more manageable steps.
                * **Code-Based Answers (Programs and Algorithms):** If the question asks for a program or algorithm:
                    * Provide the code in a well-formatted code block, using Markdown's code fencing (```).
                    * Specify the programming language (e.g., ```python, ```java, ```c++).
                    * Include comments within the code to explain the purpose of each section.
                    * Explain the logic and steps involved in the algorithm in plain English, before or after the code block.
                    * Provide example input and output, if applicable.
                    * If the question asks for multiple ways to solve a problem, provide multiple solutions in separate code blocks and explain the trade-offs in plain English.
                    * Adhere to good coding practices (e.g., meaningful variable names, proper indentation, modular design).

            7.  **General Formatting:**
                * Write in a clear, concise, and natural style.
                * To emphasize key terms or important concepts, use bold text. Do not use any Markdown-style formatting, such as asterisks (*) or underscores (_), to indicate bold text.  For example, instead of writing "*Important Concept*", "**Key Term**", or "_Emphasis_", simply write "Important Concept" (with the words "Important Concept" appearing in bold).
                * Do not use any special characters or symbols for any formatting purpose, unless it is part of a code block.
                * Use Markdown formatting only for code blocks.
                * Present information in a way that is easy to read and understand.

            8.  **Handling Unanswerable Questions:**
                * If, after your internet search, you cannot find sufficient information to provide a reasonable answer, respond with: "I cannot provide a complete answer to this question based on the available information. It is recommended to consult your course textbook or instructor for further clarification."

            Here is the relevant part of the exam paper:
            ---
            {context}
            ---

            Question: {question}








            """

            response = model.generate_content(prompt)
            answer = response.text
            formatted_response = format_code_blocks(answer)
            return JsonResponse({'answer': formatted_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)