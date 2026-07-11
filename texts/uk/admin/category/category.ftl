admin-categories = <b>{ -category-emoji } Категорії</b>
    .order-btn = { -current } { sorting-order } { -current }
    .btn = { $name } | { DATETIME($created_at, dateStyle: "short", timeStyle: "short")} { -time-emoji }
    .settings-btn = ⚙️ Налаштування
    .filters-btn = { -filter-emoji } Фільтри

admins-category-filters = <b>{ -filter-emoji } Фільтри</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { category-status-plural } { -current }
        *[other] { category-status-plural }
    }

admin-category = <b>{ -category-emoji } Редагування категорії</b>

    <b>📜 Основна інформація:</b>
    { admin-category-name }
    { admin-category-description }
    { $updated_at ->
        [None] { -current } Дата створення: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
        *[other] { -current } Дата створення: <i>{ DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</i>
            └ Остання зміна: <i>{ DATETIME($updated_at, dateStyle: "medium", timeStyle: "medium")}</i>
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -item-emoji } Товари:</b>
    ├ К-сть позицій: <code>{ $positions_amount }</code>
    { $is_archived ->
        [False] └ К-сть товарів: <code>{ $items_amount }</code>
        *[True] └ К-сть товарів: <code>{ $items_amount }</code>
            {""}
            <blockquote>🗄 Категорію заархівовано <i>{ DATETIME($archived_at, dateStyle: "medium", timeStyle: "medium")}</i></blockquote>
    }
    .show-language-btn = Показати мовою:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Назва
    .description-btn = Опис
    .media-btn = Медіа

admin-category-archive-confirmation = <b>🤔 Ви дійсно хочете заархівувати категорію <code>{ $name }</code>?</b>

    <blockquote>⚠️ <b>ВСІ</b> позиції категорії також будуть заархівовані</blockquote>

admin-category-delete-confirmation = <b>🤔 Ви дійсно хочете видалити категорію { $name }?</b>

    <blockquote>⚠️ Видалену категорію буде <b>НЕМОЖЛИВО</b> відновити. <i><b>ВСІ</b> позиції також будуть видалені</i></blockquote>

admin-category-archive-all-confirmation = <b>🤔 Ви дійсно хочете заархівувати <i>ВСІ</i> категорії?</b>

    <blockquote>⚠️ Заархівовані категорії стануть недоступними для покупки та редагування.
    <b>ВСІ</b> позиції категорії також будуть заархівовані</blockquote>

admin-category-delete-all-confirmation = <b>🤔 Ви дійсно хочете видалити <i>ВСІ</i> категорії?</b>

    <blockquote>⚠️ Видалені категорії буде <b>НЕМОЖЛИВО</b> відновити.
    <i>Будуть видалені лише заархівовані позиції.
    <b>ВСІ</b> позиції також будуть видалені</i></blockquote>
