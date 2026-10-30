---
id: "SHOP-ACC-USER-003"
module: "Личный кабинет"
submodule: "Профиль пользователя"
feature_name: "Привязка профилей социальных сетей"
status: "backlog"
icon: lucide/file
doc_version: "0.01"
order: 40
owner: "Дмитрий Хилько"
template: "spec.html"
relations:
  depends_on: []
  related:
    - feature: auth-sms
      note: "Альтернативный способ входа"
---

# Привязка профилей социальных сетей {#oauth}

## Описание {#article-overview}

Привязка внешних аккаунтов для быстрого входа.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Привязка профилей социальных сетей</b><br/><i>[бэклог]</i>"]
    n1["Вход по номеру телефона и SMS<br/><i>[реализовано]</i>"]
    n0 -.-|"связана с"| n1

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../auth-sms/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Связана с | [Вход по номеру телефона и SMS](auth-sms.md#article-overview){data-preview} | реализовано | Альтернативный способ входа |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Пользователь выбирает социальную сеть в настройках профиля.
2. Система выполняет авторизацию у провайдера и привязывает аккаунт.

## Критерии приёмки {#acceptance-criteria}

- К одному профилю можно привязать не более одного аккаунта каждой сети.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.

## Ссылка на задачу {#task}

[Задача 01](https://github.bmf/khilko/app_requirements/issues/1){:target="_blank"}
