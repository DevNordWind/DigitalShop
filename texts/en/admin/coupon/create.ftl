admin-coupon-create-view = <b>{ -coupon-emoji } Create coupon</b>

    <b>{ -current } Code:</b> <code>{ $code ->
        [None] { unknown.emoji } Not set
        *[other] { $code }
    }</code>
    <b>{ -current } Type:</b> { $type ->
            [None] { unknown.emoji } Not set
            *[other] { coupon-type } { $type ->
                [COEFFICIENT] {""}
                    └ Percentage: <code>{ $percent }%</code>
                [FIXED] {""}
                    { $amounts }
                *[other] { unknown }
            }
        }
    ➖➖➖➖➖➖➖➖➖➖
    <b>⏳ Active from:</b> { $valid_from ->
        [None] creation
        *[other] <code>{ DATETIME($valid_from, dateStyle: "medium", timeStyle: "medium")}</code>
    }
    <i> └ Valid until:</i> <code>{ coupon-valid-until }</code>

    <blockquote>🤔 Is everything correct?</blockquote>
    .code-btn = Code
    .valid-from-btn = { -time-emoji } Active from
    .valid-until-btn = { -time-emoji } Valid until
    .type-btn = Type

admin-coupon-create-code = <b>✏️ Enter coupon activation code</b>

    <b>{ -current } Current code:</b> { $code ->
        [None] { unknown.emoji } Not set
        *[other] { $code }
    }

    <blockquote>ℹ️ Example: «DISCOUNT»</blockquote>

admin-coupon-create-type =
    { $type ->
        [None] <b>Select coupon type</b>
        *[other] <b>Select coupon type</b>

            <b>{ -current } Current type:</b> { coupon-type }
            { $type ->
                [COEFFICIENT]  └ Percentage: <code>{ $percent }%</code>
                [FIXED]  { $amounts }
                *[other] { unknown }
            }
    }
    .btn = { coupon-type }

admin-coupon-create-coefficient = <b>✏️ Enter discount percentage</b>

admin-coupon-create-fixed = <b>✏️ Enter discount amount</b>

    <b>{ -current } Current amounts:</b> { $amounts ->
        [None] None
        *[other] {""}
            { $amounts }
    }
    .btn = { $is_current ->
        [True] { -current } { currency } { currency.symbol } { -current }
        *[False] { currency } { currency.symbol }
    }
    .convert-btn = Convert to other currencies

admin-coupon-create-invalid-date = <b>❌ Invalid date format</b>

admin-coupon-create-valid-from = <b>✏️ Enter coupon start date</b>

    <blockquote>ℹ️ Date format: <code>DD.MM.YY HH:MM</code></blockquote>

admin-coupon-create-valid-until = <b>✏️ Enter coupon expiration date</b>

    <blockquote>ℹ️ Date format: <code>DD.MM.YY HH:MM</code></blockquote>
