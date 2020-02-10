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

function toggleLoginButton(buttonId) {
    if ($('#' + buttonId + ' button').text().indexOf('Connect') > -1) {
        $('#' + buttonId + ' button').attr("disabled", true);
        $('#' + buttonId + ' button').text("Loading...");
    }
    else {
        $('#' + buttonId + ' button').text("Connect");
        $('#' + buttonId + ' button').attr("disabled", false);
    }
    
}

// submit form to server via AJAX
$(document).on('submit', '#login-creds', function (e) {
    toggleLoginButton(e.target.id);
    $.ajax({
        type: 'POST',
        url: '/ajax/login_creds/',
        data: {
            creds: JSON.stringify(getUserPassFromPage()),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (response) {
            $('#' + e.target.id + ' button').remove();
            $("#creds-error-message").text("Successfully logged in!");
            $("#creds-error-message").removeClass("alert alert-danger");
            $("#creds-error-message").addClass("alert alert-success");
            location.reload();
        },
        error: function (data) {
            toggleLoginButton(e.target.id);
            $("#creds-error-message").text("Error: Unable to log in with the provided credentials.");
            $("#creds-error-message").addClass("alert alert-danger");
        },
    });
});


// submit form to server via AJAX
$(document).on('submit', '#login-id', function (e) {
    toggleLoginButton(e.target.id);
    $.ajax({
        type: 'POST',
        url: '/ajax/login_id/',
        data: {
            acc_id: $("#login-id-id").val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (response) {
            $('#' + e.target.id + ' button').remove();
            $("#id-error-message").text("Successfully logged in!");
            $("#id-error-message").removeClass("alert alert-danger");
            $("#id-error-message").addClass("alert alert-success");
            location.reload();
        },
        error: function (data) {
            toggleLoginButton(e.target.id);
            $("#id-error-message").text("Error: Unable to log in with the provided team ID.");
            $("#id-error-message").addClass("alert alert-danger");
        }
    });
});
