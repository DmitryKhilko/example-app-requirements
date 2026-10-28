/* ==========================================================================
   status-filter.js — отбор перечня функциональностей по статусам и по названию

   Страница docs/feature-map.md формируется скриптом scripts/generate_docs.py.
   В ней:
     * в разделе «Статистика» стоят плитки статусов (ссылки с классом .status-tile и атрибутом
       data-filter="<код статуса>": значок статуса и число) — они же кнопки фильтра, а также
       кнопка «Сбросить» (атрибут data-filter-reset);
     * у каждой ссылки на спецификацию есть атрибут data-status="<код статуса>";
     * списки спецификаций — вложенные сворачиваемые блоки details.feature-block
       («Модуль» → «Субмодуль»); в summary блока — название и счётчики статусов.

   Скрипт реагирует на клики по плиткам и скрывает фичи, чей статус не выбран.
   Выбрано несколько статусов — показываются фичи любого из них; не выбрано ни одного —
   все. Модули, субмодули и разделы без видимых фич скрываются. Выбранные плитки
   подсвечиваются классом is-active. Выбор попадает в адрес страницы
   (?status=ready,development), поэтому им можно делиться.

   Сворачиваемые блоки. Вначале все блоки свёрнуты. Раскрытие модуля сворачивает соседний
   раскрытый модуль и все субмодули внутри; раскрытие субмодуля сворачивает соседний
   раскрытый субмодуль: развёрнут один модуль и один субмодуль. Пока действует отбор (выбран
   статус или введён текст), эти правила отключены, а блоки с совпадениями раскрыты
   автоматически; после «Сбросить» всё снова свёрнуто.

   Отбор по названию. Под кнопками стоит поле <input data-feature-search>. Введённый текст
   (без учёта регистра) ищется в названии модуля, субмодуля и функциональности: если совпало
   название модуля или субмодуля, показываются все их функциональности. Отбор по статусу и по
   названию действуют одновременно: показываются функциональности, подходящие под оба условия.
   Текст попадает в адрес страницы (?q=...).

   Итоги пересчитываются при каждом изменении отбора и всегда показывают то, что подходит под оба условия
   (выбранные статусы и текст). Плитки (числа в `<span data-stat>`): число по каждому статусу; плитка «Всего» (`<span data-stat-total>`) — общий итог.
   Счётчики в заголовках блоков модулей и субмодулей (`<span data-count-item>`) — то, что осталось
   в списке под заголовком; статусы с нулём там скрываются.

   Если по условиям отбора ничего не найдено, под полем поиска появляется сообщение
   «Нет данных, соответствующих условиям отбора» с кнопкой «Сбросить» (снимает фильтр по
   статусам и очищает поле поиска).

   Скрытие делается инлайн-стилем (display:none), поэтому от extra.css скрипт не зависит.

   Почему обработчик клика повешен на весь документ, а не на кнопки. На сайте включена
   мгновенная навигация (navigation.instant): содержимое страниц подменяется без полной
   перезагрузки, и кнопки каждый раз создаются заново. Обработчик на document создаётся
   один раз и работает всегда (делегирование событий). Применение выбора
   из адреса страницы выполняет init(): его запускает событие темы document$ после загрузки и
   после каждой мгновенной навигации; повторные вызовы безопасны.
   ========================================================================== */

(function () {
  "use strict";

  var PARAM = "status";
  var PARAM_Q = "q";
  var query = "";    // введённый текст отбора по названию (в нижнем регистре)
  var ACTIVE_CLASS = "is-active";
  var wasFiltering = false;   // действовал ли отбор при предыдущем применении (для возврата блоков в исходное состояние)
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

    /* Название узла иерархии: у блока модуля или субмодуля — первый strong или em в summary, у функциональности —
       её ссылка; счётчики статусов в заголовках блоков в поиск не попадают */
    function label(node) {
      var el = node.matches("details") ? node.querySelector(":scope > summary > strong, :scope > summary > em")
                                       : node.querySelector(":scope > a");
      return el ? el.textContent.toLowerCase() : "";
    }

    /* Совпадение с текстом отбора: название самой функциональности или блока модуля / субмодуля, в котором она лежит */
    function queryOk(a) {
      if (!query) return true;
      if (label(a.closest("li")).indexOf(query) !== -1) return true;
      for (var d = a.closest("details.feature-block"); d && root.contains(d); d = d.parentElement && d.parentElement.closest("details.feature-block")) {
        if (label(d).indexOf(query) !== -1) return true;
      }
      return false;
    }

    function matches(a) { return statusOk(a) && queryOk(a); }

    /* Фича и любой её родитель (субмодуль, модуль) скрыты, если ни одна из вложенных ссылок
       не подходит под выбранные статусы и текст отбора */
    var filtering = any || !!query;
    Array.prototype.forEach.call(root.querySelectorAll("li, details.feature-block"), function (node) {
      var inner = node.querySelectorAll("a[data-status]");
      if (!inner.length) return;
      var some = Array.prototype.some.call(inner, matches);
      setVisible(node, some);
      /* Блок с совпадениями раскрывается; после сброса отбора все блоки возвращаются в исходное (свёрнутое) состояние */
      if (node.matches("details")) {
        if (filtering) node.open = some;
        else if (wasFiltering) node.open = false;
      }
    });
    wasFiltering = filtering;

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
      section.forEach(function (el) {
        /* Блоки модулей показывает или скрывает цикл выше; здесь их можно только скрыть вместе с разделом */
        if (el.matches("details.feature-block")) { if (!show) setVisible(el, false); }
        else setVisible(el, show);
      });
    });

    /* Итоги в разделе «Статистика»: по каждому статусу и «Всего» — то, что подходит под оба условия отбора */
    var byStatus = {}, total = 0;
    Array.prototype.forEach.call(links, function (a) {
      if (!matches(a)) return;
      var code = a.getAttribute("data-status");
      byStatus[code] = (byStatus[code] || 0) + 1;
      total++;
    });
    Array.prototype.forEach.call(root.querySelectorAll("[data-stat]"), function (el) {
      el.textContent = byStatus[el.getAttribute("data-stat")] || 0;
    });
    Array.prototype.forEach.call(root.querySelectorAll("[data-stat-total]"), function (el) { el.textContent = total; });

    /* Счётчики в заголовках блоков модулей и субмодулей: что осталось в списке под заголовком */
    Array.prototype.forEach.call(root.querySelectorAll("details.feature-block"), function (block) {
      var summary = block.querySelector(":scope > summary");
      var items = summary ? Array.prototype.filter.call(summary.children, function (el) { return el.hasAttribute("data-count-item"); }) : [];
      if (!items.length) return;
      var counts = {};
      Array.prototype.forEach.call(block.querySelectorAll("a[data-status]"), function (a) {
        if (matches(a)) counts[a.getAttribute("data-status")] = (counts[a.getAttribute("data-status")] || 0) + 1;
      });
      var last = null;
      items.forEach(function (item) {
        var n = counts[item.getAttribute("data-count-item")] || 0;
        item.querySelector("[data-count]").textContent = n;
        item.hidden = n === 0;
        item.classList.remove("is-last");
        if (n) last = item;
      });
      if (last) last.classList.add("is-last");   /* после последнего видимого счётчика запятой нет */
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

  /* Раскрытие блока: пока отбор не действует, соседний блок того же уровня и вложенные блоки сворачиваются.
     Обработчик на заголовок summary: стандартное действие (открыть или закрыть блок) он не отменяет. */
  document.addEventListener("click", function (e) {
    var summary = e.target.closest ? e.target.closest("details.feature-block > summary") : null;
    if (!summary || wasFiltering) return;
    var block = summary.parentElement;
    if (block.open) return;   // блок закрывается — остальное не трогаем
    Array.prototype.forEach.call(block.parentElement.children, function (el) {
      if (el !== block && el.matches("details.feature-block")) el.open = false;
    });
    Array.prototype.forEach.call(block.querySelectorAll("details.feature-block"), function (el) { el.open = false; });
  }, true);

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

  /* document$ — событие темы: срабатывает после загрузки страницы и после каждой мгновенной навигации */
  if (typeof document$ !== "undefined") {
    document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
