$(".navbar li")
    .mouseenter(function () {
        anime({
            targets: ".underline",
            left: $(this).offset().left
        });
        $(".underline").css("width", $(this).width());
    })
    .mouseleave(function () {
        $(".underline").css("width", $(".active").width());
        anime({
            targets: ".underline",
            left: $(".active").offset().left
        });
    });

$(".navbar-icon").click(function () {
    if ($(".navbar .navbar-list").css("visibility") == "visible") {
        $(".navbar .navbar-list").css("visibility", "hidden");
    } else $(".navbar .navbar-list").css("visibility", "visible");
})

var dialog = document.querySelector('dialog');
dialogPolyfill.registerDialog(dialog);
