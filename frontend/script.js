 // DOM Elements
 const messagesContainer = document.getElementById('messages-container');
 const messageInput = document.getElementById('message-input');
 const sendButton = document.getElementById('send-button');
 const sidebarToggle = document.querySelector('.sidebar-toggle');
 const sidebar = document.querySelector('.sidebar');
 
 // Sample responses based on style
 const responseStyles = {
     normal: "I appreciate your question. Here's what I can tell you about that...",
     professional: "Thank you for your inquiry. Upon analysis, I can provide the following information...",
     casual: "Hey there! Great question! So here's the deal...",
     academic: "Upon examination of this query, several pertinent factors emerge for consideration..."
 };

 // Auto-resize textarea
 messageInput.addEventListener('input', () => {
     messageInput.style.height = 'auto';
     messageInput.style.height = messageInput.scrollHeight + 'px';
     
     // Enable/disable send button based on content
     sendButton.disabled = messageInput.value.trim() === '';
 });

 // Send message on button click
 sendButton.addEventListener('click', sendMessage);

 // Send message on Enter key (but allow Shift+Enter for new line)
 messageInput.addEventListener('keydown', (e) => {
     if (e.key === 'Enter' && !e.shiftKey) {
         e.preventDefault();
         if (!sendButton.disabled) {
             sendMessage();
         }
     }
 });

 // Toggle sidebar on mobile
 sidebarToggle.addEventListener('click', () => {
     sidebar.style.display = sidebar.style.display === 'none' ? 'flex' : 'none';
 });

 // Handle sending messages
 function sendMessage() {
     const messageText = messageInput.value.trim();
     if (!messageText) return;
     
     // Add human message
     addMessage(messageText, 'human');
     
     // Clear input
     messageInput.value = '';
     messageInput.style.height = 'auto';
     sendButton.disabled = true;
     
     // Simulate typing indicator
     const loadingMessage = addMessage('Thinking...', 'assistant');
     
     // Simulate response delay
     setTimeout(() => {
         // Remove loading message
         messagesContainer.removeChild(loadingMessage);
         
         // Add AI response based on selected style
         const stylePrefix = responseStyles[selectedStyle] || responseStyles.normal;
         const response = `${stylePrefix} ${generateResponse(messageText)}`;
         addMessage(response, 'assistant');
         
         // Scroll to bottom
         messagesContainer.scrollTop = messagesContainer.scrollHeight;
     }, 1500);
     
     // Scroll to bottom
     messagesContainer.scrollTop = messagesContainer.scrollHeight;
 }

 // Add message to the chat
 function addMessage(text, sender) {
     const messageDiv = document.createElement('div');
     messageDiv.className = `message ${sender}-message`;
     
     const headerDiv = document.createElement('div');
     headerDiv.className = 'message-header';
    //  headerDiv.textContent = sender === 'human' ? 'You' : 'Claude';
     
     const contentDiv = document.createElement('div');
     contentDiv.className = 'message-content';
     contentDiv.textContent = text;
     
     messageDiv.appendChild(contentDiv);
     
     messagesContainer.appendChild(messageDiv);
     return messageDiv;
 }

 // Generate a simple response based on the message
 function generateResponse(message) {
     message = message.toLowerCase();
     
     if (message.includes('hello') || message.includes('hi')) {
         return "Hello! It's nice to chat with you. How can I assist you today?";
     } else if (message.includes('help')) {
         return "I'm here to help! Feel free to ask me questions, request assistance with tasks, or just chat about topics you're interested in.";
     } else if (message.includes('thanks') || message.includes('thank you')) {
         return "You're welcome! I'm glad I could be of assistance.";
     } else {
         return "That's an interesting point. I'd be happy to discuss this further or provide more information if you'd like.";
     }
 }

 // Set initial size of textarea
 messageInput.style.height = 'auto';