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

// Contador de visitas (GoatCounter). Solo se muestra a partir de MIN_VISITAS; si no responde, no se ve nada.
(function () {
  var MIN_VISITAS = 500;
  var el = document.getElementById('visitas');
  if (!el || !window.fetch || !/luisarevalo\.es$/.test(location.hostname)) return;
  fetch('https://luisarevalo.goatcounter.com/counter/TOTAL.json')
    .then(function (r) { return r.ok ? r.json() : null; })
    .then(function (d) {
      if (!d || !d.count) return;
      var n = parseInt(String(d.count).replace(/\D/g, ''), 10);
      if (!(n >= MIN_VISITAS)) return;
      el.textContent = n.toLocaleString(document.documentElement.lang || 'es') + ' ' + el.dataset.label;
      el.hidden = false;
    })
    .catch(function () {});
})();
