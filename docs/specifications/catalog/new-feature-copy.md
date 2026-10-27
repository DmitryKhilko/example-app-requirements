---
module: "Каталог товаров"
submodule: "Поиск и фильтрация"
feature_name: "Ещё одна новая фича"
status: "ready"
doc_version: "0.02"
owner: "Дмитрий Хилько"
relations:
  related:
    - feature: new-feature
      note: "Копия-шаблон фичи"
---

# Ещё одна новая фича {#new-feature-copy}

## Описание {#article-overview}

Пользователь ...

<!-- relations:start — раздел формируется скриптом scripts/build_feature_map.py по полю `relations` метаданных, не редактируйте его вручную -->

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
