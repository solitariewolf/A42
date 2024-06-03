function enviarMensagem() {
    // Pegar a mensagem digitada pelo usuário
    var mensagem = document.getElementById('mensagem').value;

    // Limpar o campo de entrada
    document.getElementById('mensagem').value = '';

    // Enviar a mensagem para o servidor via POST
    fetch('http://localhost:8000/responder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensagem: mensagem })
    })
    .then(response => response.json())
    .then(data => {
        // Exibir a entrada do usuário e a resposta do servidor na interface do chat
        var display = document.getElementById('message-display');
        
        // Criar e exibir a entrada do usuário
        var perguntaUsuario = document.createElement('p');
        perguntaUsuario.textContent = 'Você: ' + mensagem;
        display.appendChild(perguntaUsuario);

        // Criar e exibir a resposta do bot
        var respostaBot = document.createElement('p');
        respostaBot.textContent = 'Bot: ' + data.resposta;
        display.appendChild(respostaBot);

        // Rolar a janela de mensagens para o final
        display.scrollTop = display.scrollHeight;
    })
    .catch(error => {
        console.error('Erro ao enviar mensagem:', error);
    });
}

// Capturar o evento de clique no botão enviar
document.getElementById('enviar').addEventListener('click', enviarMensagem);

// Capturar o evento de pressionar a tecla Enter no campo de entrada
document.getElementById('mensagem').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        enviarMensagem();
    }
});