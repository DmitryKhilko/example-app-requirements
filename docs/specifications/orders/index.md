# Управление заказами {#orders}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Описание {#article-overview}

Спецификации модуля «Управление заказами».

!!! warning "Внимание"

    На странице отображается содержимое файла `docs/specifications/orders/index.md`. Файл `index.md` формируется автоматически скриптом `scripts/generate_docs.py` при каждом внесении изменений в ветку `main`. Не редактируйте файл `index.md` вручную: правки будут перезаписаны.

!!! info "Статусы требований"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде

## Статистика функциональностей модуля в разрезе статусов {#statistics}

!!! info status-cols "Всего спецификаций: 4"

    - :lucide-file: бэклог: <span data-stat="backlog">1</span>
    - :lucide-file-pen-line: анализ: <span data-stat="analysis">0</span>
    - :lucide-file-check: готово к разработке: <span data-stat="ready">1</span>
    - :lucide-file-braces: разработка: <span data-stat="development">1</span>
    - :lucide-file-text: реализовано: <span data-stat="released">1</span>

## Отбор функциональностей модуля {#feature-selection}

Отбор (фильтрация) функциональностей модуля как по текущему статусу функциональности, так и по названию субмодуля, функциональности. При одновременном использовании отбора по статусу и названию отображается то, что подходит под оба условия.

[:lucide-file: бэклог](#){ .md-button data-filter="backlog" }
[:lucide-file-pen-line: анализ](#){ .md-button data-filter="analysis" }
[:lucide-file-check: готово к разработке](#){ .md-button data-filter="ready" }
[:lucide-file-braces: разработка](#){ .md-button data-filter="development" }
[:lucide-file-text: реализовано](#){ .md-button data-filter="released" }
[Сбросить](#){ .md-button data-filter-reset="" }

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Спецификации модуля {#specs}

- *История заказов*: <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span>
    - :lucide-file-check: [Отмена заказа клиентом](order-cancel.md#article-overview){data-preview data-status="ready"}
- *Оформление заказа*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
    - :lucide-file: [Покупка в рассрочку](credit-pay.md#article-overview){data-preview data-status="backlog"}
    - :lucide-file-text: [Оплата через СБП / QR-код](payment-sbp.md#article-overview){data-preview data-status="released"}
    - :lucide-file-braces: [Выбор адреса на интерактивной карте](checkout-map.md#article-overview){data-preview data-status="development"}
