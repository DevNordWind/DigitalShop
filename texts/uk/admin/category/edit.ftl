admin-category-edit-name = <b>✏️ Введи нову назву категорії</b>

    { -current } Поточна назва: <code>{ $name ->
        [None] Не вказано даною мовою
        *[other] { $name }
    }</code>
    .default-lang-btn = { -langs-emoji } Мова за замовчуванням
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти іншими мовами

admin-category-edit-name-default-lang = <b>{ -langs-emoji } Мова за замовчуванням</b>

    <blockquote>⚠️ Перед зміною мови за замовчуванням переконайся, що вона заповнена</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }

admin-category-edit-description = <b>✏️ Введи новий опис категорії</b>

    { -current } Поточний опис: { $has_description ->
        [True] { $description ->
            [None] Не вказано даною мовою
            *[other] { $description }
            }
        *[False] { unknown.emoji } Відсутній.

            <blockquote> ⚠️ Обрана мова стане мовою за замовчуванням</blockquote>
    }

    .default-lang-btn = { -langs-emoji } Мова за замовчуванням
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти іншими мовами

admin-category-edit-description-default-lang = <b>{ -langs-emoji } Мова за замовчуванням</b>

    <blockquote>⚠️ Перед зміною мови за замовчуванням переконайся, що вона заповнена</blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }


admin-category-edit-media = <b>{ -media-emoji } Редагування медіа</b>

    <blockquote>ℹ️ Надішли фото, відео або GIF</blockquote>
