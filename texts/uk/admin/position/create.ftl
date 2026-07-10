admin-position-create-view = <b>{ -position-emoji } Створення позиції</b>

    <b>📜 Основна інформація:</b>
    { admin-position-name }
    { admin-position-description }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -position-price-emoji } Ціни:</b>{ $prices ->
        [None] { unknown.emoji } Відсутні
        *[other] {""}
            { $prices }
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -media-emoji } Медіа:</b> { $has_media ->
        [False] Не додано
        *[True] Додано
    }
    ➖➖➖➖➖➖➖➖➖➖
    <b>{ -category-emoji } Категорія:</b> <code>{ $category_name }</code>

    <blockquote>🤔 Все правильно?</blockquote>
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

admin-position-create-name = <b>✏️ Введи назву позиції</b>

    { -current } Поточна назва: <code>{ $name ->
        [None] { unknown.emoji } Не вказано
        *[other] { $name }
    }</code>

    <blockquote>ℹ️ Заповнення назви <i>{ lang.ins-lower-case }</i> є <b>обов'язковим</b></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти на інші мови

admin-position-create-description = <b>✏️ Введи опис позиції</b>

    { -current } Поточний опис: { $description ->
        [None] { unknown.emoji } Не вказано
        *[other] { $description }
    }

    <blockquote>ℹ️ Заповнення опису <i>{ lang.ins-lower-case }</i> є <b>обов'язковим</b>. <i>Підтримується HTML форматування</i></blockquote>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
    .translate-btn = Перекласти на інші мови

admin-position-create-price = <b>✏️ Введи ціну позиції в <i>{ $currency }</i></b>

    <b>{ -current } Поточні ціни:</b> { $prices ->
        [None] Відсутні
        *[other] {""}
            { $prices }
    }

    <blockquote>ℹ️ Заповнення цін є <b>обов'язковим</b> для всіх валют</blockquote>
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .convert-btn = Конвертувати в інші валюти

admin-position-create-media = <b>{ -media-emoji } Додавання медіа</b>

    <blockquote>ℹ️ Надішли фото, відео або GIF</blockquote>

admin-position-create-warehouse = <b>{ -item-emoji } Сховище товарів</b>

    { -current } <b>Фіксоване</b> — у позиції лише один, невичерпний товар

    { -current } <b>Поповнюване</b> — у позиції може бути необмежена кількість товарів, які вважаються проданими після покупки

    <blockquote>ℹ️ Додавання товарів стане доступним після створення позиції</blockquote>
    .btn = { $is_current ->
        [True] { -current } { warehouse-type } { -current }
        *[False] { warehouse-type }
    }
