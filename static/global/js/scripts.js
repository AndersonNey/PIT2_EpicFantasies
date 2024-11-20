document.addEventListener('DOMContentLoaded', function() {
    var mobileMenu = document.getElementById('mobile-menu');
    var navMenu = document.getElementById('nav-menu');

    mobileMenu.addEventListener('click', function() {
        navMenu.classList.toggle('show');
    });
    
    var tabs = document.querySelectorAll('.profile-menu ul li a');
    tabs.forEach(function(tab) {
        tab.addEventListener('click', function(event) {
            event.preventDefault();
            var target = this.getAttribute('href').substr(1);
            var sections = document.querySelectorAll('.tab-content');
            sections.forEach(function(section) {
                section.classList.remove('active');
            });
            document.getElementById(target).classList.add('active');
            tabs.forEach(function(tab) {
                tab.parentElement.classList.remove('active');
            });
            this.parentElement.classList.add('active');
        });
    });

    var commentButtons = document.querySelectorAll('.comment-button');
    commentButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            var storyCard = this.closest('.story-card');
            var commentsSection = storyCard.querySelector('.comments-section');
            commentsSection.classList.toggle('active');
        });
    });



    // Função de pesquisa
    var searchBar = document.getElementById('search-bar');
    var searchButton = document.getElementById('search-button');
    var autocompleteList = document.getElementById('autocomplete-list');

    searchBar.addEventListener('input', function() {
        var query = this.value.toLowerCase();
        autocompleteList.innerHTML = '';

        if (query.length > 0) {
            var stories = document.querySelectorAll('.story-card');
            stories.forEach(function(story) {
                var storyContent = story.querySelector('.story-content p').textContent.toLowerCase();
                if (storyContent.includes(query)) {
                    var suggestion = document.createElement('div');
                    suggestion.classList.add('autocomplete-suggestion');
                    suggestion.textContent = storyContent.substring(0, 50) + '...';
                    suggestion.addEventListener('click', function() {
                        searchBar.value = storyContent;
                        autocompleteList.innerHTML = '';
                    });
                    autocompleteList.appendChild(suggestion);
                }
            });
        }
    });

    searchButton.addEventListener('click', function() {
        var query = searchBar.value.toLowerCase();
        var stories = document.querySelectorAll('.story-card');
        stories.forEach(function(story) {
            var storyContent = story.querySelector('.story-content p').textContent.toLowerCase();
            if (storyContent.includes(query)) {
                story.style.display = 'block';
            } else {
                story.style.display = 'none';
            }
        });
    });
    var filterDropdown = document.getElementById('filter-dropdown');
    filterDropdown.addEventListener('change', function() {
        var selectedCategory = this.value;
        var stories = document.querySelectorAll('.story-card');

        stories.forEach(function(story) {
            if (selectedCategory === 'all') {
                story.style.display = 'block';
            } else {
                // Supondo que cada story-card tenha uma data-category atribuído para a categoria
                var storyCategory = story.getAttribute('data-category');
                if (storyCategory === selectedCategory) {
                    story.style.display = 'block';
                } else {
                    story.style.display = 'none';
                }
            }
        });
    });

});

// Copiar link para area de transferencia
document.querySelectorAll(".copy-link").forEach(function(link) {
    link.addEventListener("click", function(event) {
        event.preventDefault();
        var linkText = this.getAttribute("data-link");
        navigator.clipboard.writeText(linkText)
            .then(function() {
                alert("Link copiado para a área de transferência: " + linkText);
            })
            .catch(function(err) {
                console.error('Erro ao copiar: ', err);
            });
    });
});

// Realizar denuncia
document.addEventListener('DOMContentLoaded', function() {
    const reportButtons = document.querySelectorAll(".report-button");

    reportButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Impede o comportamento padrão do link

            const id_store = this.getAttribute("data-story-id-alert");

            const confirmacao = confirm("Tem certeza que deseja denunciar?");

            if (confirmacao) {
                const csrftoken = getCookie('csrftoken'); // Obtém o token CSRF

                fetch(`/api/denuncia/${id_store}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrftoken 
                    },
                    body: JSON.stringify({}) 
                })
                .then(response => {
                    if (response.redirected) {
                        throw new Error('Usuário não autenticado. Redirecionado para a página de login.');
                    } else if (!response.ok) {
                        // Outros erros
                        if (response.status === 401) {
                            throw new Error('Erro 401: Não autorizado.');
                        } else {
                            throw new Error('Erro ao fazer a denúncia');
                        }
                    }
                    return response.json();
                }).then(data => {
                    console.log('Denúncia realizada com sucesso.');
                }).catch(error => {
                    if (error.message.includes('Usuário não autenticado')) {
                        console.error('Erro específico:', error.message);
                        window.location.href = '/entrar';
                    } else if (error.message.includes('401')) {
                        console.error('Erro específico:', error.message);
                    } else {
                        console.error('Erro:', error);
                    }
                });
            } else {
                console.log("Denúncia cancelada pelo usuário.");
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});



