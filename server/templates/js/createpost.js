var TAGS = {{all_tags | safe}}
var COURSES = {{all_courses | safe}};

console.log(TAGS);
console.log(COURSES);

$('.tags-input').tagsinput({
    typeahead: {
        source: TAGS
    },
    freeInput: false,
    // Typeahead fix
    onTagExists: function() {
        setTimeout(function() {
            $(">input[type=text]",".bootstrap-tagsinput").val("");
        }, 1);
    }
});
$('.tags-input').on('itemAdded', function(event) {
    setTimeout(function(){
        $(">input[type=text]",".bootstrap-tagsinput").val("");
    }, 1);
});
// No Enter button
$('.bootstrap-tagsinput').keydown(function(event){
    if(event.keyCode == 13) {
        event.preventDefault();
        return false;
    }
});

$('.courses-input').tagsinput({
    typeahead: {
        source: COURSES
    },
    freeInput: false,
    // Typeahead fix
    onTagExists: function() {
        setTimeout(function() {
            $(">input[type=text]",".bootstrap-tagsinput").val("");
        }, 1);
    }
});
$('.courses-input').on('itemAdded', function(event) {
    setTimeout(function(){
        $(">input[type=text]",".bootstrap-tagsinput").val("");
    }, 1);
});
// No Enter button
$('.bootstrap-tagsinput').keydown(function(event){
    if(event.keyCode == 13) {
        event.preventDefault();
        return false;
    }
});

var typingTimer;                //timer identifier
var doneTypingInterval = 500;  //time in ms (5 seconds)

//on keyup, start the countdown
$('#post_description').keyup(function(){
    clearTimeout(typingTimer);
    if ($('#post_description').val()) {
        typingTimer = setTimeout(doneTyping, doneTypingInterval);
    }
});

//user is "finished typing," do something
function doneTyping () {
    var description = $('#post_description').val().toLowerCase();
    $.each(TAGS, function(i, value) {
        if (description.includes(value) && value.length > 1 &&
                value != 'other') {
            $('.tags-input').tagsinput('add', value);
        }
    });
}
