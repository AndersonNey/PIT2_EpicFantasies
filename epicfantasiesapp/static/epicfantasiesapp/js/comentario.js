document.addEventListener('DOMContentLoaded', function() {
    
    const commentInput1 = document.getElementById('commentInput1');
    const sendCommentButton1 = document.getElementById('sendCommentButton1');
    const commentsList1 = document.getElementById('commentsList1');
    const storyId1 = "1";

    sendCommentButton1.addEventListener('click', function(event) {
        event.preventDefault(); // Impede o envio padrão do formulário

        const comment = commentInput1.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        // Envia o comentário para o backend
        fetch(`api/comentario/${storyId1}/`, { // Ajuste para o endpoint correto
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

            // Cria um novo comentário para adicionar na lista
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId1);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;

            commentsList1.prepend(newComment); // Adiciona o novo comentário no início da lista
            commentInput1.value = ''; // Limpa o campo de entrada do comentário
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';    
                console.log("redirecionar");
            }
        });
    });


    const commentInput2 = document.getElementById('commentInput2');
    const sendCommentButton2 = document.getElementById('sendCommentButton2');
    const commentsList2 = document.getElementById('commentsList2');
    const storyId2 = "2";

    sendCommentButton2.addEventListener('click', function(event) {
        event.preventDefault();

        const comment = commentInput2.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId2}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId2);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList2.prepend(newComment);
            commentInput2.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput3 = document.getElementById('commentInput3');
    const sendCommentButton3 = document.getElementById('sendCommentButton3');
    const commentsList3 = document.getElementById('commentsList3');
    const storyId3 = "3";

    sendCommentButton3.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput3.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId3}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId3);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList3.prepend(newComment);
            commentInput3.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput4 = document.getElementById('commentInput4');
    const sendCommentButton4 = document.getElementById('sendCommentButton4');
    const commentsList4 = document.getElementById('commentsList4');
    const storyId4 = "4";

    sendCommentButton4.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput4.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId4}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId4);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList4.prepend(newComment);
            commentInput4.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput5 = document.getElementById('commentInput5');
    const sendCommentButton5 = document.getElementById('sendCommentButton5');
    const commentsList5 = document.getElementById('commentsList5');
    const storyId5 = "5";

    sendCommentButton5.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput5.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId5}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId5);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList5.prepend(newComment);
            commentInput5.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput6 = document.getElementById('commentInput6');
    const sendCommentButton6 = document.getElementById('sendCommentButton6');
    const commentsList6 = document.getElementById('commentsList6');
    const storyId6 = "6";

    sendCommentButton6.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput6.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId6}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId6);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList6.prepend(newComment);
            commentInput6.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput7 = document.getElementById('commentInput7');
    const sendCommentButton7 = document.getElementById('sendCommentButton7');
    const commentsList7 = document.getElementById('commentsList7');
    const storyId7 = "7";

    sendCommentButton7.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput7.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId7}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId7);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList7.prepend(newComment);
            commentInput7.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput8 = document.getElementById('commentInput8');
    const sendCommentButton8 = document.getElementById('sendCommentButton8');
    const commentsList8 = document.getElementById('commentsList8');
    const storyId8 = "8";

    sendCommentButton8.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput8.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId8}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId8);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList8.prepend(newComment);
            commentInput8.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput9 = document.getElementById('commentInput9');
    const sendCommentButton9 = document.getElementById('sendCommentButton9');
    const commentsList9 = document.getElementById('commentsList9');
    const storyId9 = "9";

    sendCommentButton9.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput9.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId9}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId9);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList9.prepend(newComment);
            commentInput9.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    const commentInput10 = document.getElementById('commentInput10');
    const sendCommentButton10 = document.getElementById('sendCommentButton10');
    const commentsList10 = document.getElementById('commentsList10');
    const storyId10 = "10";

    sendCommentButton10.addEventListener('click', function(event) {
        event.preventDefault();
        const comment = commentInput10.value;

        if (comment.trim() === '') {
            alert('Por favor, escreva um comentário.');
            return;
        }

        fetch(`api/comentario/${storyId10}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ comment: comment })
        })
        .then(response => response.json())
        .then(data => {
            const newComment = document.createElement('div');
            newComment.classList.add('comment');
            newComment.setAttribute('data-story-id-coment-coment', storyId10);
            newComment.innerHTML = `
                <img src="${data.user.profile_picture}" alt="Avatar" class="comment-avatar">
                <div class="comment-content">
                    <p class="comment-author">${data.user.username}</p>
                    <p class="comment-text">${data.comment}</p>
                </div>
            `;
            commentsList10.prepend(newComment);
            commentInput10.value = '';
        })
        .catch(error => {
            console.error('Erro:', error);
            if (typeof error.user_logado === 'undefined') {
                window.location.href = '/entrar';
                console.log("redirecionar");
            }
        });
    });

    

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
