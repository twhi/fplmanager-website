// grab form info from page
function getInfoFromPage() {
    var numSubs = $("#num-subs").val();
    var maxBudget = $("#max-budget").val();
    var optParam = $("#opt-param").val();
    var include = $("#results-include .player-box").map(function () { return $(this).attr("data-id"); }).get();
    var exclude = $("#results-exclude .player-box").map(function () { return $(this).attr("data-id"); }).get();
    var playerElements = {
        'num_subs': typeof numSubs == 'undefined' ? null : numSubs,
        'max_budget': maxBudget,
        'opt_param': optParam,
        'include': include.length == 0 ? null : include,
        'exclude': exclude.length == 0 ? null : exclude,
    }
    return playerElements
}

// submit form to server via AJAX
$(document).on('submit', '#post-form', function (e) {
    $.ajax({
        type: 'POST',
        url: '/ajax/receive_sim_form/',
        data: {
            selected: JSON.stringify(getInfoFromPage()),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: function (response) {
            $("#simulation-results-section").html(response.results_section);
            $("#optimal-team-section").html(response.optimal_squad_table);
            $("#current-team-section").html(response.current_squad_table);
        },
        error: function (data) {
            if (data.status == 500) {
                alert(data.responseJSON.error + '\n\nError code: ' + data.status);
            } 
            else if (data.status == 401) {
                location.reload();
            }         
        }
    });
});

// remove list-item elements if close button is clicked
$('body').on('click', '.close-button', function () {
    $(this).parent('div').remove();
});

// powers the autocomplete ajax calls
$(function () {
    $("#include").autocomplete({
        source: "/ajax/get_autocomplete_players/",
        minLength: 2,
        select: function (event, ui) { //item selected
            appendPlayer(event, ui, "include");
            $(this).val("");
            return false;
        },
    });
    $("#exclude").autocomplete({
        source: "/ajax/get_autocomplete_players/",
        minLength: 2,
        select: function (event, ui) { //item selected
            appendPlayer(event, ui, "exclude");
            $(this).val("");
            return false;
        },
    });
});

// appends selected result to the results section
function appendPlayer(event, ui, player_type) {

    var selectedObj = ui.item; // get selection from dropdown

    // get items already selected by user, if the user tries to select one of these then display an alert
    var alreadySelected = document.getElementById("include-exclude").innerText;
    if (alreadySelected) {
        if (alreadySelected.includes(selectedObj.value)) {
            alert("Player has already been selected!");
            return false;
        }
    }

    // create a box for the player info to sit in
    var player_div = document.createElement('div');
    player_div.setAttribute('class', 'player-box');
    player_div.setAttribute('data-id', ui.item.player_id);

    // create player text element and append to box
    var player = document.createElement('p');
    player.textContent = selectedObj.value;
    player.setAttribute('class', 'player-name-' + player_type);
    player.setAttribute('class', 'player-name');
    player_div.append(player)

    // create close button element and append to box
    var closeButton = document.createElement('div');
    closeButton.textContent = "✖";
    closeButton.setAttribute('class', 'close-button');
    player_div.appendChild(closeButton);

    // append constructed box to results section in DOM
    var target = document.getElementById("results-" + player_type);
    target.appendChild(player_div)
}