document.addEventListener('DOMContentLoaded', () => {
    const sessionId = document.getElementById('session_id').textContent.trim();
    const userUsername = document.getElementById('user_username').textContent.trim();
    const chatBox = document.querySelector('.chat-box');
    const messageForm = document.getElementById('messageForm');
    const messageInput = messageForm.querySelector('[name=content]');

    if (!sessionId) {
        console.error('Session ID отсутствует. Начните чат, чтобы создать сессию.');
        return;
    }

    // Прокручиваем чат вниз при загрузке страницы
    chatBox.scrollTop = chatBox.scrollHeight;

    // Создаём WebSocket соединение
    const chatSocket = new WebSocket(
        `${window.location.protocol === 'https:' ? 'wss://' : 'ws://'}${window.location.host}/ws/support/${sessionId}/`
    );

    // Обработка отправки сообщения
    messageForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message,
                'sender': userUsername,
            }));
            messageInput.value = '';  // Очистка поля ввода после отправки
        }
    });

    // Обработка входящих сообщений
    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const newMessage = document.createElement('div');
        newMessage.classList.add('mb-2');
        newMessage.innerHTML = `<strong>${data.sender}:</strong> <span>${data.message}</span>`;
        chatBox.appendChild(newMessage);
        chatBox.scrollTop = chatBox.scrollHeight;  // Автопрокрутка вниз
    };

    // Обработка закрытия соединения
    chatSocket.onclose = function () {
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('text-danger', 'mb-2');
        errorMessage.textContent = 'Соединение с сервером закрыто.';
        chatBox.appendChild(errorMessage);
    };

    // Обработка ошибок соединения
    chatSocket.onerror = function (error) {
        console.error('Ошибка WebSocket:', error);
        const errorMessage = document.createElement('div');
        errorMessage.classList.add('text-danger', 'mb-2');
        errorMessage.textContent = 'Ошибка соединения с сервером.';
        chatBox.appendChild(errorMessage);
    };
});
