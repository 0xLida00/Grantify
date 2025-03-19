$(document).ready(function() {
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");

        var icon = $(this).find("i");
        if ($("#wrapper").hasClass("toggled")) {
            // Sidebar is collapsed: change arrow to point right
            icon.removeClass("fa-chevron-left").addClass("fa-chevron-right");
        } else {
            // Sidebar is expanded: change arrow to point left
            icon.removeClass("fa-chevron-right").addClass("fa-chevron-left");
        }
    });
});