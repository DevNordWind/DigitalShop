rate-row = <b>{ -current } { $source_currency }/{ $target_currency }:</b> <code>{ $rate_amount }</code>

user-rates = <b>💱 Курсы валют</b>

    { $rate_rows }

    <blockquote>ℹ️ Курсы валют обновляются каждые 6 часов</blockquote>
    .related-btn = 🔎 Смежные курсы

user-related-rates =
    { $is_rate_ready ->
        [True] <b>🔎 Смежные курсы</b>

            { rate-row }
        *[False]  <b>🔎 Смежные курсы</b>
    }
    .source-btn = Из:
    .target-btn = В:
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }
