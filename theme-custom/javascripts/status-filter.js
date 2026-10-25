/* ==========================================================================
   status-filter.js — фильтр перечня функциональностей по статусам

   Страница docs/feature-map.md формируется скриптом scripts/build_feature_map.py.
   В ней:
     * над перечнем стоят кнопки темы (ссылки с классом .md-button, см. документацию
       Zensical «Buttons») с атрибутом data-filter="<код статуса>" и кнопка «Сбросить»
       с атрибутом data-filter-reset;
     * у каждой ссылки на спецификацию есть атрибут data-status="<код статуса>".

   Скрипт реагирует на клики по кнопкам и скрывает фичи, чей статус не выбран.
   Выбрано несколько статусов — показываются фичи любого из них; не выбрано ни одного —
   все. Модули, субмодули и разделы без видимых фич скрываются. Выбранные кнопки
   выделяются классом md-button--primary. Счётчики в заголовках модулей остаются
   полными (это итоги по модулю, а не результат фильтра). Выбор попадает в адрес
   страницы (?status=ready,development), поэтому им можно делиться.

   Скрытие делается инлайн-стилем (display:none), поэтому от extra.css скрипт не зависит.

   Почему обработчик клика повешен на весь документ, а не на кнопки. На сайте включена
   мгновенная навигация (navigation.instant): содержимое страниц подменяется без полной
   перезагрузки, и кнопки каждый раз создаются заново. Обработчик на document создаётся
   один раз и работает всегда (делегирование событий, как в tiles.js). Применение выбора
   из адреса страницы выполняет init(): его запускает наблюдатель MutationObserver после
   каждой смены содержимого; повторные вызовы безопасны.
   ========================================================================== */

(function () {
  "use strict";

  var PARAM = "status";
  var ACTIVE_CLASS = "md-button--primary";
  var active = {};   // выбранные статусы: { "ready": true, ... }

  function article() { return document.querySelector(".md-content__inner"); }

  function codesOnPage(root) {
    return Array.prototype.map.call(root.querySelectorAll("a[data-filter]"), function (a) {
      return a.getAttribute("data-filter");
    });
  }

  /* Читает выбранные статусы из адреса страницы (неизвестные коды отбрасываются) */
  function readUrl(known) {
    var result = {};
    try {
      var raw = new URLSearchParams(window.location.search).get(PARAM) || "";
      raw.split(",").forEach(function (code) {
        if (known.indexOf(code) !== -1) result[code] = true;
      });
    } catch (e) { /* адрес недоступен — фильтр пустой */ }
    return result;
  }

  /* Записывает выбор в адрес страницы, не создавая записи в истории браузера */
  function writeUrl() {
    try {
      var url = new URL(window.location.href);
      var codes = Object.keys(active);
      if (codes.length) url.searchParams.set(PARAM, codes.join(","));
      else url.searchParams.delete(PARAM);
      window.history.replaceState(window.history.state, "", url.toString());
    } catch (e) { /* не критично */ }
  }

  function setVisible(el, visible) { el.style.display = visible ? "" : "none"; }

  function apply() {
    var root = article();
    if (!root) return;
    var any = Object.keys(active).length > 0;

    function matches(a) { return !any || active[a.getAttribute("data-status")]; }

    /* Фича и любой её родитель (субмодуль, модуль) скрыты, если ни одна из вложенных ссылок
       не подходит под выбранные статусы */
    Array.prototype.forEach.call(root.querySelectorAll("li"), function (li) {
      var inner = li.querySelectorAll("a[data-status]");
      if (inner.length) setVisible(li, Array.prototype.some.call(inner, matches));
    });

    /* Раздел (заголовок h2 и всё до следующего заголовка) скрыт, если в нём не осталось фич */
    Array.prototype.forEach.call(root.querySelectorAll("h2"), function (h) {
      var section = [h];
      for (var el = h.nextElementSibling; el && !/^H[1-6]$/.test(el.tagName); el = el.nextElementSibling) {
        section.push(el);
      }
      var inSection = [];
      section.forEach(function (el) {
        Array.prototype.forEach.call(el.querySelectorAll("a[data-status]"), function (a) { inSection.push(a); });
      });
      var show = !inSection.length || inSection.some(matches);
      section.forEach(function (el) { setVisible(el, show); });
    });

    /* Состояние кнопок */
    Array.prototype.forEach.call(root.querySelectorAll("a[data-filter]"), function (btn) {
      var on = !!active[btn.getAttribute("data-filter")];
      btn.classList.toggle(ACTIVE_CLASS, on);
      btn.setAttribute("role", "button");
      btn.setAttribute("aria-pressed", on ? "true" : "false");
    });
    writeUrl();
  }

  /* Клик по кнопке фильтра или «Сбросить» (захват события до обработчика мгновенной навигации) */
  document.addEventListener("click", function (e) {
    var target = e.target.closest ? e.target.closest("a[data-filter], a[data-filter-reset]") : null;
    if (!target) return;
    e.preventDefault();
    e.stopPropagation();

    if (target.hasAttribute("data-filter-reset")) {
      active = {};
    } else {
      var code = target.getAttribute("data-filter");
      if (active[code]) delete active[code]; else active[code] = true;
    }
    apply();
  }, true);

  /* Применение выбора из адреса после загрузки страницы и после мгновенной навигации */
  function init() {
    var root = article();
    if (!root) return;
    var first = root.querySelector("a[data-filter]");
    if (!first || first.hasAttribute("data-sf-init")) return;
    first.setAttribute("data-sf-init", "");
    active = readUrl(codesOnPage(root));
    apply();
  }

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
