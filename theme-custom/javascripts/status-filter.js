/* ==========================================================================
   status-filter.js — отбор перечня функциональностей по статусам и по названию

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

   Отбор по названию. Под кнопками стоит поле <input data-feature-search>. Введённый текст
   (без учёта регистра) ищется в названии модуля, субмодуля и функциональности: если совпало
   название модуля или субмодуля, показываются все их функциональности. Отбор по статусу и по
   названию действуют одновременно: показываются функциональности, подходящие под оба условия.
   Текст попадает в адрес страницы (?q=...).

   Если по условиям отбора ничего не найдено, под полем поиска появляется сообщение
   «Нет данных, соответствующих условиям отбора» с кнопкой «Сбросить» (снимает фильтр по
   статусам и очищает поле поиска).

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
  var PARAM_Q = "q";
  var query = "";    // введённый текст отбора по названию (в нижнем регистре)
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

  function readQuery() {
    try { return new URLSearchParams(window.location.search).get(PARAM_Q) || ""; }
    catch (e) { return ""; }
  }

  /* Записывает выбор в адрес страницы, не создавая записи в истории браузера */
  function writeUrl() {
    try {
      var url = new URL(window.location.href);
      var codes = Object.keys(active);
      if (codes.length) url.searchParams.set(PARAM, codes.join(","));
      else url.searchParams.delete(PARAM);
      if (query) url.searchParams.set(PARAM_Q, query);
      else url.searchParams.delete(PARAM_Q);
      window.history.replaceState(window.history.state, "", url.toString());
    } catch (e) { /* не критично */ }
  }

  function setVisible(el, visible) { el.style.display = visible ? "" : "none"; }

  function apply() {
    var root = article();
    if (!root) return;
    var any = Object.keys(active).length > 0;

    function statusOk(a) { return !any || active[a.getAttribute("data-status")]; }

    /* Название элемента списка: первый элемент strong (модуль), em (субмодуль) или a (функциональность);
       счётчики статусов в заголовках модулей в поиск не попадают */
    function label(li) {
      var el = li.querySelector(":scope > strong, :scope > em, :scope > a");
      return el ? el.textContent.toLowerCase() : "";
    }

    /* Совпадение с текстом отбора: название самой функциональности или любого из её родителей */
    function queryOk(a) {
      if (!query) return true;
      for (var li = a.closest("li"); li && root.contains(li); li = li.parentElement && li.parentElement.closest("li")) {
        if (label(li).indexOf(query) !== -1) return true;
      }
      return false;
    }

    function matches(a) { return statusOk(a) && queryOk(a); }

    /* Фича и любой её родитель (субмодуль, модуль) скрыты, если ни одна из вложенных ссылок
       не подходит под выбранные статусы и текст отбора */
    Array.prototype.forEach.call(root.querySelectorAll("li"), function (li) {
      var inner = li.querySelectorAll("a[data-status]");
      if (inner.length) setVisible(li, Array.prototype.some.call(inner, matches));
    });

    /* Пустой результат: под полем поиска показывается сообщение с кнопкой «Сбросить»
       (блок [data-feature-empty] выводит генератор; кнопка внутри обрабатывается как обычный сброс) */
    var links = root.querySelectorAll("a[data-status]");
    var shown = Array.prototype.filter.call(links, matches).length;
    var empty = root.querySelector("[data-feature-empty]");
    if (empty) empty.hidden = !((any || query) && links.length && shown === 0);

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
    var field = root.querySelector("input[data-feature-search]");
    if (field && field.value.toLowerCase().trim() !== query) field.value = query;
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
      query = "";
    } else {
      var code = target.getAttribute("data-filter");
      if (active[code]) delete active[code]; else active[code] = true;
    }
    apply();
  }, true);

  /* Ввод текста в поле отбора по названию (в том числе очистка крестиком в поле поиска) */
  document.addEventListener("input", function (e) {
    var field = e.target && e.target.matches ? (e.target.matches("input[data-feature-search]") ? e.target : null) : null;
    if (!field) return;
    query = field.value.toLowerCase().trim();
    apply();
  }, true);

  /* Применение выбора из адреса после загрузки страницы и после мгновенной навигации */
  function init() {
    var root = article();
    if (!root) return;
    var first = root.querySelector("a[data-filter], a[data-filter-reset], input[data-feature-search]");
    if (!first || first.hasAttribute("data-sf-init")) return;
    first.setAttribute("data-sf-init", "");
    active = readUrl(codesOnPage(root));
    var q = readQuery();
    query = q.toLowerCase().trim();
    var field = root.querySelector("input[data-feature-search]");
    if (field) field.value = q;
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
