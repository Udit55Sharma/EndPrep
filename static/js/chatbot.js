document.addEventListener("DOMContentLoaded", () => {

    const threadId = document.getElementById("thread-id").value;
    
    const chatbotIcon = document.getElementById('chatbot-icon');
    
    const chatbotWindow = document.getElementById('chatbot-window');
    
    const closeChatbotButton = document.getElementById('close-chatbot');
    
    const chatbotMessages = document.getElementById('chatbot-messages');
    
    const chatbotInput = document.getElementById('chatbot-input');
    
    const sendMessageButton = document.getElementById('send-message');
    
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    const questionPaperContent = chatbotWindow.dataset.paperContent;
    
    let isTyping = false; // Track typing state
    
    
    
    // Show/hide chatbot window with animation
    
    chatbotIcon.addEventListener('click', () => {
    
    if (chatbotWindow.classList.contains('show')) {
    
    chatbotWindow.classList.remove('show');
    
    } else {
    
    chatbotWindow.classList.add('show');
    
    }
    
    });
    
    
    
    // Close chatbot window
    
    closeChatbotButton.addEventListener('click', () => {
    
    chatbotWindow.classList.remove('show');
    
    });
    
    
    
    // Send message on button click or Enter key press
    
    sendMessageButton.addEventListener('click', sendMessage);
    
    chatbotInput.addEventListener('keypress', (event) => {
    
    if (event.key === 'Enter') {
    
    sendMessage();
    
    }
    
    });
    
    
    
    /**
    
    * Sends the user's question and the question paper content to the backend.
    
    */
    
    function sendMessage() {
    
    const question = chatbotInput.value.trim();
    
    if (question) {
    
    addUserMessage(question); // Display user's question
    
    chatbotInput.value = ''; // Clear the input field
    
    startTypingIndicator(); // Show typing indicator
    
    sendMessageButton.disabled = true; // Disable send button
    
    
    
    fetch('/api/ask-question/', { // Your Django API endpoint
    
    method: 'POST',
    
    headers: {
    
    'Content-Type': 'application/json',
    
    'X-CSRFToken': csrfToken // Include CSRF token for Django
    
    },
    
    body: JSON.stringify({
    
    question: question,
    
    context: questionPaperContent // Send the question paper content
    
    })
    
    })
    
    .then(response => response.json()) // Parse the JSON response
    
    .then(data => {
    
    stopTypingIndicator(); // Hide typing indicator
    
    sendMessageButton.disabled = false;
    
    if (data.answer) {
    
    addBotMessage(data.answer); // Display the bot's answer
    
    } else if (data.error) {
    
    addBotMessage('Error: ' + data.error); // Display an error message
    
    } else {
    
    addBotMessage('No response received.'); // Handle empty responses
    
    }
    
    })
    
    .catch(error => {
    
    stopTypingIndicator(); // Hide typing indicator
    
    sendMessageButton.disabled = false;
    
    console.error('Error sending message:', error);
    
    addBotMessage('Failed to send message.'); // Handle network errors
    
    });
    
    }
    
    }
    
    
    
    /**
    
    * Adds a user message to the chat log.
    
    * @param {string} message - The user's message.
    
    */
    
    function addUserMessage(message) {
    
    const messageDiv = document.createElement('div');
    
    messageDiv.classList.add('user-message'); // Apply CSS class for user messages
    
    messageDiv.textContent = message;
    
    const timestampDiv = document.createElement('div');
    
    timestampDiv.classList.add('message-timestamp');
    
    timestampDiv.textContent = formatTimestamp(new Date());
    
    messageDiv.appendChild(timestampDiv);
    
    chatbotMessages.appendChild(messageDiv); // Append to the chat log
    
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to bottom
    
    }
    
    
    
    /**
    
    * Adds a bot message to the chat log.
    
    * @param {string} message - The bot's message.
    
    */
    
    function addBotMessage(message) {
    
    const messageDiv = document.createElement('div');
    
    messageDiv.classList.add('bot-message'); // Apply CSS class for bot messages
    
    messageDiv.textContent = message;
    
    const timestampDiv = document.createElement('div');
    
    timestampDiv.classList.add('message-timestamp');
    
    timestampDiv.textContent = formatTimestamp(new Date());
    
    messageDiv.appendChild(timestampDiv);
    
    chatbotMessages.appendChild(messageDiv); // Append to the chat log
    
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight; // Scroll to bottom
    
    }
    
    
    
    /**
    
    * Displays a typing indicator in the chat log.
    
    */
    
    function startTypingIndicator() {
    
    if (!isTyping) {
    
    const typingDiv = document.createElement('div');
    
    typingDiv.classList.add('typing-indicator');
    
    typingDiv.innerHTML = '<span></span><span></span><span></span>';
    
    chatbotMessages.appendChild(typingDiv);
    
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    
    isTyping = true;
    
    }
    
    }
    
    
    
    /**
    
    * Hides the typing indicator in the chat log.
    
    */
    
    function stopTypingIndicator() {
    
    if (isTyping) {
    
    const typingDiv = chatbotMessages.querySelector('.typing-indicator');
    
    if (typingDiv) {
    
    typingDiv.remove();
    
    }
    
    isTyping = false;
    
    }
    
    }
    
    
    
    /**
    
    * Formats a timestamp in HH:MM format.
    
    * @param {Date} date - The date object.
    
    * @returns {string} - The formatted timestamp.
    
    */
    
    function formatTimestamp(date) {
    
    const hours = String(date.getHours()).padStart(2, '0');
    
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${hours}:${minutes}`;
    
    }
    
    
    
    // Existing discussion forum functionality remains here
    
    function fetchComments() {
    
    fetch(`/api/comments/${threadId}/`)
    
    .then(response => response.json())
    
    .then(data => {
    
    const container = document.getElementById("comments-container");
    
    container.innerHTML = "";
    
    data.forEach(comment => {
    
    const commentElement = document.createElement("div");
    
    commentElement.classList.add("comment");
    
    commentElement.innerHTML = `
    
    <p><strong>${comment.user}</strong> (${comment.created_at}): ${comment.content}</p>
    
    <button class="comment-reply-btn" onclick="replyToComment(${comment.id})">Reply</button>
    
    `;
    
    container.appendChild(commentElement);
    
    
    
    if (comment.replies.length > 0) {
    
    const repliesContainer = document.createElement("div");
    
    repliesContainer.classList.add("replies");
    
    comment.replies.forEach(reply => {
    
    const replyElement = document.createElement("div");
    
    replyElement.innerHTML = `
    
    <p><strong>${reply.user}</strong> (${reply.created_at}): ${reply.content}</p>
    
    
    
    `;
    
    repliesContainer.appendChild(replyElement);
    
    });
    
    container.appendChild(repliesContainer);
    
    }
    
    });
    
    });
    
    }
    
    
    
    document.getElementById("comment-form").addEventListener("submit", event => {
    
    event.preventDefault();
    
    const content = document.getElementById("comment-content").value;
    
    const parentId = document.getElementById("parent-id").value;
    
    
    
    fetch(`/api/comments/`, {
    
    method: "POST",
    
    headers: { "Content-Type": "application/json" },
    
    body: JSON.stringify({ thread_id: threadId, content: content, parent_id: parentId }),
    
    })
    
    .then(response => response.json())
    
    .then(data => {
    
    if (data.success) {
    
    document.getElementById("comment-content").value = "";
    
    document.getElementById("parent-id").value = "";
    
    fetchComments();
    
    }
    
    });
    
    });
    
    
    
    fetchComments();
    
    });
    
    
    
    /**
    
    * Sets the parent comment ID for a reply and focuses the comment input.
    
    * @param {number} commentId - The ID of the parent comment.
    
    */
    
    function replyToComment(commentId) {
    
    document.getElementById("parent-id").value = commentId;
    
    document.getElementById("comment-content").focus();
    
    }