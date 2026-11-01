/* ==========================================================================
   status-filter.js — отбор перечня функциональностей по статусам и по названию

   Страницы «Действующие» и «Архив» (index.md подразделов) и индексы модулей
   формируются скриптом scripts/generate_docs.py. В них:
     * под заголовком первого уровня (у индексов модулей — в разделе «Статистика») стоят плитки статусов (ссылки с классом .status-tile и атрибутом
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
   (выбранные статусы и текст). Плитки (числа в `<span data-stat>`): число по каждому статусу; плитка «Всего спецификаций» (`<span data-stat-total>`) — общий итог.
   Счётчики в заголовках блоков модулей и субмодулей (`<span data-count-item>`) — то, что осталось
   в списке под заголовком; статусы с нулём там скрываются.

   Если по условиям отбора ничего не найдено, под полем поиска появляется сообщение
   «Нет данных, соответствующих условиям отбора» с кнопкой «Сбросить» (снимает фильтр по
   статусам и очищает поле поиска).

   Скрытие делается инлайн-стилем (display:none), поэтому от extra.css скрипт не зависит.

   Кнопки «Раскрыть всё» и «Свернуть всё» (a[data-expand-all], a[data-collapse-all], стоят после «Скачать») принудительно раскрывают и
   сворачивают все аккордеоны страницы (раскрываются только блоки, не скрытые отбором).

   Кнопка «Скачать» (a[data-filter-download], стоит после «Сбросить») сохраняет в текстовый файл перечень, который сейчас
   виден на странице, то есть с учётом отбора по статусам и названию (формат — перед обработчиком кнопки ниже).

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

    /* Название узла иерархии: у блока модуля или субмодуля — элемент .feature-title в summary, у функциональности —
       её ссылка; счётчики статусов в заголовках блоков в поиск не попадают */
    function label(node) {
      var el = node.matches("details") ? node.querySelector(":scope > summary .feature-title")
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

    /* Счётчики в заголовках блоков модулей и субмодулей: что осталось в списке под заголовком.
       Первый счётчик — общая сумма (data-count-item="total": «всего: N»), далее по статусам. */
    Array.prototype.forEach.call(root.querySelectorAll("details.feature-block"), function (block) {
      var summary = block.querySelector(":scope > summary");
      var items = summary ? Array.prototype.slice.call(summary.querySelectorAll("[data-count-item]")) : [];
      if (!items.length) return;
      var counts = { total: 0 };
      Array.prototype.forEach.call(block.querySelectorAll("a[data-status]"), function (a) {
        if (!matches(a)) return;
        counts[a.getAttribute("data-status")] = (counts[a.getAttribute("data-status")] || 0) + 1;
        counts.total++;
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

  /* ----- Кнопка «Скачать»: перечень спецификаций, видимый на странице (с учётом отбора), в текстовый файл -----
     Текст собирается из самой страницы (как в releases.js), поэтому всегда совпадает с тем, что видно. Формат:

         Модуль (всего: 4, <статус>: 1, <статус>: 3)
             Субмодуль (всего: 2, <статус>: 2)
                  - [статус] Название спецификации

     Статистика — как в заголовке блока (первой идёт сумма «всего», статусы с нулём не выводятся). Вместо значков —
     русские названия статусов («бэклог», «разработка», …) из атрибута data-titles кнопки («статус=название;…», задаёт
     STATUS_TITLES в scripts/docgen/config.py); у спецификации название стоит в квадратных скобках.
     Модули — без отступа, субмодули — 4 пробела, спецификации — 9 пробелов и «- ». На странице модуля нет блоков модулей:
     там субмодули стоят без отступа, а спецификации — с отступом 5. Файл: UTF-8 с BOM, переводы строк Windows. */
  var EOL = "\r\n";

  function words(text) { return (text || "").replace(/\s+/g, " ").trim(); }
  function shown(el) { return el.style.display !== "none"; }
  function pad(n) { return new Array(n + 1).join(" "); }

  function parseSymbols(raw) {
    var map = {};
    (raw || "").split(";").forEach(function (pair) {
      var i = pair.indexOf("=");
      if (i > 0) map[pair.slice(0, i)] = pair.slice(i + 1);
    });
    return map;
  }

  /* «Название (всего: N, значок: n, …)»: строка статистики берётся из заголовка блока, скрытые счётчики пропускаются */
  function blockTitle(block, symbols) {
    var title = words(block.querySelector(":scope > summary .feature-title").textContent);
    var parts = [];
    Array.prototype.forEach.call(block.querySelectorAll(":scope > summary [data-count-item]"), function (item) {
      if (item.hidden) return;
      var code = item.getAttribute("data-count-item");
      var label = code === "total" ? "всего" : (symbols[code] || code);
      parts.push(label + ": " + words(item.querySelector("[data-count]").textContent));
    });
    return title + (parts.length ? " (" + parts.join(", ") + ")" : "");
  }

  function specLines(block, symbols, indent) {
    var lines = [];
    Array.prototype.forEach.call(block.querySelectorAll(":scope > ul > li"), function (li) {
      var a = li.querySelector("a[data-status]");
      if (!a || !shown(li)) return;
      var code = a.getAttribute("data-status");
      lines.push(pad(indent) + "- [" + (symbols[code] || code) + "] " + words(a.textContent));
    });
    return lines;
  }

  function buildList(root, symbols) {
    var lines = [], heading = "";
    function walk(block, level) {
      lines.push(pad(level * 4) + blockTitle(block, symbols));
      var subs = block.querySelectorAll(":scope > details.feature-block");
      Array.prototype.forEach.call(subs, function (sub) { if (shown(sub)) walk(sub, level + 1); });
      lines = lines.concat(specLines(block, symbols, level * 4 + 5));
    }
    Array.prototype.forEach.call(root.children, function (el) {
      if (/^H2$/.test(el.tagName)) {
        var h = el.cloneNode(true);
        Array.prototype.forEach.call(h.querySelectorAll(".headerlink"), function (x) { x.parentNode.removeChild(x); });
        heading = shown(el) ? words(h.textContent) : "";
        return;
      }
      if (!el.matches("details.feature-block") || !shown(el)) return;
      if (heading) {   /* заголовок раздела выводится один раз перед первым видимым блоком */
        if (lines.length) lines.push("");
        lines.push(heading);
        heading = "";
      }
      /* верхний блок — модуль, а на странице модуля — субмодуль: отступ считается от него, поэтому он стоит без отступа */
      walk(el, 0);
    });
    if (!lines.length) lines.push("Нет данных, соответствующих условиям отбора");
    return lines.join(EOL) + EOL;
  }

  function saveText(name, text) {
    var blob = new Blob(["\ufeff" + text], { type: "text/plain;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = name;
    a.style.display = "none";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  /* Клик по кнопке фильтра, «Сбросить» или «Скачать» (захват события до обработчика мгновенной навигации) */
  document.addEventListener("click", function (e) {
    var target = e.target.closest ? e.target.closest("a[data-filter], a[data-filter-reset], a[data-filter-download], a[data-expand-all], a[data-collapse-all]") : null;
    if (!target) return;
    e.preventDefault();
    e.stopPropagation();

    /* «Раскрыть всё» / «Свернуть всё»: принудительно открывают или закрывают все аккордеоны страницы. Раскрываются только
       видимые блоки (скрытые отбором остаются закрытыми); сворачиваются все. Отбор и поле поиска не меняются. */
    if (target.hasAttribute("data-expand-all") || target.hasAttribute("data-collapse-all")) {
      var open = target.hasAttribute("data-expand-all");
      var scope = article();
      if (!scope) return;
      Array.prototype.forEach.call(scope.querySelectorAll("details.feature-block"), function (block) {
        if (!open) { block.open = false; return; }
        var hidden = false;
        for (var n = block; n && n !== scope; n = n.parentElement) { if (n.style.display === "none") { hidden = true; break; } }
        if (!hidden) block.open = true;
      });
      return;
    }

    if (target.hasAttribute("data-filter-download")) {
      var page = article();
      if (!page) return;
      var name = (target.getAttribute("data-filter-download") || "list").replace(/[^0-9A-Za-z._-]+/g, "_");
      saveText("specifications-" + name + ".txt", buildList(page, parseSymbols(target.getAttribute("data-titles"))));
      return;
    }

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
