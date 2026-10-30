---
id: "SHOP-CAT-SF-005"
module: "Каталог товаров"
submodule: "Поиск и фильтрация"
feature_name: "Новая фича"
status: "analysis"
icon: lucide/file-pen-line
order: 60
doc_version: "0.01"
owner: "Дмитрий Хилько"
relations:
  depends_on: []
---

# Новая фича {#new-feature}

## Описание {#article-overview}

Пользователь ...

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Новая фича</b><br/><i>[анализ]</i>"]
    n1["Ещё одна новая фича<br/><i>[готово к разработке]</i>"]
    n0 -.-|"связана с"| n1

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../new-feature-copy/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Связана с | [Ещё одна новая фича](new-feature-copy.md#article-overview){data-preview} | готово к разработке | Копия-шаблон фичи |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. ...
2. ...
3. ...

## Критерии приёмки {#acceptance-criteria}

- ...
- ...

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.

## Ссылка на задачу {#task}

[Задача 01](https://github.bmf/khilko/app_requirements/issues/1){:target="_blank"}
