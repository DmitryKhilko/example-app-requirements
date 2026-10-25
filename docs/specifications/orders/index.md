# Управление заказами {#orders}

## Описание {#article-overview}

Спецификации раздела «Управление заказами»: всего 4.

!!! warning "Внимание"

    Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку `main`. Не редактируйте его вручную: правки будут перезаписаны.

## Спецификации {#specs}

- *История заказов*: :lucide-file-check:: 1
    - :lucide-file-check: [Отмена заказа клиентом](order-cancel.md#article-overview){data-preview data-status="ready"}
- *Оформление заказа*: :lucide-file:: 1, :lucide-file-braces:: 1, :lucide-file-text:: 1
    - :lucide-file-braces: [Выбор адреса на интерактивной карте](checkout-map.md#article-overview){data-preview data-status="development"}
    - :lucide-file-text: [Оплата через СБП / QR-код](payment-sbp.md#article-overview){data-preview data-status="released"}
    - :lucide-file: [Покупка в рассрочку](credit-pay.md#article-overview){data-preview data-status="backlog"}
