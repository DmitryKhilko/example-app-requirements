---
hide:
  - toc
---

# Управление заказами {#orders}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

<div class="status-total" markdown="span">:lucide-files: <span class="status-name">Всего спецификаций</span> <span data-stat-total>4</span></div>

<div class="status-tiles" data-n="5" markdown>

[<span class="status-top">:lucide-file: <span data-stat="backlog">1</span></span><span class="status-name">бэклог</span>](#){ .status-tile data-filter="backlog" title="зафиксированное сырое требование или идея" aria-label="бэклог: зафиксированное сырое требование или идея" }
[<span class="status-top">:lucide-file-pen-line: <span data-stat="analysis">0</span></span><span class="status-name">анализ</span>](#){ .status-tile data-filter="analysis" title="детализация и согласование требования" aria-label="анализ: детализация и согласование требования" }
[<span class="status-top">:lucide-file-check: <span data-stat="ready">1</span></span><span class="status-name">готово к разработке</span>](#){ .status-tile data-filter="ready" title="утверждённое требование, готовое к реализации" aria-label="готово к разработке: утверждённое требование, готовое к реализации" }
[<span class="status-top">:lucide-file-braces: <span data-stat="development">1</span></span><span class="status-name">разработка</span>](#){ .status-tile data-filter="development" title="требование в работе у команды разработки и тестирования" aria-label="разработка: требование в работе у команды разработки и тестирования" }
[<span class="status-top">:lucide-file-text: <span data-stat="released">1</span></span><span class="status-name">реализовано</span>](#){ .status-tile data-filter="released" title="код, связанный с требованием, успешно развёрнут на проде" aria-label="реализовано: код, связанный с требованием, успешно развёрнут на проде" }

</div>

<div class="feature-filter" markdown>

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p></div>

## Спецификации {#specs}

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*История заказов*</span><span class="feature-counts"><span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span></span></summary>

- :lucide-file-check: [Отмена заказа клиентом](order-cancel.md#article-overview){data-preview data-status="ready"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Оформление заказа*</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file: [Покупка в рассрочку](credit-pay.md#article-overview){data-preview data-status="backlog"}
- :lucide-file-text: [Оплата через СБП / QR-код](payment-sbp.md#article-overview){data-preview data-status="released"}
- :lucide-file-braces: [Выбор адреса на интерактивной карте](checkout-map.md#article-overview){data-preview data-status="development"}

</details>
