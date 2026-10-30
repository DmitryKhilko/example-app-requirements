---
id: "SHOP-CAT-CARD-001"
module: "Каталог товаров"
submodule: "Карточка товара"
feature_name: "Галерея изображений с зумом"
status: "released"
icon: lucide/file-text
order: 30
doc_version: "0.01"
owner: "Дмитрий Хилько"
relations:
  depends_on: []
---

# Галерея изображений с зумом {#product-gallery}

## Описание {#article-overview}

Просмотр изображений товара с увеличением.

<!-- relations:start — раздел формируется автоматически по полю `relations` метаданных, не редактируйте его вручную -->

## Взаимосвязи {#relations}

Схема и таблица показывают прямые связи этой функциональности с другими спецификациями.

```mermaid
%%{init: {"themeVariables": {"fontSize": "12.8px"}}}%%
flowchart LR
    n0["<b>Галерея изображений с зумом</b><br/><i>[реализовано]</i>"]
    n1["Блок похожих товаров (рекомендации)<br/><i>[бэклог]</i>"]
    n0 -.-|"связана с"| n1

    classDef current stroke-width:3px
    classDef archived stroke-dasharray:5 4
    class n0 current

    click n1 "../product-recommendations/"
```

| Связь | Функциональность | Статус | Комментарий |
|---|---|---|---|
| Связана с | [Блок похожих товаров (рекомендации)](product-recommendations.md#article-overview){data-preview} | бэклог | Соседние блоки карточки товара |

<!-- relations:end -->

## Основной сценарий {#main-scenario}

1. Пользователь выбирает миниатюру.
2. Система показывает изображение в основной области.
3. Пользователь наводит курсор или щипком увеличивает изображение.

## Критерии приёмки {#acceptance-criteria}

- Поддерживается не менее 10 изображений на товар.
- Зум работает на мобильных устройствах.

## Критерии релиза {#release-criteria}

- **Наступление даты:** Не ранее 1 декабря 2026 года.

## Ссылка на задачу {#task}

[Задача 01](https://github.bmf/khilko/app_requirements/issues/1){:target="_blank"}
