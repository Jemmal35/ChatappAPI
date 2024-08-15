const roomName = "your_room_name"; // Set the room name dynamically
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + roomName + '/'
);

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

// Sending a message
document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // Enter key
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    }
};



const socket = new WebSocket('ws://localhost:8000/ws/chat/jemal>/'); // Update with your WebSocket URL

socket.onopen = () => {
    console.log('WebSocket connection established.');
    socket.send(JSON.stringify({ message: 'Hello, Jemmal!' })); // Send a message
};

socket.onmessage = (event) => {
    console.log('Message from server:', event.data); // Handle incoming messages
};

socket.onclose = () => {
    console.log('WebSocket connection closed.');
};
