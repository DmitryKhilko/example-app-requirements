/* ==========================================================================
   spec-passport.js — «паспорт» спецификации под заголовком первого уровня

   Шаблон theme-custom/spec.html выводит блок <dl class="spec-passport"> (данные из Front Matter) перед содержимым страницы,
   то есть над заголовком первого уровня. Скрипт переносит блок сразу под заголовок: вверху страницы стоит название
   функциональности, под ним — информация из метаданных. Без JavaScript блок остаётся над заголовком (всё читается).

   Запускается событием темы document$ — после загрузки страницы и после каждой мгновенной навигации (navigation.instant);
   повторный вызов безопасен.
   ========================================================================== */
(function () {
  "use strict";

  function place() {
    var root = document.querySelector(".md-content__inner");
    if (!root) return;
    var passport = root.querySelector(":scope > dl.spec-passport");
    var title = root.querySelector(":scope > h1");
    if (!passport || !title || title.nextElementSibling === passport) return;
    title.insertAdjacentElement("afterend", passport);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(place);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", place);
  } else {
    place();
  }
})();
