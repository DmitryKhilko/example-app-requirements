# Управление заказами {#orders}

## Описание {#article-overview}

Спецификации модуля «Управление заказами».

!!! warning "Внимание"

    Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку `main`. Не редактируйте файл вручную: правки будут перезаписаны.

!!! info "Статусы требований"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде

## Статистика функциональностей модуля в разрезе статусов {#statistics}

!!! info status-cols "Всего спецификаций: 4"

    - :lucide-file: бэклог: 1
    - :lucide-file-pen-line: анализ: 0
    - :lucide-file-check: готово к разработке: 1
    - :lucide-file-braces: разработка: 1
    - :lucide-file-text: реализовано: 1

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

- *История заказов*: :lucide-file-check:: 1
    - :lucide-file-check: [Отмена заказа клиентом](order-cancel.md#article-overview){data-preview data-status="ready"}
- *Оформление заказа*: :lucide-file:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 1
    - :lucide-file-braces: [Выбор адреса на интерактивной карте](checkout-map.md#article-overview){data-preview data-status="development"}
    - :lucide-file-text: [Оплата через СБП / QR-код](payment-sbp.md#article-overview){data-preview data-status="released"}
    - :lucide-file: [Покупка в рассрочку](credit-pay.md#article-overview){data-preview data-status="backlog"}
