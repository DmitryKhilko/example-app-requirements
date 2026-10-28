---
module: "Личный кабинет"
submodule: "Профиль пользователя"
feature_name: "Редактирование персональных данных"
status: "released"
icon: lucide/file-text
doc_version: "0.01"
order: 30
owner: "Дмитрий Хилько"
relations:
  related:
    - feature: auth-sms
      note: "Смена номера телефона влияет на вход по SMS"
---

# Редактирование персональных данных {#edit-data}

## Описание {#article-overview}

Изменение имени, e-mail и контактных данных пользователя.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Редактирование персональных данных</b><br/><i>[реализовано]</i>"]
    n1["Покупка в рассрочку<br/><i>[бэклог]</i>"]
    n2["Вход по номеру телефона и SMS<br/><i>[реализовано]</i>"]
    n1 -->|"зависит от"| n0
    n0 -.-|"связана с"| n2

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../../orders/credit-pay/"
    click n2 "../auth-sms/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Используется в | [Покупка в рассрочку](../orders/credit-pay.md#article-overview){data-preview} | бэклог | Персональные данные клиента передаются в заявке банку-партнёру |
| Связана с | [Вход по номеру телефона и SMS](auth-sms.md#article-overview){data-preview} | реализовано | Смена номера телефона влияет на вход по SMS |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Пользователь открывает раздел «Профиль».
2. Пользователь изменяет поля и сохраняет форму.

## Критерии приёмки {#acceptance-criteria}

- Смена e-mail требует подтверждения по ссылке из письма.

## Ссылка на задачу {#task}

[Задача 01](https://github.bmf/khilko/app_requirements/issues/1)
