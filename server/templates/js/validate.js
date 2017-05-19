function validate() {
    var isValid = true;
    // title
    $(".validate-input").each(function() {
        var child = $(this).find("input");
        if (child.val().length <= 0) {
            $(this).addClass("invalidInput");
            isValid = false;
        } else {
            $(this).removeClass("invalidInput");
        }
    });

    $(".validate-input-email").each(function() {
        var child = $(this).find("input");
        var regex = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (!(child.val().match(regex))) {
            isValid = false;
            $(this).addClass("invalidInput");
        } else {
            $(this).removeClass("invalidInput");
        }
    });
    return isValid;
}