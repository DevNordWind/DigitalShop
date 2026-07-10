rate-row = <b>{ -current } { $source_currency }/{ $target_currency }:</b> <code>{ $rate_amount }</code>

user-rates = <b>💱 Курси валют</b>

    { $rate_rows }

    <blockquote>ℹ️ Курси валют оновлюються кожні 6 годин</blockquote>
    .related-btn = 🔎 Суміжні курси

user-related-rates =
    { $is_rate_ready ->
        [True] <b>🔎 Суміжні курси</b>

            { rate-row }
        *[False]  <b>🔎 Суміжні курси</b>
    }
    .source-btn = З:
    .target-btn = До:
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }
