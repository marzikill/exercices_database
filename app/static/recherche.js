$( "#search_button" ).click(function() {
    // Éxecute une requette sur l'api lorsque
    // le bouton de recherche est cliqué
    $.ajax({
        url: "/recherche/api",
	data: $('form').serialize(),
        type: 'POST',
        success: display_results
    });
});

function display_results(result) {
    // $("#search_result_wrapper").text("Recherche effectuée avec succès");
    $("#search_result_wrapper").empty();
    $("#search_result_wrapper").append(result);
    console.log("Résultat de la requête :", result);
}
