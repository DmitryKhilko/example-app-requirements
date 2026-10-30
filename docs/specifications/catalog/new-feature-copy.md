---
id: "SHOP-CAT-SF-006"
module: "Каталог товаров"
submodule: "Поиск и фильтрация"
feature_name: "Ещё одна новая фича"
status: "ready"
icon: lucide/file-check
order: 70
doc_version: "0.02"
owner: "Дмитрий Хилько"
template: "spec.html"
relations:
  depends_on: []
  related:
    - feature: new-feature
      note: "Копия-шаблон фичи"
---

# Ещё одна новая фича {#new-feature-copy}

## Описание {#article-overview}

Пользователь ...

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Ещё одна новая фича</b><br/><i>[готово к разработке]</i>"]
    n1["Новая фича<br/><i>[анализ]</i>"]
    n0 -.-|"связана с"| n1

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../new-feature/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Связана с | [Новая фича](new-feature.md#article-overview){data-preview} | анализ | Копия-шаблон фичи |

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
