# Спецификации {#specifications}

## Описание {#article-overview}

Действующие спецификации функциональностей продукта по модулям и субмодулям.

!!! warning "Внимание"

    На странице отображается содержимое файла `docs/specifications/index.md`. Файл `index.md` формируется автоматически скриптом `scripts/build_feature_map.py` при каждом внесении изменений в ветку `main`. Не редактируйте файл `index.md` вручную: правки будут перезаписаны.

!!! info "Статусы требований"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде

## Статистика функциональностей раздела в разрезе статусов {#statistics}

!!! info status-cols "Всего спецификаций: 15"

    - :lucide-file: бэклог: 3
    - :lucide-file-pen-line: анализ: 1
    - :lucide-file-check: готово к разработке: 2
    - :lucide-file-braces: разработка: 3
    - :lucide-file-text: реализовано: 6

## Отбор функциональностей раздела {#feature-selection}

Отбор (фильтрация) функциональностей раздела как по текущему статусу функциональности, так и по названию модуля, субмодуля, функциональности. При одновременном использовании отбора по статусу и названию отображается то, что подходит под оба условия.

[:lucide-file: бэклог](#){ .md-button data-filter="backlog" }
[:lucide-file-pen-line: анализ](#){ .md-button data-filter="analysis" }
[:lucide-file-check: готово к разработке](#){ .md-button data-filter="ready" }
[:lucide-file-braces: разработка](#){ .md-button data-filter="development" }
[:lucide-file-text: реализовано](#){ .md-button data-filter="released" }
[Сбросить](#){ .md-button data-filter-reset="" }

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию модуля или субмодуля или функциональности" aria-label="Отбор по названию модуля или субмодуля или функциональности">

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Спецификации раздела {#specs}

- **Каталог товаров**: :lucide-file:: 1, :lucide-file-pen-line:: 1, :lucide-file-check:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 3
    - *Карточка товара*: :lucide-file:: 1, :lucide-file-text:: 1
        - :lucide-file: [Блок похожих товаров (рекомендации)](catalog/product-recommendations.md#article-overview){data-preview data-status="backlog"}
        - :lucide-file-text: [Галерея изображений с зумом](catalog/product-gallery.md#article-overview){data-preview data-status="released"}
    - *Поиск и фильтрация*: :lucide-file-pen-line:: 1, :lucide-file-check:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 2
        - :lucide-file-check: [Ещё одна новая фича](catalog/new-feature-copy.md#article-overview){data-preview data-status="ready"}
        - :lucide-file-pen-line: [Новая фича](catalog/new-feature.md#article-overview){data-preview data-status="analysis"}
        - :lucide-file-text: [Полнотекстовый поиск по названию](catalog/search-text.md#article-overview){data-preview data-status="released"}
        - :lucide-file-braces: [Фильтр по диапазону цен с ползунком](catalog/filter-price-slider.md#article-overview){data-preview data-status="development"}
        - :lucide-file-text: [Фильтрация по категориям и тегам](catalog/filter-categories.md#article-overview){data-preview data-status="released"}
- **Личный кабинет**: :lucide-file:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 2
    - *Авторизация*: :lucide-file-braces:: 1, :lucide-file-text:: 1
        - :lucide-file-text: [Вход по номеру телефона и SMS](profile/auth-sms.md#article-overview){data-preview data-status="released"}
        - :lucide-file-braces: [Двухфакторная аутентификация (2FA)](profile/auth-2fa.md#article-overview){data-preview data-status="development"}
    - *Профиль пользователя*: :lucide-file:: 1, :lucide-file-text:: 1
        - :lucide-file: [Привязка профилей социальных сетей](profile/oauth.md#article-overview){data-preview data-status="backlog"}
        - :lucide-file-text: [Редактирование персональных данных](profile/edit-data.md#article-overview){data-preview data-status="released"}
- **Управление заказами**: :lucide-file:: 1, :lucide-file-check:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 1
    - *История заказов*: :lucide-file-check:: 1
        - :lucide-file-check: [Отмена заказа клиентом](orders/order-cancel.md#article-overview){data-preview data-status="ready"}
    - *Оформление заказа*: :lucide-file:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 1
        - :lucide-file-braces: [Выбор адреса на интерактивной карте](orders/checkout-map.md#article-overview){data-preview data-status="development"}
        - :lucide-file-text: [Оплата через СБП / QR-код](orders/payment-sbp.md#article-overview){data-preview data-status="released"}
        - :lucide-file: [Покупка в рассрочку](orders/credit-pay.md#article-overview){data-preview data-status="backlog"}
