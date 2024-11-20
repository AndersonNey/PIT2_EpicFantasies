
document.addEventListener('DOMContentLoaded', function() {
    const commentInput = document.getElementById('commentInput');
    const sendCommentButton = document.getElementById('sendCommentButton');
    const commentsList = document.getElementById('commentsList');
    const storyId = sendCommentButton.getAttribute('data-story-id-coment');

    sendCommentButton.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        const comment = commentInput.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId}/`, { // Ajuste para o endpoint correto
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Para Django, por exemplo
            },
            body: JSON.stringify({ 
                comment: comment
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erro ao enviar o comentário');
                
            }
            return response.json();
        })
        .then(data => {
            console.log('Comentário enviado com sucesso:', data);


            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;

            commentsList.prepend(newComment); // Adiciona o novo comentário no início da lista
            commentInput.value = ''; // Limpa o campo de entrada do comentário
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined' ){
                window.location.href = '/entrar';    
                console.log("redirecionar")
            }

        });
    });

    // Função para obter o CSRF token em caso de uso com Django
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

