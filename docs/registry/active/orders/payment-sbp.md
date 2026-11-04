---
id: "SHOP-ORD-CHCK-003"
module: "Управление заказами"
submodule: "Оформление заказа"
feature_name: "Оплата через СБП / QR-код"
status: "released"
icon: lucide/file-text
order: 20
doc_version: "0.00.18"
datetime_version: "01.11.2026 20:01"
owner: "Dmitry Khilko"
task_id: "1"
release_id: "1.2.1"
release_date: "15.09.2026"
template: "spec.html"
relations:
  depends_on: []
---

# Оплата через СБП / QR-код {#payment-sbp}

??? note no-icon "<h2 id="change-history" style="display: inline;">Журнал изменений</h2>"

    - [Версия 0.00.18](https://github.com/DmitryKhilko/example-app-requirements/commit/75f3ebdc1c6dca93c1dd99f62bd2e8c61a01e329). Ответственный: Dmitry Khilko
    - [Версия 0.00.17](https://github.com/DmitryKhilko/example-app-requirements/commit/0051b0603735add2d8accbce728da892dbae579d). Ответственный: Dmitry Khilko
    - [Версия 0.00.16](https://github.com/DmitryKhilko/example-app-requirements/commit/7d5df6bfefd1fe59eb97b755a4bdf6d43080dbf8). Ответственный: Dmitry Khilko
    - [Версия 0.00.15](https://github.com/DmitryKhilko/example-app-requirements/commit/87d5d9dc7b4cb601a64eb95f3878882246cb4101). Ответственный: Dmitry Khilko
    - [Версия 0.00.14](https://github.com/DmitryKhilko/example-app-requirements/commit/6bb44418e10d07e49d58a62f2260a3bd5cb55669). Ответственный: Dmitry Khilko
    - [Версия 0.00.13](https://github.com/DmitryKhilko/example-app-requirements/commit/694c2f6fb21f1f454979f1fb76709d1ef0b3a550). Ответственный: Khilko Dmitry
    - [Версия 0.00.12](https://github.com/DmitryKhilko/example-app-requirements/commit/ddc79dfa59baa67a57809a122542dd07e7ab984a). Ответственный: Khilko Dmitry
    - [Версия 0.00.11](https://github.com/DmitryKhilko/example-app-requirements/commit/cfe4d7b95be70c543cd94879cb04881476177cef). Ответственный: Khilko Dmitry
    - [Версия 0.00.10](https://github.com/DmitryKhilko/example-app-requirements/commit/cf30c68a1ee461acc89b2ed7ea500787754ccb20). Ответственный: Dmitry Khilko
    - [Версия 0.00.09](https://github.com/DmitryKhilko/example-app-requirements/commit/246a4da50b1259642c7b29a410f7e3bdf7f83dfc). Ответственный: Khilko Dmitry
    - [Версия 0.00.08](https://github.com/DmitryKhilko/example-app-requirements/commit/5a2dd672e698a54f6e2dbc118c0b72eea8e05d35). Ответственный: Khilko Dmitry
    - [Версия 0.00.07](https://github.com/DmitryKhilko/example-app-requirements/commit/4bbd4a605df6cae4baa5920512c61dbf350921b6). Ответственный: Khilko Dmitry
    - [Версия 0.00.06](https://github.com/DmitryKhilko/example-app-requirements/commit/663868fc7b7896a5cba00bc32218a76f0332c92a). Ответственный: Dmitry Khilko
    - [Версия 0.00.05](https://github.com/DmitryKhilko/example-app-requirements/commit/5f50ce3550ed662b10aee0b27f23d6a2ff2a30b5). Ответственный: Dmitry Khilko
    - [Версия 0.00.04](https://github.com/DmitryKhilko/example-app-requirements/commit/35f1dbbb63dbe4f347c0bc4e5093d6ada996a519). Ответственный: Dmitry Khilko
    - [Версия 0.00.03](https://github.com/DmitryKhilko/example-app-requirements/commit/3cf1d6105f42d465a0b58d0c9a7e3873168a3169). Ответственный: Dmitry Khilko
    - [Версия 0.00.02](https://github.com/DmitryKhilko/example-app-requirements/commit/13a86cc861427e7cfc81cdc1b3eeccd7ba62d2d2). Ответственный: Dmitry Khilko
    - [Версия 0.00.01](https://github.com/DmitryKhilko/example-app-requirements/commit/8e7d7a96059eee2eb5f175a615118d6f9d813dce). Ответственный: Dmitry Khilko

## Описание {#article-overview}

Оплата заказа через Систему быстрых платежей.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Оплата через СБП / QR-код</b><br/><i>[реализовано]</i>"]
    n1["Отмена заказа клиентом<br/><i>[готово к разработке]</i>"]
    n2["Выбор адреса на интерактивной карте<br/><i>[разработка]</i>"]
    n3["Покупка в рассрочку<br/><i>[бэклог]</i>"]
    n1 -->|"зависит от"| n0
    n0 -.-|"связана с"| n2
    n0 -.-|"связана с"| n3

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../order-cancel/"
    click n2 "../checkout-map/"
    click n3 "../credit-pay/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Используется в | [Отмена заказа клиентом](order-cancel.md#article-overview){data-preview} | готово к разработке | Возврат средств при отмене выполняется тем же способом, которым оплачен заказ |
| Связана с | [Выбор адреса на интерактивной карте](checkout-map.md#article-overview){data-preview} | разработка | Соседние шаги оформления заказа: доставка и оплата |
| Связана с | [Покупка в рассрочку](credit-pay.md#article-overview){data-preview} | бэклог | Альтернативный способ оплаты при оформлении заказа |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Клиент выбирает способ оплаты «СБП».
2. Система показывает QR-код и ссылку для мобильного приложения банка.
3. Система получает подтверждение платежа и завершает оформление.

## Критерии приёмки {#acceptance-criteria}

- Срок действия QR-кода — 10 минут.
- Статус оплаты обновляется без перезагрузки страницы.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.
