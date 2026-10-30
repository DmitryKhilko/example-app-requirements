---
id: "SHOP-ORD-CHCK-001"
module: "Управление заказами"
submodule: "Оформление заказа"
feature_name: "Выбор адреса на интерактивной карте"
status: "development"
icon: lucide/file-braces
doc_version: "0.01"
order: 40
owner: "Дмитрий Хилько"
task_id: "1"
relise_id: ""
template: "spec.html"
relations:
  depends_on: []
  related:
    - feature: payment-sbp
      note: "Соседние шаги оформления заказа: доставка и оплата"
---

# Выбор адреса на интерактивной карте {#checkout-map}

## Описание {#article-overview}

Выбор адреса доставки указанием точки на карте.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Выбор адреса на интерактивной карте</b><br/><i>[разработка]</i>"]
    n1["Оплата через СБП / QR-код<br/><i>[реализовано]</i>"]
    n0 -.-|"связана с"| n1

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../payment-sbp/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Связана с | [Оплата через СБП / QR-код](payment-sbp.md#article-overview){data-preview} | реализовано | Соседние шаги оформления заказа: доставка и оплата |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Клиент открывает карту на шаге доставки.
2. Клиент указывает точку, система определяет адрес.
3. Клиент подтверждает адрес.

## Критерии приёмки {#acceptance-criteria}

- Адрес можно скорректировать вручную.
- Недоступные для доставки зоны выделяются на карте.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.
