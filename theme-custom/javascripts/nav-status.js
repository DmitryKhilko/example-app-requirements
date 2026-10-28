/* ==========================================================================
   nav-status.js — значки статусов спецификаций в левом меню

   Задача. Перед названием каждой спецификации в левом меню показать значок её статуса
   (бэклог, анализ, готово к разработке, разработка, реализовано, архив) и убрать штатный
   значок темы («i» в кружке) справа от названия.

   Как работает.
   1. Генератор scripts/generate_docs.py пишет docs/nav-status.json: {"адрес страницы": "статус"}.
      Файл публикуется в корне сайта и обновляется вместе с меню, вручную его не правят.
   2. Этот скрипт загружает файл, находит в левом меню ссылки на эти страницы, ставит перед названием
      <span class="nav-status-icon" data-status="…"> (рисунок — в extra.css, разделы 8 и 9), а все прочие
      вложенные элементы ссылки, кроме названия, прячет (штатный значок темы).
   Правое оглавление страницы («Содержание») значков не имеет.
   Скрипт не зависит от разметки конкретной версии темы. Если файл статусов не загрузился,
   ничего не меняется и работает штатное отображение темы.

   Подключение: extra_javascript в zensical.toml (выше раздела [project.theme]).
   Расположение: theme-custom/javascripts/nav-status.js (имя файла используется для вычисления адреса сайта).
   ========================================================================== */
(function () {
  "use strict";

  var script = document.currentScript;
  var match = script && script.src && script.src.match(/^(.*\/)javascripts\/nav-status\.js(?:[?#].*)?$/);
  if (!match) return;
  var base = match[1];                                   // адрес корня сайта, например https://host/path/
  var basePath = new URL(base).pathname;
  var map = null;

  // Адрес страницы относительно корня сайта: «specifications/catalog/search-text/»
  function pageKey(href) {
    var path;
    try { path = decodeURIComponent(new URL(href, window.location.href).pathname); } catch (e) { return ""; }
    if (path.indexOf(basePath) !== 0) return "";
    path = path.slice(basePath.length).replace(/index\.html$/, "");
    return path && path.slice(-1) !== "/" && !/\.html$/.test(path) ? path + "/" : path;
  }

  function decorate() {
    if (!map) return;
    var links = document.querySelectorAll("a.md-nav__link[href]");
    Array.prototype.forEach.call(links, function (a) {
      // Правое оглавление страницы («Содержание») и якорные ссылки значков статуса не получают
      if (a.closest(".md-nav--secondary, .md-sidebar--secondary") || a.getAttribute("href").charAt(0) === "#") return;
      var status = map[pageKey(a.href)];
      if (!status || a.getAttribute("data-status") === status) return;
      if (a.querySelector("nav, ul")) return;            // ссылка-группа с вложенными страницами

      // Название — вложенный элемент с самым длинным текстом; остальные элементы (значок «i» темы) прячем
      var title = null, longest = -1;
      Array.prototype.forEach.call(a.children, function (child) {
        if (child.classList.contains("nav-status-icon")) return;
        var length = (child.textContent || "").trim().length;
        if (length > longest) { longest = length; title = child; }
      });
      Array.prototype.forEach.call(a.children, function (child) {
        if (child !== title && !child.classList.contains("nav-status-icon")) child.style.display = "none";
      });

      var icon = a.querySelector(".nav-status-icon");
      if (!icon) {
        icon = document.createElement("span");
        icon.className = "nav-status-icon";
        icon.setAttribute("aria-hidden", "true");
        a.insertBefore(icon, a.firstChild);
      }
      icon.setAttribute("data-status", status);
      a.setAttribute("data-status", status);
    });
  }

  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () { scheduled = false; decorate(); });
  }

  fetch(base + "nav-status.json", { credentials: "same-origin" })
    .then(function (response) { return response.ok ? response.json() : null; })
    .then(function (data) {
      if (!data) return;
      map = data;
      decorate();
      // Мгновенная навигация (navigation.instant) перерисовывает меню без перезагрузки страницы
      new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
    })
    .catch(function () { /* без файла статусов остаётся штатное отображение темы */ });
})();
