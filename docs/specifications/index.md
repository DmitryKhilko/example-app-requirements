---
hide:
  - toc
---

# Спецификации {#specifications}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

<div class="status-tiles" style="--n: 5" markdown>

<span class="status-total">:lucide-files: <span class="status-name">Всего</span> <span data-stat-total>15</span></span>
[<span class="status-top">:lucide-file: <span data-stat="backlog">3</span></span><span class="status-name">бэклог</span>](#){ .status-tile data-filter="backlog" title="зафиксированное сырое требование или идея" aria-label="бэклог: зафиксированное сырое требование или идея" }
[<span class="status-top">:lucide-file-pen-line: <span data-stat="analysis">1</span></span><span class="status-name">анализ</span>](#){ .status-tile data-filter="analysis" title="детализация и согласование требования" aria-label="анализ: детализация и согласование требования" }
[<span class="status-top">:lucide-file-check: <span data-stat="ready">2</span></span><span class="status-name">готово к разработке</span>](#){ .status-tile data-filter="ready" title="утверждённое требование, готовое к реализации" aria-label="готово к разработке: утверждённое требование, готовое к реализации" }
[<span class="status-top">:lucide-file-braces: <span data-stat="development">3</span></span><span class="status-name">разработка</span>](#){ .status-tile data-filter="development" title="требование в работе у команды разработки и тестирования" aria-label="разработка: требование в работе у команды разработки и тестирования" }
[<span class="status-top">:lucide-file-text: <span data-stat="released">6</span></span><span class="status-name">реализовано</span>](#){ .status-tile data-filter="released" title="код, связанный с требованием, успешно развёрнут на проде" aria-label="реализовано: код, связанный с требованием, успешно развёрнут на проде" }

</div>

<div class="feature-filter" markdown>

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию модуля или субмодуля или функциональности" aria-label="Отбор по названию модуля или субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Спецификации {#specs}

<details class="feature-block feature-module" markdown="block">
<summary markdown="span">**Каталог товаров**: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="analysis">:lucide-file-pen-line:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>3</span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Карточка товара*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file-text: [Галерея изображений с зумом](catalog/product-gallery.md#article-overview){data-preview data-status="released"}
- :lucide-file: [Блок похожих товаров (рекомендации)](catalog/product-recommendations.md#article-overview){data-preview data-status="backlog"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Поиск и фильтрация*: <span data-count-item="analysis">:lucide-file-pen-line:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>2</span></span></summary>

- :lucide-file-text: [Фильтрация по категориям и тегам](catalog/filter-categories.md#article-overview){data-preview data-status="released"}
- :lucide-file-braces: [Фильтр по диапазону цен с ползунком](catalog/filter-price-slider.md#article-overview){data-preview data-status="development"}
- :lucide-file-text: [Полнотекстовый поиск по названию](catalog/search-text.md#article-overview){data-preview data-status="released"}
- :lucide-file-pen-line: [Новая фича](catalog/new-feature.md#article-overview){data-preview data-status="analysis"}
- :lucide-file-check: [Ещё одна новая фича](catalog/new-feature-copy.md#article-overview){data-preview data-status="ready"}

</details>


</details>

<details class="feature-block feature-module" markdown="block">
<summary markdown="span">**Управление заказами**: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*История заказов*: <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span></summary>

- :lucide-file-check: [Отмена заказа клиентом](orders/order-cancel.md#article-overview){data-preview data-status="ready"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Оформление заказа*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file: [Покупка в рассрочку](orders/credit-pay.md#article-overview){data-preview data-status="backlog"}
- :lucide-file-text: [Оплата через СБП / QR-код](orders/payment-sbp.md#article-overview){data-preview data-status="released"}
- :lucide-file-braces: [Выбор адреса на интерактивной карте](orders/checkout-map.md#article-overview){data-preview data-status="development"}

</details>


</details>

<details class="feature-block feature-module" markdown="block">
<summary markdown="span">**Личный кабинет**: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>2</span></span></summary>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Авторизация*: <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file-braces: [Двухфакторная аутентификация (2FA)](profile/auth-2fa.md#article-overview){data-preview data-status="development"}
- :lucide-file-text: [Вход по номеру телефона и SMS](profile/auth-sms.md#article-overview){data-preview data-status="released"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Профиль пользователя*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file-text: [Редактирование персональных данных](profile/edit-data.md#article-overview){data-preview data-status="released"}
- :lucide-file: [Привязка профилей социальных сетей](profile/oauth.md#article-overview){data-preview data-status="backlog"}

</details>


</details>
