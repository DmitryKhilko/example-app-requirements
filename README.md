# example-app-requirements
Пример организации требований с использованием подхода "Documentation as Code"

Адрес сайта: https://dmitrykhilko.github.io/example-app-requirements/

## Как устроена карта фичей

Карта фичей (`docs/feature-map.md`) — иерархическое оглавление «Модуль → Субмодуль → Фича» со ссылками на
спецификации. **Вручную её не редактируют**: её формирует скрипт `scripts/build_feature_map.py` по метаданным
(YAML Front Matter) в начале каждой спецификации.

```
Слияние в main ──► feature-map: python scripts/build_feature_map.py ──► коммит docs/feature-map.md (если изменился)
                                                                        │
                                                                        ▼
                                                  deploy: zensical build ──► GitHub Pages
```

Workflow: `.github/workflows/deploy.yml`. Карта обновляется только при слиянии в `main`; в рабочих ветках
`docs/feature-map.md` не трогают, поэтому конфликтов слияния в нём не возникает.

### Метаданные спецификации

Шаблон — `templates/feature-spec-template.md`.

| Поле           | Обязательное | Описание                                                          |
|----------------|--------------|-------------------------------------------------------------------|
| `module`       | да           | Модуль (верхний уровень карты)                                    |
| `submodule`    | нет          | Субмодуль; по умолчанию `Общее`                                   |
| `feature_name` | да           | Название фичи — текст ссылки в карте                              |
| `status`       | рекомендуется| `draft` 📋, `review` ⏳, `published` 🟢, `archived` 📦. Допустимы синонимы: `бэклог`, `в разработке`, `готово`, `архив` |

Каждая ссылка карты ведёт на раздел «Описание» спецификации и показывает его в окне предпросмотра при наведении
(`{ data-preview }`).

**Якоря заголовков — обязательное условие.** У каждого заголовка спецификации должен быть явный якорь в конце строки,
как в `glossary.md`:

```markdown
# Отмена заказа клиентом {#order-cancel}
## Описание {#article-overview}
## Основной сценарий {#main-scenario}
## Критерии приёмки {#acceptance-criteria}
```

Идентификатор — латиница, цифры, `-`, `_`, первая буква; в пределах файла уникален. Заголовок «Описание» всегда
получает `{#article-overview}`. Нарушение любого правила — ошибка: сборка завершается с кодом 1 (в Actions — аннотация
с файлом и строкой), карта и сайт не обновляются.

Статьи без полей `module`, `submodule`, `feature_name` (например, глоссарий) в карту не попадают.
Если `module` или `feature_name` не заполнены, сборка тоже падает с указанием файла.
Неизвестный `status` приводит к предупреждению, фича показывается как `draft`.

### Архив

Чтобы архивировать спецификацию, переместите файл в `docs/archive/` с сохранением подпапки
(например, `docs/specifications/orders/order-cancel.md` → `docs/archive/specifications/orders/order-cancel.md`) — метаданные менять не нужно.
В карте фича перейдёт в раздел «Архив фичей» со значком 📦, ссылка останется рабочей.
Тот же результат даёт `status: "archived"` у файла вне папки архива.

### Локальный запуск

```bash
pip install -r scripts/requirements.txt
python scripts/build_feature_map.py          # пересобрать карту
python scripts/build_feature_map.py --check  # проверить, что карта актуальна (код возврата 1, если нет)
```

### Настройки репозитория

* Settings → Pages → Source: **GitHub Actions**.
* Settings → Actions → General → Workflow permissions: **Read and write permissions** (нужно для коммита карты).
* Если ветка `main` защищена правилом «только через Pull Request», разрешите обход правила для GitHub Actions
  либо замените `GITHUB_TOKEN` в шаге коммита на токен с правом записи.
