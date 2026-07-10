admin-statistic-top-ups =
    <b>📥 Поповнень:</b> <code>{ $count }</code>
    └ На суму: <code>{ $amount }{ currency.symbol }</code>

admin-statistic-sales =
    <b>🛒 Продажів:</b> <code>{ $count }</code>
    └ На суму: <code>{ $amount }{ currency.symbol }</code>

admin-statistic-period-unit = { $unit ->
    [WEEK] За тиждень
    [MONTH] За місяць
    [TODAY] За сьогодні
    [None] За весь час
    *[other] { unknown }
}

admin-statistic = <b>📊 Статистика</b>

    <b>👥 Нових користувачів:</b> { $new_users }
    ➖➖➖➖➖➖➖➖➖➖
    { $sales }
    ➖➖➖➖➖➖➖➖➖➖
    { $top_ups }
    ➖➖➖➖➖➖➖➖➖➖
    <b>📦 Товари:</b>
    ├ Категорій: <code>{ $category_count }</code>
    ├ Позицій: <code>{ $position_count }</code>
    └ Товарів: <code>{ $items_count }</code>

    <blockquote>🕰 Статистика { $has_period ->
        [True] від { $from_date } до { $to_date }
        *[False] За весь час
    }
    </blockquote>
    .period-unit-btn = { $is_current ->
        [True] { -current } { admin-statistic-period-unit } { -current }
        *[False] { admin-statistic-period-unit }
    }
    .period-btn = 🕰 Власний період
    .convert-btn = 💱 Конвертувати

-admin-statistic-period-title = <b>✏️ Введи період статистики</b>

admin-statistic-period =
    { $has_custom_period ->
        [False] { -admin-statistic-period-title }
        *[True] { -admin-statistic-period-title }
            {""}
            <b>{ -current } Поточний період:</b> <code>{ $from_date } - { $to_date }</code>
    }

    <blockquote>ℹ️ Формат: <code>ММ.ДД.ГГ - ММ.ДД.ГГ</code></blockquote>
    .invalid = <b>❌ Невірний формат періоду</b>

admin-statistic-convert = <b>💱 Конвертація статистики</b>

    <blockquote>ℹ️ Суми статистики будуть рахуватися у вказаній валюті</blockquote>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }
