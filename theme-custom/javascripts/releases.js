/* ==========================================================================
   releases.js — скачивание списка спецификаций релиза в текстовый файл

   Страница docs/releases.md формируется скриптом scripts/generate_docs.py. В ней на каждый релиз стоит сворачиваемый блок
   details.release-block (атрибуты data-release="<номер релиза>" и data-release-date="<дата ДД.ММ.ГГГГ>"); в панели блока — кнопка «Скачать в текстовый файл»
   (ссылка с атрибутом data-release-download) и список спецификаций: у каждой есть ссылка с названием (a[data-status],
   код спецификации — в атрибуте data-id) и под ней описание.

   По клику скрипт собирает текст из самой панели (данные в файле всегда совпадают с тем, что видно на странице) и отдаёт
   его браузеру как файл release-<номер>.txt (UTF-8 с BOM и переводами строк Windows: файл корректно открывается в Блокноте).
   Файл формируется в браузере, сервер не нужен.

   Формат файла:
       Релиз 1.2.1 (15.09.2026)
       Спецификаций: 4

       1. Название спецификации [КОД]
          Описание (строки описания — с отступом)

   Обработчик клика повешен на весь документ (делегирование событий): на сайте включена мгновенная навигация
   (navigation.instant), и кнопки при переходах создаются заново. Клик перехватывается на стадии захвата, чтобы мгновенная
   навигация не обработала ссылку «#».
   ========================================================================== */

(function () {
  "use strict";

  var EOL = "\r\n";

  function words(text) { return (text || "").replace(/\s+/g, " ").trim(); }

  /* Описание: текст панели элемента списка без первой строки (ссылки с названием); строки сохраняются */
  function describe(item) {
    var copy = item.cloneNode(true);
    var link = copy.querySelector("a[data-status]");
    var head = link ? link.closest("p") || link : null;
    if (head && head.parentNode) head.parentNode.removeChild(head);
    return (copy.textContent || "").split(/\r?\n/).map(words).filter(Boolean);
  }

  function buildText(block) {
    var release = block.getAttribute("data-release") || "";
    var date = block.getAttribute("data-release-date") || "";
    var items = block.querySelectorAll("li");
    var lines = ["Релиз " + release + (date ? " (" + date + ")" : ""), "Спецификаций: " + items.length, ""];
    Array.prototype.forEach.call(items, function (item, index) {
      var link = item.querySelector("a[data-status]");
      var id = link ? link.getAttribute("data-id") : "";
      lines.push((index + 1) + ". " + words(link ? link.textContent : "") + (id ? " [" + id + "]" : ""));
      describe(item).forEach(function (line) { lines.push("   " + line); });
      lines.push("");
    });
    return lines.join(EOL);
  }

  function download(name, text) {
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

  document.addEventListener("click", function (e) {
    var button = e.target.closest ? e.target.closest("a[data-release-download]") : null;
    if (!button) return;
    e.preventDefault();
    e.stopPropagation();
    var block = button.closest("details.release-block");
    if (!block) return;
    var release = block.getAttribute("data-release") || "";
    download("release-" + release.replace(/[^0-9A-Za-z._-]+/g, "_") + ".txt", buildText(block));
  }, true);
})();
