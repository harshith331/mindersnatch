var Objects = anime({
  targets: '#Home',
  strokeDashoffset: [anime.setDashoffset, 0],
  easing: 'easeInOutSine',
  duration: 3000,
  delay: function(el, i) { return i * 250 },
  direction: 'alternate',
  loop: true
});


var Objects = anime({
  targets: '#Stay',
  keyframes: [
    {translateY: -20},
    {translateY: -40},
    {translateY: 20},
    {translateY: 0},
    {translateY: 0}
  ],
  duration: 4000,
  easing: 'easeOutElastic(1, .8)',
  loop: true,
  direction: 'alternate'
  
});



var Objects = anime({
  targets: '#Vector_62, #Vector_61, #Vector_60, #Vector_59, #Vector_63, #Vector_64',
  rotate: 360,
  duration: 3000,
  direction: 'alternate',
  loop: true
});