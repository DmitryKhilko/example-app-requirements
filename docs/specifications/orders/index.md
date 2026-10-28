---
hide:
  - toc
---

# Управление заказами {#orders}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

<div class="status-tiles" markdown>

<span class="status-total">:lucide-files: <span class="status-name">Всего</span> <span data-stat-total>4</span></span>
[:lucide-file: <span class="status-name">бэклог</span> <span data-stat="backlog">1</span>](#){ .status-tile data-filter="backlog" title="зафиксированное сырое требование или идея" aria-label="бэклог: зафиксированное сырое требование или идея" }
[:lucide-file-pen-line: <span class="status-name">анализ</span> <span data-stat="analysis">0</span>](#){ .status-tile data-filter="analysis" title="детализация и согласование требования" aria-label="анализ: детализация и согласование требования" }
[:lucide-file-check: <span class="status-name">готово к разработке</span> <span data-stat="ready">1</span>](#){ .status-tile data-filter="ready" title="утверждённое требование, готовое к реализации" aria-label="готово к разработке: утверждённое требование, готовое к реализации" }
[:lucide-file-braces: <span class="status-name">разработка</span> <span data-stat="development">1</span>](#){ .status-tile data-filter="development" title="требование в работе у команды разработки и тестирования" aria-label="разработка: требование в работе у команды разработки и тестирования" }
[:lucide-file-text: <span class="status-name">реализовано</span> <span data-stat="released">1</span>](#){ .status-tile data-filter="released" title="код, связанный с требованием, успешно развёрнут на проде" aria-label="реализовано: код, связанный с требованием, успешно развёрнут на проде" }

</div>

<div class="feature-filter" markdown>

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Спецификации {#specs}

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*История заказов*: <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span></summary>

- :lucide-file-check: [Отмена заказа клиентом](order-cancel.md#article-overview){data-preview data-status="ready"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Оформление заказа*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file: [Покупка в рассрочку](credit-pay.md#article-overview){data-preview data-status="backlog"}
- :lucide-file-text: [Оплата через СБП / QR-код](payment-sbp.md#article-overview){data-preview data-status="released"}
- :lucide-file-braces: [Выбор адреса на интерактивной карте](checkout-map.md#article-overview){data-preview data-status="development"}

</details>
