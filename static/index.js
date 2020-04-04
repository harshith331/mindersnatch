// //Svg Animation
anime({
  targets: 'path',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 1500,
  delay: function(el, i) { return i * 250 }
});

anime({
  targets: ".navbar ul li",
  opacity: [0, 1],
  scale: [0, 1],
  easing: 'easeInOutQuad'
});

// Subtitle Animation
var textWrapper = document.querySelector('.ml11 .letters');
textWrapper.innerHTML = textWrapper.textContent.replace(/([^\x00-\x80]|\w)/g, "<span class='letter'>$&</span>");

anime.timeline()
  .add({
    targets: '.ml11 .line',
    scaleY: [0,1],
    opacity: [0.5,1],
    easing: "easeOutExpo",
    duration: 700
  })
  .add({
    targets: '.ml11 .line',
    translateX: [0, document.querySelector('.ml11 .letters').getBoundingClientRect().width + 10],
    easing: "easeOutExpo",
    duration: 700,
    delay: 100
  }).add({
    targets: '.ml11 .letter',
    opacity: [0,1],
    easing: "easeOutExpo",
    duration: 600,
    offset: '-=775',
    delay: (el, i) => 34 * (i+1)
  }).add({
  targets: ".profile-container img",
  opacity: [0, 1],
  translateX: ["-150%", "-200%"],
  easing: 'easeInOutQuad',
  delay: 200
}).add({
  targets: ".profile-container span",
  opacity: [0, 1],
  translateX: ["-70%", "-30%"],
  easing: 'easeInOutQuad',
  delay: 200
});
 

// Navbar Animation
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