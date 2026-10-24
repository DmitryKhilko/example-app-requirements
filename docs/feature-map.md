# Карта фичей продукта

> Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку `main`. Не редактируйте его вручную: правки будут перезаписаны.

!!! info "Обозначения"

    - :lucide-inbox: бэклог
    - :lucide-file-pen-line: проработка
    - :lucide-clipboard-check: готова к разработке
    - :lucide-code-xml: в разработке
    - :lucide-rocket: реализована
    - :lucide-archive: архив

!!! info "Всего спецификаций: 18"

    - :lucide-inbox: бэклог: 3
    - :lucide-file-pen-line: проработка: 2
    - :lucide-clipboard-check: готова к разработке: 1
    - :lucide-code-xml: в разработке: 3
    - :lucide-rocket: реализована: 6
    - :lucide-archive: архив: 3

## Активные фичи

- **Каталог товаров**
    - *Карточка товара*
        - :lucide-inbox: [Блок похожих товаров (рекомендации)](specifications/catalog/product-recommendations.md#article-overview){data-preview}
        - :lucide-rocket: [Галерея изображений с зумом](specifications/catalog/product-gallery.md#article-overview){data-preview}
    - *Поиск и фильтрация*
        - :lucide-file-pen-line: [Ещё одна новая фича](specifications/catalog/new-feature-copy.md#article-overview){data-preview}
        - :lucide-file-pen-line: [Новая фича](specifications/catalog/new-feature.md#article-overview){data-preview}
        - :lucide-rocket: [Полнотекстовый поиск по названию](specifications/catalog/search-text.md#article-overview){data-preview}
        - :lucide-code-xml: [Фильтр по диапазону цен с ползунком](specifications/catalog/filter-price-slider.md#article-overview){data-preview}
        - :lucide-rocket: [Фильтрация по категориям и тегам](specifications/catalog/filter-categories.md#article-overview){data-preview}
- **Личный кабинет**
    - *Авторизация*
        - :lucide-rocket: [Вход по номеру телефона и SMS](specifications/profile/auth-sms.md#article-overview){data-preview}
        - :lucide-code-xml: [Двухфакторная аутентификация (2FA)](specifications/profile/auth-2fa.md#article-overview){data-preview}
    - *Профиль пользователя*
        - :lucide-inbox: [Привязка профилей социальных сетей](specifications/profile/oauth.md#article-overview){data-preview}
        - :lucide-rocket: [Редактирование персональных данных](specifications/profile/edit-data.md#article-overview){data-preview}
- **Управление заказами**
    - *История заказов*
        - :lucide-clipboard-check: [Отмена заказа клиентом](specifications/orders/order-cancel.md#article-overview){data-preview}
    - *Оформление заказа*
        - :lucide-code-xml: [Выбор адреса на интерактивной карте](specifications/orders/checkout-map.md#article-overview){data-preview}
        - :lucide-rocket: [Оплата через СБП / QR-код](specifications/orders/payment-sbp.md#article-overview){data-preview}
        - :lucide-inbox: [Покупка в рассрочку](specifications/orders/credit-pay.md#article-overview){data-preview}

## Архив фичей

> Спецификации из папки `docs/archive/` или со статусом `archived`.

- **Каталог товаров**
    - *Поиск и фильтрация*
        - :lucide-archive: [Старый текстовый поиск (устарел)](archive/specifications/catalog/search-old.md#article-overview){data-preview}
- **Личный кабинет**
    - *Профиль пользователя*
        - :lucide-archive: [Дисконтные карты старого образца](archive/specifications/profile/legacy-cards.md#article-overview){data-preview}
- **Управление заказами**
    - *История заказов*
        - :lucide-archive: [Выписка заказов в виде бумажного чека](archive/specifications/orders/print-receipt.md#article-overview){data-preview}
