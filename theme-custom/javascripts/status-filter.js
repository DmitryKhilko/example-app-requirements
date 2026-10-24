/* ==========================================================================
   status-filter.js — фильтр перечня функциональностей по статусам

   Страница docs/feature-map.md формируется скриптом scripts/build_feature_map.py.
   В ней:
     * у каждой ссылки на спецификацию есть атрибут data-status="<код статуса>";
     * в блоке «Обозначения» (<div class="admonition info status-cols">) название
       каждого статуса обёрнуто в <span data-status="<код>">.

   Скрипт строит над перечнем панель кнопок (по одной на статус, значок и название
   берутся из блока «Обозначения», в скобках — число фич) и скрывает фичи, чей статус
   не выбран. Если выбрано несколько статусов, показываются фичи любого из них;
   если не выбрано ни одного — все. Модули, субмодули и разделы без видимых фич
   скрываются. Счётчики в заголовках модулей остаются полными (это итоги, а не
   результат фильтра). Выбор попадает в адрес страницы (?status=ready,development),
   поэтому им можно делиться. Без JavaScript страница показывает всё.

   Подключение: extra_javascript в zensical.toml. Стили панели — в extra.css, раздел 5.

   Почему скрипт сам следит за страницей. На сайте включена мгновенная навигация
   (navigation.instant): страницы подгружаются без полной перезагрузки. Поэтому
   наблюдатель MutationObserver повторно запускает init() при каждой смене содержимого;
   init() безопасен для повторных вызовов (панель создаётся один раз на страницу).
   ========================================================================== */

(function () {
  "use strict";

  var PARAM = "status";
  var HIDDEN = "sf-hidden";

  /* Читает выбранные статусы из адреса страницы */
  function readUrl(known) {
    var result = {};
    try {
      var raw = new URLSearchParams(window.location.search).get(PARAM) || "";
      raw.split(",").forEach(function (code) {
        if (known.indexOf(code) !== -1) result[code] = true;
      });
    } catch (e) { /* адрес недоступен — фильтр просто пустой */ }
    return result;
  }

  /* Записывает выбор в адрес страницы, не создавая записи в истории браузера */
  function writeUrl(active) {
    try {
      var url = new URL(window.location.href);
      var codes = Object.keys(active);
      if (codes.length) url.searchParams.set(PARAM, codes.join(","));
      else url.searchParams.delete(PARAM);
      window.history.replaceState(window.history.state, "", url.toString());
    } catch (e) { /* не критично */ }
  }

  function init() {
    var article = document.querySelector(".md-content__inner");
    if (!article || article.querySelector(".status-filter")) return;

    var links = article.querySelectorAll("a[data-status]");
    var legendBlock = article.querySelector(".admonition.status-cols");
    if (!links.length || !legendBlock) return;

    var legendItems = legendBlock.querySelectorAll("li span[data-status]");
    var codes = Array.prototype.map.call(legendItems, function (el) {
      return el.getAttribute("data-status");
    });
    var anchorHeading = article.querySelector("h2");
    if (!codes.length || !anchorHeading) return;

    var active = readUrl(codes);

    /* ---- Панель фильтра ---- */
    var bar = document.createElement("div");
    bar.className = "status-filter";
    bar.setAttribute("role", "group");
    bar.setAttribute("aria-label", "Фильтр по статусу");

    var label = document.createElement("span");
    label.className = "status-filter__label";
    label.textContent = "Фильтр по статусу:";
    bar.appendChild(label);

    var buttons = {};
    Array.prototype.forEach.call(legendItems, function (span) {
      var code = span.getAttribute("data-status");
      var count = article.querySelectorAll('a[data-status="' + code + '"]').length;

      var button = document.createElement("button");
      button.type = "button";
      button.className = "status-filter__btn";
      button.setAttribute("data-filter", code);

      /* Значок и название копируются из пункта легенды (значок уже превращён темой в SVG) */
      Array.prototype.forEach.call(span.parentNode.childNodes, function (node) {
        var copy = node.cloneNode(true);
        if (copy.removeAttribute) copy.removeAttribute("data-status");
        button.appendChild(copy);
      });
      var badge = document.createElement("span");
      badge.className = "status-filter__count";
      badge.textContent = String(count);
      button.appendChild(badge);

      button.addEventListener("click", function () {
        if (active[code]) delete active[code]; else active[code] = true;
        apply();
      });
      buttons[code] = button;
      bar.appendChild(button);
    });

    var reset = document.createElement("button");
    reset.type = "button";
    reset.className = "status-filter__reset";
    reset.textContent = "Сбросить";
    reset.addEventListener("click", function () { active = {}; apply(); });
    bar.appendChild(reset);

    anchorHeading.parentNode.insertBefore(bar, anchorHeading);

    /* ---- Применение фильтра ---- */
    function apply() {
      var any = Object.keys(active).length > 0;

      /* Фича (и любой её родитель — субмодуль, модуль) скрыта, если ни одна из вложенных
         ссылок не подходит под выбранные статусы */
      Array.prototype.forEach.call(article.querySelectorAll("li"), function (li) {
        var inner = li.querySelectorAll("a[data-status]");
        if (!inner.length) return;
        var visible = !any || Array.prototype.some.call(inner, function (a) {
          return active[a.getAttribute("data-status")];
        });
        li.classList.toggle(HIDDEN, !visible);
      });

      /* Раздел (заголовок h2 и всё до следующего заголовка) скрыт, если в нём не осталось фич */
      var headings = article.querySelectorAll("h2");
      Array.prototype.forEach.call(headings, function (h) {
        var section = [h];
        for (var el = h.nextElementSibling; el && !/^H[1-6]$/.test(el.tagName); el = el.nextElementSibling) {
          section.push(el);
        }
        var inSection = [];
        section.forEach(function (el) {
          Array.prototype.forEach.call(el.querySelectorAll("a[data-status]"), function (a) { inSection.push(a); });
        });
        var show = !inSection.length || !any || inSection.some(function (a) {
          return active[a.getAttribute("data-status")];
        });
        section.forEach(function (el) { el.classList.toggle(HIDDEN, !show); });
      });

      codes.forEach(function (code) {
        var on = !!active[code];
        buttons[code].classList.toggle("is-active", on);
        buttons[code].setAttribute("aria-pressed", on ? "true" : "false");
      });
      reset.disabled = !any;
      writeUrl(active);
    }

    apply();
  }

  /* Запуск при загрузке и после каждой мгновенной навигации */
  var scheduled = false;
  function schedule() {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () { scheduled = false; init(); });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
  new MutationObserver(schedule).observe(document.body, { childList: true, subtree: true });
})();
