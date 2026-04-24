admin-payment-methods = <b> { -payment-method-emoji } Payment systems</b>
    .btn = { payment-method }

admin-payment-settings =
    { $commission_percent ->
        [None] <b>⚙️ Settings { payment-method }</b>
        *[other] <b>⚙️ Settings { payment-method }</b>

            <blockquote>ℹ️ Commission rate - { $commission_percent }%</blockquote>
    }
    .commission-btn = Commission:
    .commission-type-btn = { $is_current ->
        [True] { -current } { commission-type } { -current }
        *[False] { commission-type }
    }
    .status-btn = Status
    .switch-status-btn = { $is_active ->
        [True] ✅ Enabled
        *[False] ❌ Disabled
    }

admin-payment-settings-commission = <b>✏️ Enter commission percentage</b>
    .zero-percent = <b>❌ Percentage must be greater than zero</b>
