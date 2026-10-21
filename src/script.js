(function () {
  var home = document.getElementById('home');
  var art = document.getElementById('articulo');
  function route() {
    var showArticle = location.hash === '#articulo';
    art.hidden = !showArticle;
    home.hidden = showArticle;
    if (showArticle) window.scrollTo(0, 0);
  }
  window.addEventListener('hashchange', route);
  document.querySelectorAll('a[href="#articulo"]').forEach(function (a) {
    a.addEventListener('click', function () { setTimeout(route, 0); });
  });
  document.querySelectorAll('a[href^="#"]:not([href="#articulo"])').forEach(function (a) {
    a.addEventListener('click', function () {
      if (!home.hidden) return;
      art.hidden = true; home.hidden = false;
    });
  });
  route();
})();
