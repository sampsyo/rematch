// posts
$(document).ready(function() {
    $(".star").on("click", function() {
        $(this).removeClass('star');
        $(this).removeClass('ion-ios-star');
        $(this).addClass('star-outline');
        $(this).addClass('ion-ios-star-outline');
        console.log('Unstar this post id: ' + $(this).data('id'));
        // can grab out of jinja, since its globally defined unlike each post
        console.log('user netid: ' + '{{profile.netid}}');
        $.ajax({
            type: 'DELETE',
            url: "/api/students/laz37/" + $(this).data('id'),
            success: function(response) {
                console.log(response);
                $(this).removeClass('star').addClass('star-outline');
            },
            failure: function(response) {
                console.log(response);
            }
        });
    });
    $(".star-outline").on("click", function() {
        $(this).addClass('star');
        $(this).addClass('ion-ios-star');
        $(this).removeClass('star-outline');
        $(this).removeClass('ion-ios-star-outline');
        console.log('Star this post: ' + $(this).data('id'));
        console.log('user netid: ' + 'laz37');
        $.ajax({
            type: 'POST',
            url: "/api/students/laz37/" + $(this).data('id'),
            success: function(response) {
                console.log(response);
                $(this).toggleClass('star-outline star');
            },
            failure: function(response) {
                console.log(response);
            }
        });
    });
});