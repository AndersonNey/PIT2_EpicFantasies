$(document).ready(function(){
    $('.emoji-link').on('click', function(e) {
        e.preventDefault(); 
        var url = $(this).data('url');
        var storyId = $(this).data('story-id');

        $.ajax({
            url: url,
            type: 'GET', 
            success: function(response) {
                if (typeof response.excelente === 'undefined' ){
                    window.location.href = '/entrar';    
                    console.log("redirecionar")
                }

                $(`.emoji-Excelente[data-story-id="${storyId}"]`).text(response.excelente);
                $(`.emoji-Bom[data-story-id="${storyId}"]`).text(response.bom);
                $(`.emoji-Legal[data-story-id="${storyId}"]`).text(response.legal);
                $(`.emoji-Naoetaolegal[data-story-id="${storyId}"]`).text(response.naoetaolegal);
                $(`.emoji-Naogostei[data-story-id="${storyId}"]`).text(response.naogostei);
            },
            error: function(error) {
                console.log('Erro:', error);
            }
        });
    });
});
