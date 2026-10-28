---
hide:
  - toc
---

# Личный кабинет {#profile}

<!-- generated: файл формируется автоматически, не редактируйте его вручную -->

## Статистика {#statistics}

<div class="status-tiles" style="--n: 5" markdown>

<span class="status-total">:lucide-files: <span class="status-name">Всего</span> <span data-stat-total>4</span></span>
[<span class="status-top">:lucide-file: <span data-stat="backlog">1</span></span><span class="status-name">бэклог</span>](#){ .status-tile data-filter="backlog" title="зафиксированное сырое требование или идея" aria-label="бэклог: зафиксированное сырое требование или идея" }
[<span class="status-top">:lucide-file-pen-line: <span data-stat="analysis">0</span></span><span class="status-name">анализ</span>](#){ .status-tile data-filter="analysis" title="детализация и согласование требования" aria-label="анализ: детализация и согласование требования" }
[<span class="status-top">:lucide-file-check: <span data-stat="ready">0</span></span><span class="status-name">готово к разработке</span>](#){ .status-tile data-filter="ready" title="утверждённое требование, готовое к реализации" aria-label="готово к разработке: утверждённое требование, готовое к реализации" }
[<span class="status-top">:lucide-file-braces: <span data-stat="development">1</span></span><span class="status-name">разработка</span>](#){ .status-tile data-filter="development" title="требование в работе у команды разработки и тестирования" aria-label="разработка: требование в работе у команды разработки и тестирования" }
[<span class="status-top">:lucide-file-text: <span data-stat="released">2</span></span><span class="status-name">реализовано</span>](#){ .status-tile data-filter="released" title="код, связанный с требованием, успешно развёрнут на проде" aria-label="реализовано: код, связанный с требованием, успешно развёрнут на проде" }

</div>

<div class="feature-filter" markdown>

<input type="search" class="feature-search" data-feature-search="" autocomplete="off" placeholder="Отбор по названию субмодуля или функциональности" aria-label="Отбор по названию субмодуля или функциональности">

[Сбросить](#){ .md-button data-filter-reset="" }

</div>

<div class="feature-empty" data-feature-empty="" hidden><p>Нет данных, соответствующих условиям отбора</p><p><a href="#" class="md-button" data-filter-reset="">Сбросить</a></p></div>

## Спецификации {#specs}

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
