# Карта функциональностей {#feature-map}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Описание {#article-overview}

Карта функциональностей - иерархическое оглавление спецификаций продукта: **модуль -> субмодуль -> функциональность**. Название каждой функциональности - ссылка на раздел «Описание» её спецификации (при наведении курсора показывается предпросмотр). Перед названием стоит значок статуса, а в заголовках модулей и субмодулей указано число функциональностей по статусам. Актуальные и архивные функциональности выведены отдельными разделами; нужные статусы можно выбрать кнопками фильтра в разделе «Отбор функциональностей продукта».

!!! warning "Внимание"

    На странице отображается содержимое файла `docs/feature-map.md`. Файл `feature-map.md` формируется автоматически скриптом `scripts/generate_docs.py` при каждом внесении изменений в ветку `main`. Не редактируйте файл `feature-map.md` вручную: правки будут перезаписаны.

!!! info "Статусы требований"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде
    - :lucide-file-archive: архив: отклонённое или устаревшее требование

## Статистика функциональностей продукта в разрезе статусов {#statistics}

!!! info status-cols "Всего спецификаций: 18"

    - :lucide-file: бэклог: <span data-stat="backlog">3</span>
    - :lucide-file-pen-line: анализ: <span data-stat="analysis">1</span>
    - :lucide-file-check: готово к разработке: <span data-stat="ready">2</span>
    - :lucide-file-braces: разработка: <span data-stat="development">3</span>
    - :lucide-file-text: реализовано: <span data-stat="released">6</span>
    - :lucide-file-archive: архив: <span data-stat="archived">3</span>

## Отбор функциональностей продукта {#feature-selection}

Отбор (фильтрация) функциональностей продукта как по текущему статусу функциональности, так и по названию модуля, субмодуля, функциональности. При одновременном использовании отбора по статусу и названию отображается то, что подходит под оба условия. При этом автоматически обновляются итоги в разделе статистики функциональностей.

[:lucide-file: бэклог](#){ .md-button data-filter="backlog" }
[:lucide-file-pen-line: анализ](#){ .md-button data-filter="analysis" }
[:lucide-file-check: готово к разработке](#){ .md-button data-filter="ready" }
[:lucide-file-braces: разработка](#){ .md-button data-filter="development" }
[:lucide-file-text: реализовано](#){ .md-button data-filter="released" }
[:lucide-file-archive: архив](#){ .md-button data-filter="archived" }
[Сбросить](#){ .md-button data-filter-reset="" }

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию модуля или субмодуля или функциональности" aria-label="Отбор по названию модуля или субмодуля или функциональности">

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Актуальные функциональности {#active-features}

- **Каталог товаров**: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="analysis">:lucide-file-pen-line:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>3</span></span>
    - *Карточка товара*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
        - :lucide-file-text: [Галерея изображений с зумом](specifications/catalog/product-gallery.md#article-overview){data-preview data-status="released"}
        - :lucide-file: [Блок похожих товаров (рекомендации)](specifications/catalog/product-recommendations.md#article-overview){data-preview data-status="backlog"}
    - *Поиск и фильтрация*: <span data-count-item="analysis">:lucide-file-pen-line:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>2</span></span>
        - :lucide-file-text: [Фильтрация по категориям и тегам](specifications/catalog/filter-categories.md#article-overview){data-preview data-status="released"}
        - :lucide-file-braces: [Фильтр по диапазону цен с ползунком](specifications/catalog/filter-price-slider.md#article-overview){data-preview data-status="development"}
        - :lucide-file-text: [Полнотекстовый поиск по названию](specifications/catalog/search-text.md#article-overview){data-preview data-status="released"}
        - :lucide-file-pen-line: [Новая фича](specifications/catalog/new-feature.md#article-overview){data-preview data-status="analysis"}
        - :lucide-file-check: [Ещё одна новая фича](specifications/catalog/new-feature-copy.md#article-overview){data-preview data-status="ready"}
- **Управление заказами**: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
    - *История заказов*: <span data-count-item="ready">:lucide-file-check:: <span data-count>1</span></span>
        - :lucide-file-check: [Отмена заказа клиентом](specifications/orders/order-cancel.md#article-overview){data-preview data-status="ready"}
    - *Оформление заказа*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
        - :lucide-file: [Покупка в рассрочку](specifications/orders/credit-pay.md#article-overview){data-preview data-status="backlog"}
        - :lucide-file-text: [Оплата через СБП / QR-код](specifications/orders/payment-sbp.md#article-overview){data-preview data-status="released"}
        - :lucide-file-braces: [Выбор адреса на интерактивной карте](specifications/orders/checkout-map.md#article-overview){data-preview data-status="development"}
- **Личный кабинет**: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>2</span></span>
    - *Авторизация*: <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
        - :lucide-file-braces: [Двухфакторная аутентификация (2FA)](specifications/profile/auth-2fa.md#article-overview){data-preview data-status="development"}
        - :lucide-file-text: [Вход по номеру телефона и SMS](specifications/profile/auth-sms.md#article-overview){data-preview data-status="released"}
    - *Профиль пользователя*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
        - :lucide-file-text: [Редактирование персональных данных](specifications/profile/edit-data.md#article-overview){data-preview data-status="released"}
        - :lucide-file: [Привязка профилей социальных сетей](specifications/profile/oauth.md#article-overview){data-preview data-status="backlog"}

## Архивные функциональности {#archived-features}

> Спецификации из папки `docs/archive/` или со статусом `archived`.

- **Каталог товаров**: <span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span>
    - *Поиск и фильтрация*: <span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span>
        - :lucide-file-archive: [Старый текстовый поиск (устарел)](archive/specifications/catalog/search-old.md#article-overview){data-preview data-status="archived"}
- **Управление заказами**: <span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span>
    - *История заказов*: <span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span>
        - :lucide-file-archive: [Выписка заказов в виде бумажного чека](archive/specifications/orders/print-receipt.md#article-overview){data-preview data-status="archived"}
- **Личный кабинет**: <span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span>
    - *Профиль пользователя*: <span data-count-item="archived">:lucide-file-archive:: <span data-count>1</span></span>
        - :lucide-file-archive: [Дисконтные карты старого образца](archive/specifications/profile/legacy-cards.md#article-overview){data-preview data-status="archived"}
