---
hide:
  - toc
---

# Личный кабинет {#profile}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

??? info "Статусы спецификаций"

    - :lucide-file: бэклог: зафиксированное сырое требование или идея
    - :lucide-file-pen-line: анализ: детализация и согласование требования
    - :lucide-file-check: готово к разработке: утверждённое требование, готовое к реализации
    - :lucide-file-braces: разработка: требование в работе у команды разработки и тестирования
    - :lucide-file-text: реализовано: код, связанный с требованием, успешно развёрнут на проде

<div class="status-total" markdown="span">:lucide-files: <span class="status-name">Всего спецификаций</span> <span data-stat-total>4</span></div>

<div class="status-tiles" data-n="5" markdown>

[<span class="status-top">:lucide-file: <span data-stat="backlog">1</span></span><span class="status-name">бэклог</span>](#){ .status-tile data-filter="backlog" aria-label="бэклог" }
[<span class="status-top">:lucide-file-pen-line: <span data-stat="analysis">0</span></span><span class="status-name">анализ</span>](#){ .status-tile data-filter="analysis" aria-label="анализ" }
[<span class="status-top">:lucide-file-check: <span data-stat="ready">0</span></span><span class="status-name">готово к разработке</span>](#){ .status-tile data-filter="ready" aria-label="готово к разработке" }
[<span class="status-top">:lucide-file-braces: <span data-stat="development">1</span></span><span class="status-name">разработка</span>](#){ .status-tile data-filter="development" aria-label="разработка" }
[<span class="status-top">:lucide-file-text: <span data-stat="released">2</span></span><span class="status-name">реализовано</span>](#){ .status-tile data-filter="released" aria-label="реализовано" }

</div>

<div class="feature-filter" markdown>

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p></div>

## Спецификации {#specs}

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Авторизация*</span><span class="feature-counts"><span data-count-item="development">:lucide-file-braces:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file-braces: [Двухфакторная аутентификация (2FA)](auth-2fa.md#article-overview){data-preview data-status="development"}
- :lucide-file-text: [Вход по номеру телефона и SMS](auth-sms.md#article-overview){data-preview data-status="released"}

</details>

<details class="feature-block feature-submodule" markdown="block">
<summary markdown="span"><span class="feature-title">*Профиль пользователя*</span><span class="feature-counts"><span data-count-item="backlog">:lucide-file:: <span data-count>1</span></span> <span data-count-item="released">:lucide-file-text:: <span data-count>1</span></span></span></summary>

- :lucide-file-text: [Редактирование персональных данных](edit-data.md#article-overview){data-preview data-status="released"}
- :lucide-file: [Привязка профилей социальных сетей](oauth.md#article-overview){data-preview data-status="backlog"}

</details>
