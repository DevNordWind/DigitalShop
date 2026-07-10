admin-positions-categories = <b>{ -category-emoji } Вибери категорію</b>
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Налаштування️
    .filters-btn = { -filter-emoji } Фільтри

admin-positions-category-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { category-status-plural } { -current }
        *[other] { category-status-plural }
    }

admins-position-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { position-status-plural } { -current }
        *[other] { position-status-plural }
    }

admin-positions = <b>{ -position-emoji } Позиції</b>
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Налаштування️
    .filters-btn = { -filter-emoji } Фільтри

admin-position = <b>{ -position-emoji } Редагування позиції</b>

    <b>📜 Основна інформація:</b>
    { admin-position-name }
    { admin-position-description }
    { $updated_at ->
        [None] { -current } Дата створення: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
        *[other] { -current } Дата створення: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Остання зміна: <i>{ DATETIME($updated_at, dateStyle: "medium", timeStyle: "medium")}</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -position-price-emoji } Ціни:</b>
    { $prices }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -item-emoji } Товари:</b>
    { $is_archived ->
        [False] └ Кількість товарів: <code>{ $items_amount }</code>
        *[True] └ Кількість товарів: <code>{ $items_amount }</code>
            {""}
            <blockquote>🗄 Позиція заархівована</blockquote>
    }
    .show-language-btn = Показати на:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Назва
    .description-btn = Опис
    .media-btn = Медіа
    .price-btn = Ціни
    .items-btn = Товари

admin-position-archive-confirmation = <b>🤔 Ви дійсно хочете архівувати позицію <code>{ $name }</code>?</b>

    <blockquote>⚠️ Заархівована позиція стане недоступною для покупки та редагування</blockquote>

admin-position-delete-confirmation = <b>🤔 Ви дійсно хочете видалити позицію <code>{ $name }</code>?</b>

    <blockquote>⚠️ Видалену позицію буде <b>НЕМОЖЛИВО</b> відновити</blockquote>

admin-position-archive-all-confirmation = <b>🤔 Ви дійсно хочете архівувати <i>ВСІ</i> позиції?</b>

    <blockquote>⚠️ Заархівовані позиції стануть недоступними для покупки та редагування</blockquote>

admin-position-delete-all-confirmation = <b>🤔 Ви дійсно хочете видалити <i>ВСІ</i> позиції?</b>

    <blockquote>⚠️ Видалені позиції буде <b>НЕМОЖЛИВО</b> відновити. <i>Будуть видалені лише заархівовані позиції</i></blockquote>
