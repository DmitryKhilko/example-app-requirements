# Личный кабинет {#profile}

## Описание {#article-overview}

Спецификации модуля «Личный кабинет».

!!! warning "Внимание"

    Файл формируется автоматически скриптом `scripts/build_feature_map.py` при слиянии изменений в ветку `main`. Не редактируйте файл вручную: правки будут перезаписаны.

!!! info "Статусы требований"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде

## Статистика функциональностей модуля в разрезе статусов {#statistics}

!!! info status-cols "Всего спецификаций: 4"

    - :lucide-file: бэклог: 1
    - :lucide-file-pen-line: анализ: 0
    - :lucide-file-check: готово к разработке: 0
    - :lucide-file-braces: разработка: 1
    - :lucide-file-text: реализовано: 2

## Отбор функциональностей модуля {#feature-selection}

Отбор (фильтрация) функциональностей модуля как по текущему статусу функциональности, так и по названию субмодуля, функциональности. При одновременном использовании отбора по статусу и названию отображается то, что подходит под оба условия.

[:lucide-file: бэклог](#){ .md-button data-filter="backlog" }
[:lucide-file-pen-line: анализ](#){ .md-button data-filter="analysis" }
[:lucide-file-check: готово к разработке](#){ .md-button data-filter="ready" }
[:lucide-file-braces: разработка](#){ .md-button data-filter="development" }
[:lucide-file-text: реализовано](#){ .md-button data-filter="released" }
[Сбросить](#){ .md-button data-filter-reset="" }

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

## Спецификации модуля {#specs}

- *Авторизация*: :lucide-file-braces:: 1, :lucide-file-text:: 1
    - :lucide-file-text: [Вход по номеру телефона и SMS](auth-sms.md#article-overview){data-preview data-status="released"}
    - :lucide-file-braces: [Двухфакторная аутентификация (2FA)](auth-2fa.md#article-overview){data-preview data-status="development"}
- *Профиль пользователя*: :lucide-file:: 1, :lucide-file-text:: 1
    - :lucide-file: [Привязка профилей социальных сетей](oauth.md#article-overview){data-preview data-status="backlog"}
    - :lucide-file-text: [Редактирование персональных данных](edit-data.md#article-overview){data-preview data-status="released"}
