# Личный кабинет {#profile}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

??? warning "Внимание"

    На странице отображается содержимое файла `docs/specifications/profile/index.md`. Файл `index.md` формируется автоматически скриптом `scripts/generate_docs.py` при каждом внесении изменений в ветку `main`. Не редактируйте файл `index.md` вручную: правки будут перезаписаны.

<div class="status-tiles" markdown>

[:lucide-file: <span data-stat="backlog">1</span>](#){ .status-tile data-filter="backlog" title="зафиксированное сырое требование или идея" aria-label="бэклог: зафиксированное сырое требование или идея" }
[:lucide-file-pen-line: <span data-stat="analysis">0</span>](#){ .status-tile data-filter="analysis" title="детализация и согласование требования" aria-label="анализ: детализация и согласование требования" }
[:lucide-file-check: <span data-stat="ready">0</span>](#){ .status-tile data-filter="ready" title="утверждённое требование, готовое к реализации" aria-label="готово к разработке: утверждённое требование, готовое к реализации" }
[:lucide-file-braces: <span data-stat="development">1</span>](#){ .status-tile data-filter="development" title="требование в работе у команды разработки и тестирования" aria-label="разработка: требование в работе у команды разработки и тестирования" }
[:lucide-file-text: <span data-stat="released">2</span>](#){ .status-tile data-filter="released" title="код, связанный с требованием, успешно развёрнут на проде" aria-label="реализовано: код, связанный с требованием, успешно развёрнут на проде" }

</div>

<<<<<<< HEAD
<div class="feature-filter" markdown>
=======
!!! info status-cols "Всего спецификаций: 4"

    - :lucide-file: бэклог: <span data-stat="backlog">1</span>
    - :lucide-file-pen-line: анализ: <span data-stat="analysis">0</span>
    - :lucide-file-check: готово к разработке: <span data-stat="ready">0</span>
    - :lucide-file-braces: разработка: <span data-stat="development">1</span>
    - :lucide-file-text: реализовано: <span data-stat="released">2</span>

## Отбор функциональностей модуля {#feature-selection}

Отбор (фильтрация) функциональностей модуля как по текущему статусу функциональности, так и по названию субмодуля, функциональности. При одновременном использовании отбора по статусу и названию отображается то, что подходит под оба условия. При этом автоматически обновляются итоги в разделе статистики функциональностей.

[:lucide-file: бэклог](#){ .md-button data-filter="backlog" }
[:lucide-file-pen-line: анализ](#){ .md-button data-filter="analysis" }
[:lucide-file-check: готово к разработке](#){ .md-button data-filter="ready" }
[:lucide-file-braces: разработка](#){ .md-button data-filter="development" }
[:lucide-file-text: реализовано](#){ .md-button data-filter="released" }
[Сбросить](#){ .md-button data-filter-reset="" }
>>>>>>> 246a4da50b1259642c7b29a410f7e3bdf7f83dfc

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Спецификации {#specs}

<<<<<<< HEAD
<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Авторизация*: <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file-braces: [Двухфакторная аутентификация (2FA)](auth-2fa.md#article-overview){data-preview data-status="development"}
- :lucide-file-text: [Вход по номеру телефона и SMS](auth-sms.md#article-overview){data-preview data-status="released"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span">*Профиль пользователя*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></summary>

- :lucide-file-text: [Редактирование персональных данных](edit-data.md#article-overview){data-preview data-status="released"}
- :lucide-file: [Привязка профилей социальных сетей](oauth.md#article-overview){data-preview data-status="backlog"}

</details>
=======
- *Авторизация*: <span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
    - :lucide-file-braces: [Двухфакторная аутентификация (2FA)](auth-2fa.md#article-overview){data-preview data-status="development"}
    - :lucide-file-text: [Вход по номеру телефона и SMS](auth-sms.md#article-overview){data-preview data-status="released"}
- *Профиль пользователя*: <span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span>
    - :lucide-file-text: [Редактирование персональных данных](edit-data.md#article-overview){data-preview data-status="released"}
    - :lucide-file: [Привязка профилей социальных сетей](oauth.md#article-overview){data-preview data-status="backlog"}
>>>>>>> 246a4da50b1259642c7b29a410f7e3bdf7f83dfc
