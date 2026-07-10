admin-category-create-view =  <b> { -category-emoji } Створення категорії</b>

    <b>📜 Основна інформація:</b>
    { admin-category-name }
    { admin-category-description }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -media-emoji } Медіа:</b> { $has_media ->
        [False] Не додано
        *[True] Додано
    }

    <blockquote>🤔 Все правильно?</blockquote>
    .show-language-btn = Показати мовою:
    .lang-btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang.ins } { -current }
        *[False] { lang.emoji } { lang.ins }
    }
    .name-btn = Назва
    .description-btn = Опис
    .media-btn = Медіа

admin-category-create-name = <b>✏️ Введи назву категорії</b>

    { -current } Поточна назва: <code>{ $name ->
        [None] { unknown.emoji } Не вказано
        *[other] { $name }
    }</code>

    <blockquote>ℹ️ Заповнення назви <i>{ lang.ins-lower-case }</i> є <b>обов'язковим</b></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти іншими мовами

admin-category-create-description = <b>✏️ Введи опис категорії</b>

    { -current } Поточний опис: { $description ->
        [None] { unknown.emoji } Не вказано
        *[other] { $description }
    }

    <blockquote>ℹ️ Заповнення опису <i>{ lang.ins-lower-case }</i> є <b>обов'язковим</b>. <i>Підтримується HTML форматування</i></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти іншими мовами

admin-category-create-media = <b>{ -media-emoji } Додавання медіа</b>

    <blockquote>ℹ️ Надішли фото, відео або GIF</blockquote>
