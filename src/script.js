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

// Filtro de temas del blog. Las ideas sin publicar solo se ven con "Todos".
(function () {
  var bar = document.querySelector('.topic-filter');
  if (!bar) return;
  var items = document.querySelectorAll('.posts > li');
  var empty = document.querySelector('.topic-empty');
  bar.hidden = false;
  bar.addEventListener('click', function (e) {
    var btn = e.target.closest('.topic');
    if (!btn) return;
    var topic = btn.dataset.topic;
    bar.querySelectorAll('.topic').forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
    var shown = 0;
    items.forEach(function (li) {
      var tags = (li.dataset.tags || '').split(' ');
      var show = !topic || tags.indexOf(topic) !== -1;
      li.hidden = !show;
      if (show) shown++;
    });
    if (empty) empty.hidden = shown > 0;
  });
})();
