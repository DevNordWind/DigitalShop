rate-row = <b>{ -current } { $source_currency }/{ $target_currency }:</b> <code>{ $rate_amount }</code>

user-rates = <b>💱 Currency rates</b>

    { $rate_rows }

    <blockquote>ℹ️ Exchange rates are updated every 6 hours</blockquote>
    .related-btn = 🔎 Similar rates

user-related-rates =
    { $is_rate_ready ->
        [True] <b>🔎 Similar rates</b>

            { rate-row }
        *[False]  <b>🔎 Similar rates</b>
    }
    .source-btn = From:
    .target-btn = To:
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }