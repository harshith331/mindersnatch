anime({
    targets: ".icon",
    translateY: ["-20%", "0%"],
    direction: "alternate",
    loop: true,
    easing: "linear"
  });
  
  $(".icon").click(function() {
    anime({
    targets: ".icon",
    translateY: ["-100%", "0%"]
  });
  })
  
  anime({
    targets: ".container",
    translateY: ["200%", "0%"],
  })
  
  anime({
    targets: ".bounce",
    translateY: ["-100%", "0%"],
    direction: "alternate",
    loop: true,
    easing: "easeOutBounce"
  });
  
  function bounce() {
    anime({
      targets: ".bounce",
      left: "+=50px",
      easing: "linear",
      complete: function(anim) {
        if($(window).width() < $(".bounce").offset().left)       {
          $(".bounce").css("left", "0px");
        }
      bounce();
      }
    });
  }
  
  bounce();
  