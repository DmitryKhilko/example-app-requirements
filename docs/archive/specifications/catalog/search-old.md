---
id: "SHOP-CAT-SF-001"
module: "Каталог товаров"
submodule: "Поиск и фильтрация"
feature_name: "Старый текстовый поиск (устарел)"
status: "archived"
icon: lucide/file-archive
doc_version: "0.01"
order: 10
owner: "Дмитрий Хилько"
task_id: "1"
relise_id: ""
relise_date: ""
template: "spec.html"
relations:
  depends_on: []
---

# Старый текстовый поиск (устарел) {#search-old}

## Описание {#article-overview}

Поиск по точному совпадению названия. Заменён полнотекстовым поиском.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Старый текстовый поиск (устарел)</b><br/><i>[архив]</i>"]
    n1["Полнотекстовый поиск по названию<br/><i>[реализовано]</i>"]
    n1 ==>|"заменяет"| n0

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current
    class n0 archived

    click n1 "../../../../specifications/catalog/search-text/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Заменена функциональностью | [Полнотекстовый поиск по названию](../../../specifications/catalog/search-text.md#article-overview){data-preview} | реализовано | Поиск по точному совпадению названия выведен из эксплуатации |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Пользователь вводит полное название товара.
2. Система возвращает товары с точным совпадением.

## Критерии приёмки {#acceptance-criteria}

- Заменено фичей ["Полнотекстовый поиск по названию"](../../../specifications/catalog/search-text.md#article-overview){data-preview}.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.
