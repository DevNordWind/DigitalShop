admin-statistic-top-ups =
    <b>📥 Пополнений:</b> <code>{ $count }</code>
    └ На сумму: <code>{ $amount }{ currency.symbol }</code>

admin-statistic-sales =
    <b>🛒 Продаж:</b> <code>{ $count }</code>
    └ На сумму: <code>{ $amount }{ currency.symbol }</code>

admin-statistic-period-unit = { $unit ->
    [WEEK] За неделю
    [MONTH] За месяц
    [TODAY] За сегодня
    [None] За всё время
    *[other] { unknown }
}

admin-statistic = <b>📊 Статистика</b>

    <b>👥 Новых пользователей:</b> { $new_users }
    ➖➖➖➖➖➖➖➖➖➖
    { $sales }
    ➖➖➖➖➖➖➖➖➖➖
    { $top_ups }
    ➖➖➖➖➖➖➖➖➖➖
    <b>📦 Товары:</b>
    ├ Категорий: <code>{ $category_count }</code>
    ├ Позиций: <code>{ $position_count }</code>
    └ Товаров: <code>{ $items_count }</code>

    <blockquote>🕰 Статистика { $has_period ->
        [True] от { $from_date } до { $to_date }
        *[False] За всё время
    }
    </blockquote>
    .period-unit-btn = { $is_current ->
        [True] { -current } { admin-statistic-period-unit } { -current }
        *[False] { admin-statistic-period-unit }
    }
    .period-btn = 🕰 Свой пероид
    .convert-btn = 💱 Конвертировать

-admin-statistic-period-title = <b>✏️ Введи период статистики</b>

admin-statistic-period =
    { $has_custom_period ->
        [False] { -admin-statistic-period-title }
        *[True] { -admin-statistic-period-title }
            {""}
            <b>{ -current } Текщий период:</b> <code>{ $from_date } - { $to_date }</code>
    }

    <blockquote>ℹ️ Формат: <code>ММ:ДД:ГГ - ММ:ДД:ГГ</code></blockquote>
    .invalid = <b>❌ Неверный формат периода</b>

admin-statistic-convert = <b>💱 Конвертация статистики</b>

    <blockquote>ℹ️ Суммы статистики буду считаться в указанной валюте</blockquote>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }

