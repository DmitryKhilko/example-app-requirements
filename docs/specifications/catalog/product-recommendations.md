---
module: "Каталог товаров"
submodule: "Карточка товара"
feature_name: "Блок похожих товаров (рекомендации)"
status: "backlog"
icon: lucide/file
doc_version: "0.01"
order: 40
owner: "Дмитрий Хилько"
relations:
  depends_on:
    - feature: filter-categories
      note: "Похожие товары подбираются по категориям и тегам"
  related:
    - feature: product-gallery
      note: "Соседние блоки карточки товара"
---

# Блок похожих товаров (рекомендации) {#product-recommendations}

## Описание {#article-overview}

Показ товаров, похожих на просматриваемый.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Блок похожих товаров (рекомендации)</b><br/><i>[бэклог]</i>"]
    n1["Фильтрация по категориям и тегам<br/><i>[реализовано]</i>"]
    n2["Галерея изображений с зумом<br/><i>[реализовано]</i>"]
    n0 -->|"зависит от"| n1
    n0 -.-|"связана с"| n2

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../filter-categories/"
    click n2 "../product-gallery/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Зависит от | [Фильтрация по категориям и тегам](filter-categories.md#article-overview){data-preview} | реализовано | Похожие товары подбираются по категориям и тегам |
| Связана с | [Галерея изображений с зумом](product-gallery.md#article-overview){data-preview} | реализовано | Соседние блоки карточки товара |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Пользователь открывает карточку товара.
2. Система подбирает до 8 похожих товаров по категории и тегам.

## Критерии приёмки {#acceptance-criteria}

- Блок не показывается, если подходящих товаров меньше 3.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.

## Ссылка на задачу {#task}

[Задача 01](https://github.bmf/khilko/app_requirements/issues/1){:target="_blank"}
