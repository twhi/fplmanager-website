// grab form info from page
function getUserPassFromPage() {
    var user = $("#login-creds-user").val();
    var pass = $("#login-creds-password").val();
    
    var creds = {
        'user': user,
        'pass': pass,
    }
    return creds
}

// submit form to server via AJAX
$(document).on('submit', '#login-creds', function (e) {
    $.ajax({
        type: 'POST',
        url: '/ajax/login_creds/',
        data: {
            creds: JSON.stringify(getUserPassFromPage()),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (response) {
            $("#creds-error-message").text("Successfully logged in!");
            $("#creds-error-message").removeClass("alert alert-danger");
            $("#creds-error-message").addClass("alert alert-success");
            location.reload();
        },
        error: function (data) {
            $("#creds-error-message").text("Error: Unable to log in with the provided credentials.");
            $("#creds-error-message").addClass("alert alert-danger");
        }
    });
});


// submit form to server via AJAX
$(document).on('submit', '#login-id', function (e) {
    $.ajax({
        type: 'POST',
        url: '/ajax/login_id/',
        data: {
            acc_id: $("#login-id-id").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (response) {
            $("#id-error-message").text("Successfully logged in!");
            $("#id-error-message").removeClass("alert alert-danger");
            $("#id-error-message").addClass("alert alert-success");
            location.reload();
        },
        error: function (data) {
            $("#id-error-message").text("Error: Unable to log in with the provided team ID.");
            $("#id-error-message").addClass("alert alert-danger");
        }
    });
});
