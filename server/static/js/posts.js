// posts
$(document).ready(function() {
    $(".star").on("click", function() {
        console.log('Unstar this post id: ' + $(this).data('id'));
        // can grab out of jinja, since its globally defined unlike each post
        console.log('user netid: ' + '{{profile.netid}}');
        $.ajax({
            type: 'DELETE',
            url: "/api/students/laz37/1",
            done: function(response) {
                console.log(response);
            }
        });
    });
    $(".star-outline").on("click", function() {
        console.log('Star this post: ' + $(this).data('id'));
        console.log('user netid: ' + profile);
    });
});