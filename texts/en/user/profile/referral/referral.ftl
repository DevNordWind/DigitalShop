referral-default = { -current } Invite referrals and earn <b>{ $percent }%</b> from order amounts

referral-time-unit = { $unit ->
    [WEEK] This week
    [MONTH] This month
    [TODAY] Today
    [None] For all time
    *[other] { unknown }
}

referral = <b>👥 Referrals</b>

    { $is_referrer ->
        [False] { referral-default }
        *[True]  { referral-default }

        <b>📊 Statistics</b>:
        ├ Invited: <code>{ $referral_count }</code>
        ├ Rewards count: <code>{ $awards_count }</code>
        └ Earned: <code>{ $total_amount }{ currency.symbol }</code>

        <b>🔗 Your referral link:</b> { $link }
    }
    .time-unit-btn = { $is_current ->
        [True] { -current } { referral-time-unit } { -current }
        *[False] { referral-time-unit }
    }
    .get-link-btn = 🔗 Get link
    .my-awards-btn = 🏆 My rewards
    .change-currency-btn = 💱 Change currency
    .notifications-btn = { $send_notifications ->
        [True] 🔕 Disable notifications
        *[False] 🔔 Enable notifications
    }

referral-change-currency = <b>{ -wallet-emoji } Choose the currency in which you want to receive rewards</b>
    .btn = { $is_current ->
        [True] { -current } { $currency } { -current }
        *[False] { $currency }
    }

referral-my-awards = <b>🏆 My rewards</b>
    .btn = { $status ->
        [COMPLETED] { $amount }{ currency.symbol } | { DATETIME($created_at, dateStyle: "short")} { referral-award-status.emoji }
        [PENDING] { DATETIME($created_at, dateStyle: "short")} { referral-award-status.emoji }
        *[other] { unknown }
    }
    .order-btn = { -current } { sorting-order } { -current }

referral-my-award-completed =
    <b>💸 Reward amount: <code>{ $amount }{ currency.symbol }</code></b>
    └ Percent: <code>{ $percent }%</code>

    <blockquote>{ -time-emoji } Credited to balance at { DATETIME($completed_at, dateStyle: "medium", timeStyle: "medium")}</blockquote>

referral-my-award-pending =
    <blockquote>{ -time-emoji } Processing since { DATETIME($created_at, dateStyle: "medium", timeStyle: "medium")}</blockquote>

referral-my-award = <b>🏆 Reward</b>

    { $status ->
        [COMPLETED] { referral-my-award-completed }
        [PENDING] { referral-my-award-pending }
        *[other] { Unknown }
    }
