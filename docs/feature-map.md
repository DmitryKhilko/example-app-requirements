---
hide:
  - toc
---

# Карта функциональностей продукта {#feature-map}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

??? info "Статусы спецификаций"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде
    - :lucide-file-archive: архив: отклонённое или устаревшее требование

<div class="status-total" markdown="span">:lucide-files: <span class="status-name">Всего спецификаций</span> <span data-stat-total>18</span></div>

<div class="status-tiles" data-n="6" markdown>

[<span class="status-top">:lucide-file: <span data-stat="backlog">3</span></span><span class="status-name">бэклог</span>](#){ .status-tile data-filter="backlog" aria-label="бэклог" }
[<span class="status-top">:lucide-file-pen-line: <span data-stat="analysis">1</span></span><span class="status-name">анализ</span>](#){ .status-tile data-filter="analysis" aria-label="анализ" }
[<span class="status-top">:lucide-file-check: <span data-stat="ready">2</span></span><span class="status-name">готово к разработке</span>](#){ .status-tile data-filter="ready" aria-label="готово к разработке" }
[<span class="status-top">:lucide-file-braces: <span data-stat="development">3</span></span><span class="status-name">разработка</span>](#){ .status-tile data-filter="development" aria-label="разработка" }
[<span class="status-top">:lucide-file-text: <span data-stat="released">6</span></span><span class="status-name">реализовано</span>](#){ .status-tile data-filter="released" aria-label="реализовано" }
[<span class="status-top">:lucide-file-archive: <span data-stat="archived">3</span></span><span class="status-name">архив</span>](#){ .status-tile data-filter="archived" aria-label="архив" }

</div>

<div class="feature-filter" markdown>

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию модуля или субмодуля или функциональности" aria-label="Отбор по названию модуля или субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p></div>

## Действующие спецификации {#active-features}

<details class="feature-block feature-module" markdown="block">
<summary markdown="span"><span class="feature-title">**Каталог товаров**</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="analysis">:lucide-file-pen-line:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>3</span></span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Карточка товара*</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file-text: [Галерея изображений с зумом](specifications/catalog/product-gallery.md#article-overview){data-preview data-status="released"}
- :lucide-file: [Блок похожих товаров (рекомендации)](specifications/catalog/product-recommendations.md#article-overview){data-preview data-status="backlog"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Поиск и фильтрация*</span><span class="feature-counts"><span data-count-item="analysis">:lucide-file-pen-line:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>2</span></span></span></summary>

- :lucide-file-text: [Фильтрация по категориям и тегам](specifications/catalog/filter-categories.md#article-overview){data-preview data-status="released"}
- :lucide-file-braces: [Фильтр по диапазону цен с ползунком](specifications/catalog/filter-price-slider.md#article-overview){data-preview data-status="development"}
- :lucide-file-text: [Полнотекстовый поиск по названию](specifications/catalog/search-text.md#article-overview){data-preview data-status="released"}
- :lucide-file-pen-line: [Новая фича](specifications/catalog/new-feature.md#article-overview){data-preview data-status="analysis"}
- :lucide-file-check: [Ещё одна новая фича](specifications/catalog/new-feature-copy.md#article-overview){data-preview data-status="ready"}

</details>


</details>

<details class="feature-block feature-module" markdown="block">
<summary markdown="span"><span class="feature-title">**Управление заказами**</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*История заказов*</span><span class="feature-counts"><span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span></span></summary>

- :lucide-file-check: [Отмена заказа клиентом](specifications/orders/order-cancel.md#article-overview){data-preview data-status="ready"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Оформление заказа*</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file: [Покупка в рассрочку](specifications/orders/credit-pay.md#article-overview){data-preview data-status="backlog"}
- :lucide-file-text: [Оплата через СБП / QR-код](specifications/orders/payment-sbp.md#article-overview){data-preview data-status="released"}
- :lucide-file-braces: [Выбор адреса на интерактивной карте](specifications/orders/checkout-map.md#article-overview){data-preview data-status="development"}

</details>


</details>

<details class="feature-block feature-module" markdown="block">
<summary markdown="span"><span class="feature-title">**Личный кабинет**</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>2</span></span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Авторизация*</span><span class="feature-counts"><span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file-braces: [Двухфакторная аутентификация (2FA)](specifications/profile/auth-2fa.md#article-overview){data-preview data-status="development"}
- :lucide-file-text: [Вход по номеру телефона и SMS](specifications/profile/auth-sms.md#article-overview){data-preview data-status="released"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Профиль пользователя*</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file-text: [Редактирование персональных данных](specifications/profile/edit-data.md#article-overview){data-preview data-status="released"}
- :lucide-file: [Привязка профилей социальных сетей](specifications/profile/oauth.md#article-overview){data-preview data-status="backlog"}

</details>


</details>

## Архив спецификаций {#archived-features}

<details class="feature-block feature-module" markdown="block">
<summary markdown="span"><span class="feature-title">**Каталог товаров**</span><span class="feature-counts"><span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Поиск и фильтрация*</span><span class="feature-counts"><span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span></span></summary>

- :lucide-file-archive: [Старый текстовый поиск (устарел)](archive/specifications/catalog/search-old.md#article-overview){data-preview data-status="archived"}

</details>


</details>

<details class="feature-block feature-module" markdown="block">
<summary markdown="span"><span class="feature-title">**Управление заказами**</span><span class="feature-counts"><span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*История заказов*</span><span class="feature-counts"><span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span></span></summary>

- :lucide-file-archive: [Выписка заказов в виде бумажного чека](archive/specifications/orders/print-receipt.md#article-overview){data-preview data-status="archived"}

</details>


</details>

<details class="feature-block feature-module" markdown="block">
<summary markdown="span"><span class="feature-title">**Личный кабинет**</span><span class="feature-counts"><span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Профиль пользователя*</span><span class="feature-counts"><span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span></span></summary>

- :lucide-file-archive: [Дисконтные карты старого образца](archive/specifications/profile/legacy-cards.md#article-overview){data-preview data-status="archived"}

</details>


</details>
