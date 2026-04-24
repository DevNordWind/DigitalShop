admin-statistic-top-ups =
    <b>📥 Top-ups:</b> <code>{ $count }</code>
    └ Total amount: <code>{ $amount }{ currency.symbol }</code>

admin-statistic-sales =
    <b>🛒 Sales:</b> <code>{ $count }</code>
    └ Total amount: <code>{ $amount }{ currency.symbol }</code>

admin-statistic-period-unit = { $unit ->
    [WEEK] Last week
    [MONTH] Last month
    [TODAY] Today
    [None] All time
    *[other] { unknown }
}

admin-statistic = <b>📊 Statistics</b>

    <b>👥 New users:</b> { $new_users }
    ➖➖➖➖➖➖➖➖➖➖
    { $sales }
    ➖➖➖➖➖➖➖➖➖➖
    { $top_ups }
    ➖➖➖➖➖➖➖➖➖➖
    <b>📦 Products:</b>
    ├ Categories: <code>{ $category_count }</code>
    ├ Positions: <code>{ $position_count }</code>
    └ Items: <code>{ $items_count }</code>

    <blockquote>🕰 Statistics { $has_period ->
        [True] from { $from_date } to { $to_date }
        *[False] All time
    }
    </blockquote>
    .period-unit-btn = { $is_current ->
        [True] { -current } { admin-statistic-period-unit } { -current }
        *[False] { admin-statistic-period-unit }
    }
    .period-btn = 🕰 Custom period
    .convert-btn = 💱 Convert

-admin-statistic-period-title = <b>✏️ Enter statistics period</b>

admin-statistic-period =
    { $has_custom_period ->
        [False] { -admin-statistic-period-title }
        *[True] { -admin-statistic-period-title }
            {""}
            <b>{ -current } Current period:</b> <code>{ $from_date } - { $to_date }</code>
    }

    <blockquote>ℹ️ Format: <code>MM:DD:YY - MM:DD:YY</code></blockquote>
    .invalid = <b>❌ Invalid period format</b>

admin-statistic-convert = <b>💱 Statistics conversion</b>

    <blockquote>ℹ️ Statistics amounts will be calculated in the selected currency</blockquote>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }
