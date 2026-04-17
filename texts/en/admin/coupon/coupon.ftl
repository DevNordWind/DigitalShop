admin-coupons = <b>{ -coupon-emoji } Coupons</b>

    <blockquote>⚙️ Select a coupon for revocation or detailed information</blockquote>
    .filters = { -filter-emoji } Filters
    .btn = { $code } | { $type ->
        [FIXED] Fixed
        [COEFFICIENT] { $percent }%
        *[other] { unknown }
    }

admin-coupon = <b>🎫 Coupon { $code }</b>

    <b>{ -current } Type:</b> { coupon-type }
    { $type ->
        [COEFFICIENT]└ Percentage: <code>{ $percent }%</code>
        [FIXED] { $amounts }
        *[other] { unknown }
    }
    { $is_revoked ->
        [True]{""}
            <blockquote>♻️ Coupon revoked</blockquote>
        *[False]
            ➖➖➖➖➖➖➖➖➖➖
            <b>⏳ Active from:</b> <code>{ DATETIME($valid_from, dateStyle: "medium", timeStyle: "medium")}</code>
            <i> └ Valid until:</i> <code>{ coupon-valid-until }</code>
    }
    .revoke-btn = ♻️ Revoke


admin-coupons-filters = <b>{ -filter-emoji } Filters</b>
    .order-btn = { -current } { sorting-order } { -current }
    .status-btn = { $is_current ->
        [True] { -current } { coupon-status } { -current }
        *[other] { coupon-status }
    }