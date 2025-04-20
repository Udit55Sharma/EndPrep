# EndPrep (Exam Paper Chatbot and Discussion Forum)

This project is a web application designed to enhance the learning experience for students by providing a platform to interact with exam papers in a more dynamic way. It includes a chatbot that can answer questions related to the exam paper and a discussion forum for students to collaborate.

## Features

* **Exam Paper Viewing:** Students can view exam papers in PDF format directly within the web application.
* **Chatbot Integration:** A chatbot is integrated into the platform, allowing students to ask questions about the exam paper and receive AI-powered answers.
* **Discussion Forum:** A discussion forum is available for each exam paper, enabling students to discuss questions, answers, and related topics with their peers.
* **User Authentication:** The platform includes user authentication, ensuring that only registered users can access the features.
* **Question Paper Management:** Admins can upload and manage exam papers.
* **Dynamic Content Loading**: Uses AJAX to load chatbot responses and forum comments dynamically.
* **Responsive Design**: Clean and modern UI.

## Technologies Used

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python (Django Framework)
* **PDF Handling:** pdf.js
* **Chatbot:** Google Gemini API
* **Database:** PostgreSQL
* **Version Control:** Git

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/Udit55Sharma/EndPrep.git
    cd EndPrep
    ```

2.  **Set up a Virtual Environment (Recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables:**
    * Create a `.env` file in the project root.
    * Add the following, replacing the values with your actual credentials:
    ```
    GEMINI_API_KEY= YOUR_GEMINI_API_KEY
    SECRET_KEY= your_django_secret_key

    # Database settings
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    DB_PORT=5432
    ```
    
5.  **Apply Migrations:**

    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7.  **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

8.  **Access the Application:**
    Open your web browser and go to `http://localhost:8000/`.

##   Important Considerations

* **PDF.js:** The project uses PDF.js to render PDF files in the browser.
* **Google Gemini API Key:** You MUST obtain a Google Gemini API key and add it to your `.env` file as `GEMINI_API_KEY`.
* **Database:** Ensure your database server is running and configured correctly. The  `settings.py`  file should be configured to connect to your database.
* **requirements.txt:** This file lists all the Python dependencies of the project.  It is crucial for replicating the project environment.
* **CSRF Protection:** Django's CSRF protection is used.  The  `{% csrf_token %}`  template tag is used in the HTML forms, and the  `X-CSRFToken`  header is included in the JavaScript fetch requests.
* **Static Files:** The CSS and JavaScript files are served as static files.  The `{% load static %}` template tag is used to reference them in the HTML.  Make sure static files are configured correctly in your Django project.
* **File Handling:** The project involves file uploads (exam papers).  Ensure that your Django project is configured to handle file uploads correctly (e.g., `MEDIA_URL`, `MEDIA_ROOT` settings).
* **AJAX:** The chatbot and discussion forum features use AJAX to communicate with the server without requiring full page reloads.
* **User Interface**: The UI is created using HTML, CSS, and Javascript.
* **Error Handling**:  The application includes error handling for PDF loading and chatbot API requests.
*	**Security**:  Follow Django security best practices.

##  Further Development

* Implement more advanced chatbot features (e.g., follow-up questions, context retention).
* Enhance the discussion forum (e.g., nested replies, user profiles, voting).
* Add more comprehensive admin features.
* Implement user roles and permissions.
* Add search functionality.
* Improve the UI/UX.

##  Contributing

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Commit your changes.
4.  Push to the branch.
5.  Submit a pull request.

## THANKYOU.
