anime({
  targets: "ul li span.name",
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

history.pushState(null, null, document.URL);
window.addEventListener('popstate', function () {
  history.pushState(null, null, document.URL);
});