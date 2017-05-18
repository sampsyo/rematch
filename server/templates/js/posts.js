$(document).ready(function() {
    $(".post_star").on("click", function() {
        if($(this).hasClass('star') && $(this).hasClass('ion-ios-star')) {
            $(this).addClass('star-outline');
            $(this).addClass('ion-ios-star-outline');
            $(this).removeClass('star');
            $(this).removeClass('ion-ios-star');
            $.ajax({
                type: 'DELETE',
                url: "/api/students/" + $('meta').data('user-id') + "/" + $(this).data('id'),
                success: function(response) {
                    console.log(response);
                },
                failure: function(response) {
                    console.log(response);
                }
            });
        } else {
            $(this).addClass('star');
            $(this).addClass('ion-ios-star');
            $(this).removeClass('star-outline');
            $(this).removeClass('ion-ios-star-outline');
            $.ajax({
                type: 'POST',
                url: "/api/students/" + $('meta').data('user-id') + "/" + $(this).data('id'),
                success: function(response) {
                    console.log(response);
                },
                failure: function(response) {
                    console.log(response);
                }
            });
        }
    });
});