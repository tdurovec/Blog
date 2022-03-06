$(document).ready(function(){
    var simplemde = new SipleMDE();

    $("form").on("submit", function(){
        html_render = simplemde.markdown(simplemde.value());
        alert("funkcia sa spustila")
        $("#html_render").val(html_render)
    })
})