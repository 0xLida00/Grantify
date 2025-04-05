$(document).ready(function() {
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");

        var icon = $(this).find("i");
        if ($("#wrapper").hasClass("toggled")) {
            icon.removeClass("fa-chevron-left").addClass("fa-chevron-right");
        } else {
            icon.removeClass("fa-chevron-right").addClass("fa-chevron-left");
        }
    });
});