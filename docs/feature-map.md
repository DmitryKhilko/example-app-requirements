# Перечень функциональностей продукта {#feature-map}

## Описание {#article-overview}

Перечень функциональностей — иерархическое оглавление спецификаций продукта: **модуль → субмодуль → функциональность**. Название каждой функциональности — ссылка на раздел «Описание» её спецификации (при наведении курсора показывается предпросмотр). Перед названием стоит значок статуса, а в заголовках модулей и субмодулей указано число функциональностей по статусам. Актуальные и архивные функциональности выведены отдельными разделами; нужные статусы можно выбрать кнопками фильтра в разделе «Статистика».

> Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку `main`. Не редактируйте его вручную: правки будут перезаписаны.

!!! info "Статусы требований"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде
    - :lucide-file-archive: архив: отклонённое или устаревшее требование

## Статистика {#statistics}

!!! info status-cols "Всего спецификаций: 18"

    - :lucide-file: бэклог: 3
    - :lucide-file-pen-line: анализ: 2
    - :lucide-file-check: готово к разработке: 1
    - :lucide-file-braces: разработка: 3
    - :lucide-file-text: реализовано: 6
    - :lucide-file-archive: архив: 3

**Фильтр по статусу:**

[:lucide-file: бэклог](#){ .md-button data-filter="backlog" }
[:lucide-file-pen-line: анализ](#){ .md-button data-filter="analysis" }
[:lucide-file-check: готово к разработке](#){ .md-button data-filter="ready" }
[:lucide-file-braces: разработка](#){ .md-button data-filter="development" }
[:lucide-file-text: реализовано](#){ .md-button data-filter="released" }
[:lucide-file-archive: архив](#){ .md-button data-filter="archived" }
[Сбросить](#){ .md-button data-filter-reset="" }

## Актуальные функциональности {#active-features}

- **Каталог товаров**: :lucide-file:: 1, :lucide-file-pen-line:: 2, :lucide-file-braces:: 1, :lucide-file-text:: 3
    - *Карточка товара*: :lucide-file:: 1, :lucide-file-text:: 1
        - :lucide-file: [Блок похожих товаров (рекомендации)](specifications/catalog/product-recommendations.md#article-overview){data-preview data-status="backlog"}
        - :lucide-file-text: [Галерея изображений с зумом](specifications/catalog/product-gallery.md#article-overview){data-preview data-status="released"}
    - *Поиск и фильтрация*: :lucide-file-pen-line:: 2, :lucide-file-braces:: 1, :lucide-file-text:: 2
        - :lucide-file-pen-line: [Ещё одна новая фича](specifications/catalog/new-feature-copy.md#article-overview){data-preview data-status="analysis"}
        - :lucide-file-pen-line: [Новая фича](specifications/catalog/new-feature.md#article-overview){data-preview data-status="analysis"}
        - :lucide-file-text: [Полнотекстовый поиск по названию](specifications/catalog/search-text.md#article-overview){data-preview data-status="released"}
        - :lucide-file-braces: [Фильтр по диапазону цен с ползунком](specifications/catalog/filter-price-slider.md#article-overview){data-preview data-status="development"}
        - :lucide-file-text: [Фильтрация по категориям и тегам](specifications/catalog/filter-categories.md#article-overview){data-preview data-status="released"}
- **Личный кабинет**: :lucide-file:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 2
    - *Авторизация*: :lucide-file-braces:: 1, :lucide-file-text:: 1
        - :lucide-file-text: [Вход по номеру телефона и SMS](specifications/profile/auth-sms.md#article-overview){data-preview data-status="released"}
        - :lucide-file-braces: [Двухфакторная аутентификация (2FA)](specifications/profile/auth-2fa.md#article-overview){data-preview data-status="development"}
    - *Профиль пользователя*: :lucide-file:: 1, :lucide-file-text:: 1
        - :lucide-file: [Привязка профилей социальных сетей](specifications/profile/oauth.md#article-overview){data-preview data-status="backlog"}
        - :lucide-file-text: [Редактирование персональных данных](specifications/profile/edit-data.md#article-overview){data-preview data-status="released"}
- **Управление заказами**: :lucide-file:: 1, :lucide-file-check:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 1
    - *История заказов*: :lucide-file-check:: 1
        - :lucide-file-check: [Отмена заказа клиентом](specifications/orders/order-cancel.md#article-overview){data-preview data-status="ready"}
    - *Оформление заказа*: :lucide-file:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 1
        - :lucide-file-braces: [Выбор адреса на интерактивной карте](specifications/orders/checkout-map.md#article-overview){data-preview data-status="development"}
        - :lucide-file-text: [Оплата через СБП / QR-код](specifications/orders/payment-sbp.md#article-overview){data-preview data-status="released"}
        - :lucide-file: [Покупка в рассрочку](specifications/orders/credit-pay.md#article-overview){data-preview data-status="backlog"}

## Архивные функциональности {#archived-features}

> Спецификации из папки `docs/archive/` или со статусом `archived`.

- **Каталог товаров**: :lucide-file-archive:: 1
    - *Поиск и фильтрация*: :lucide-file-archive:: 1
        - :lucide-file-archive: [Старый текстовый поиск (устарел)](archive/specifications/catalog/search-old.md#article-overview){data-preview data-status="archived"}
- **Личный кабинет**: :lucide-file-archive:: 1
    - *Профиль пользователя*: :lucide-file-archive:: 1
        - :lucide-file-archive: [Дисконтные карты старого образца](archive/specifications/profile/legacy-cards.md#article-overview){data-preview data-status="archived"}
- **Управление заказами**: :lucide-file-archive:: 1
    - *История заказов*: :lucide-file-archive:: 1
        - :lucide-file-archive: [Выписка заказов в виде бумажного чека](archive/specifications/orders/print-receipt.md#article-overview){data-preview data-status="archived"}
