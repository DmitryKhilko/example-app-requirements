# 🗺️ Карта фичей продукта

> Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку `main`. Не редактируйте его вручную: правки будут перезаписаны.

Всего спецификаций: **17** · 🟢 6 · ⏳ 4 · 📋 4 · 📦 3

Обозначения: 🟢 опубликовано · ⏳ на проверке · 📋 черновик · 📦 архив

## 🚀 Активные фичи

- **Каталог товаров**
    - *Карточка товара*
        - 📋 [Блок похожих товаров (рекомендации)](specifications/catalog/product-recommendations.md)
        - 🟢 [Галерея изображений с зумом](specifications/catalog/product-gallery.md)
    - *Поиск и фильтрация*
        - 📋 [Новая фича](specifications/catalog/new-feature.md)
        - 🟢 [Полнотекстовый поиск по названию](specifications/catalog/search-text.md)
        - ⏳ [Фильтр по диапазону цен с ползунком](specifications/catalog/filter-price-slider.md)
        - 🟢 [Фильтрация по категориям и тегам](specifications/catalog/filter-categories.md)
- **Личный кабинет**
    - *Авторизация*
        - 🟢 [Вход по номеру телефона и SMS](specifications/profile/auth-sms.md)
        - ⏳ [Двухфакторная аутентификация (2FA)](specifications/profile/auth-2fa.md)
    - *Профиль пользователя*
        - 📋 [Привязка профилей социальных сетей](specifications/profile/oauth.md)
        - 🟢 [Редактирование персональных данных](specifications/profile/edit-data.md)
- **Управление заказами**
    - *История заказов*
        - ⏳ [Отмена заказа клиентом](specifications/orders/order-cancel.md)
    - *Оформление заказа*
        - ⏳ [Выбор адреса на интерактивной карте](specifications/orders/checkout-map.md)
        - 🟢 [Оплата через СБП / QR-код](specifications/orders/payment-sbp.md)
        - 📋 [Покупка в рассрочку](specifications/orders/credit-pay.md)

## 📦 Архив фичей

> Спецификации из папки `docs/archive/` или со статусом `archived`.

- **Каталог товаров**
    - *Поиск и фильтрация*
        - 📦 [Старый текстовый поиск (устарел)](archive/specifications/catalog/search-old.md)
- **Личный кабинет**
    - *Профиль пользователя*
        - 📦 [Дисконтные карты старого образца](archive/specifications/profile/legacy-cards.md)
- **Управление заказами**
    - *История заказов*
        - 📦 [Выписка заказов в виде бумажного чека](archive/specifications/orders/print-receipt.md)
