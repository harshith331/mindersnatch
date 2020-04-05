$(".navbar li").mouseenter(function() {
  anime({
    targets: '.underline',
    left: $(this).offset().left
  })
  $(".underline").css("width", $(this).width());
}).mouseleave(function() {
 $(".underline").css("width", $(".active").width());
  anime({
    targets: '.underline',
    left: $(".active").offset().left
  })
})

$(".navbar-icon").click(function() {
  $(".navbar ul").toggle();
  $(".navbar-icon i").toggleClass("fa-bars"); 
  $(".navbar-icon i").toggleClass("fa-times");
  $(".navbar").toggleClass("overlay");
  
  anime({
    targets: '.overlay',
    height: ["0vh", "100vh"],
    duration: 500,
    easing: "linear"
  })
  
  anime({
    targets: '.overlay ul',
    opacity: [0, 1],
    left: ["-50%", "50%"],
    delay: 700,
    duration: 700
  })
})