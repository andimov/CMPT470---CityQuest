$(document).ready(function() {
function attend (event_id) {
    $.ajax({
        type: "POST",
        url: "/attend/"
        data: {"event": event_id},
        success: function() {
            $("#event-attend-" + event_id).hide()
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    return false;
}

$("a.attend").click(function() {
    var event_id = parseInt(this.id.split("-")[2]);
    return attend(event_id);
})

});
