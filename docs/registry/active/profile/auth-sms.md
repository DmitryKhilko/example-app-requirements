---
id: "SHOP-ACC-AUTH-002"
module: "Личный кабинет"
submodule: "Авторизация"
feature_name: "Вход по номеру телефона и SMS"
status: "released"
icon: lucide/file-text
doc_version: "0.01.04"
datetime_version: "03.11.2026 21:56"
order: 20
owner: "Dmitry Khilko"
task_id: "1"
release_id: "1.3.0"
release_date: "20.10.2026"
template: "spec.html"
relations:
  depends_on: []
---

# Вход по номеру телефона и SMS {#auth-sms}

??? note no-icon "<h2 id="change-history" style="display: inline;">Журнал изменений</h2>"

    - [Версия 0.01.04 (03.11.2026 21:56)](https://github.com/DmitryKhilko/example-app-requirements/commit/946722cd65c3f1b10f33bbd5502c07f99e42a396){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.01.03 (03.11.2026 21:51)](https://github.com/DmitryKhilko/example-app-requirements/commit/6d5152879e740681cfa1d38d1fb47f3e55422280){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.01.02 (03.11.2026 21:47)](https://github.com/DmitryKhilko/example-app-requirements/commit/16ca5959584d722232cf45bb4545f42a24b08e87){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.01.01 (03.11.2026 21:44)](https://github.com/DmitryKhilko/example-app-requirements/commit/1979332543f39afa8d422ce4a7a1ba5c48a50c0d){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.01.00 (03.11.2026 21:40)](https://github.com/DmitryKhilko/example-app-requirements/commit/4854f9e877a6a4f5d1ce452e5a24495a43c56049){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.18 (01.11.2026 20:01)](https://github.com/DmitryKhilko/example-app-requirements/commit/75f3ebdc1c6dca93c1dd99f62bd2e8c61a01e329){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.17 (01.11.2026 00:28)](https://github.com/DmitryKhilko/example-app-requirements/commit/0051b0603735add2d8accbce728da892dbae579d){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.16 (31.10.2026 04:00)](https://github.com/DmitryKhilko/example-app-requirements/commit/7d5df6bfefd1fe59eb97b755a4bdf6d43080dbf8){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.15 (30.10.2026 22:51)](https://github.com/DmitryKhilko/example-app-requirements/commit/87d5d9dc7b4cb601a64eb95f3878882246cb4101){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.14 (30.10.2026 21:58)](https://github.com/DmitryKhilko/example-app-requirements/commit/6bb44418e10d07e49d58a62f2260a3bd5cb55669){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.13 (30.10.2026 11:22)](https://github.com/DmitryKhilko/example-app-requirements/commit/694c2f6fb21f1f454979f1fb76709d1ef0b3a550){target="_blank" rel="noopener"}. Ответственный: Khilko Dmitry
    - [Версия 0.00.12 (29.10.2026 18:37)](https://github.com/DmitryKhilko/example-app-requirements/commit/ddc79dfa59baa67a57809a122542dd07e7ab984a){target="_blank" rel="noopener"}. Ответственный: Khilko Dmitry
    - [Версия 0.00.11 (29.10.2026 11:26)](https://github.com/DmitryKhilko/example-app-requirements/commit/cfe4d7b95be70c543cd94879cb04881476177cef){target="_blank" rel="noopener"}. Ответственный: Khilko Dmitry
    - [Версия 0.00.10 (28.10.2026 23:10)](https://github.com/DmitryKhilko/example-app-requirements/commit/cf30c68a1ee461acc89b2ed7ea500787754ccb20){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.09 (28.10.2026 17:51)](https://github.com/DmitryKhilko/example-app-requirements/commit/246a4da50b1259642c7b29a410f7e3bdf7f83dfc){target="_blank" rel="noopener"}. Ответственный: Khilko Dmitry
    - [Версия 0.00.08 (28.10.2026 17:42)](https://github.com/DmitryKhilko/example-app-requirements/commit/5a2dd672e698a54f6e2dbc118c0b72eea8e05d35){target="_blank" rel="noopener"}. Ответственный: Khilko Dmitry
    - [Версия 0.00.07 (28.10.2026 14:37)](https://github.com/DmitryKhilko/example-app-requirements/commit/4bbd4a605df6cae4baa5920512c61dbf350921b6){target="_blank" rel="noopener"}. Ответственный: Khilko Dmitry
    - [Версия 0.00.06 (27.10.2026 23:42)](https://github.com/DmitryKhilko/example-app-requirements/commit/663868fc7b7896a5cba00bc32218a76f0332c92a){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.05 (27.10.2026 22:52)](https://github.com/DmitryKhilko/example-app-requirements/commit/5f50ce3550ed662b10aee0b27f23d6a2ff2a30b5){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.04 (27.10.2026 22:27)](https://github.com/DmitryKhilko/example-app-requirements/commit/35f1dbbb63dbe4f347c0bc4e5093d6ada996a519){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.03 (27.10.2026 21:21)](https://github.com/DmitryKhilko/example-app-requirements/commit/3cf1d6105f42d465a0b58d0c9a7e3873168a3169){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.02 (24.10.2026 23:00)](https://github.com/DmitryKhilko/example-app-requirements/commit/13a86cc861427e7cfc81cdc1b3eeccd7ba62d2d2){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko
    - [Версия 0.00.01 (24.10.2026 22:01)](https://github.com/DmitryKhilko/example-app-requirements/commit/8e7d7a96059eee2eb5f175a615118d6f9d813dce){target="_blank" rel="noopener"}. Ответственный: Dmitry Khilko

## Описание {#article-overview}

Вход без пароля по одноразовому коду из SMS.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Вход по номеру телефона и SMS</b><br/><i>[реализовано]</i>"]
    n1["Двухфакторная аутентификация (2FA)<br/><i>[разработка]</i>"]
    n2["Привязка профилей социальных сетей<br/><i>[бэклог]</i>"]
    n3["Редактирование персональных данных<br/><i>[реализовано]</i>"]
    n1 -.->|"расширяет"| n0
    n0 -.-|"связана с"| n2
    n0 -.-|"связана с"| n3

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../auth-2fa/"
    click n2 "../oauth/"
    click n3 "../edit-data/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Расширяется функциональностью | [Двухфакторная аутентификация (2FA)](auth-2fa.md#article-overview){data-preview} | разработка | Добавляет второй шаг к входу по номеру телефона |
| Связана с | [Привязка профилей социальных сетей](oauth.md#article-overview){data-preview} | бэклог | Альтернативный способ входа |
| Связана с | [Редактирование персональных данных](edit-data.md#article-overview){data-preview} | реализовано | Смена номера телефона влияет на вход по SMS |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Пользователь вводит номер телефона.
2. Система отправляет SMS с шестизначным кодом.
3. Пользователь вводит код, система создаёт сессию.

## Критерии приёмки {#acceptance-criteria}

- Код действует 5 минут.
- После 3 неверных попыток ввод блокируется на 15 минут.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.
