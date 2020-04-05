anime({
  targets: "ul li span",
  opacity: [0, 1],
  translateX: ["500%", "0%"],
  duration: 1000,
  delay: anime.stagger(1000)
})

anime({
  targets: "ul li img",
  opacity: [0, 1],
  translateX: ["-500%", "0%"],
  duration: 1000,
  delay: anime.stagger(1000)
})