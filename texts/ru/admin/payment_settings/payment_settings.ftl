admin-payment-methods = <b> { -payment-method-emoji } Платёжные системы</b>
    .btn = { payment-method }

admin-payment-settings =
    { $commission_percent ->
        [None] <b>⚙️ Настройки { payment-method }</b>
        *[other] <b>⚙️ Настройки { payment-method }</b>

            <blockquote>ℹ️ Размер комиссии - { $commission_percent }%</blockquote>
    }
    .commission-btn = Комиссия:
    .commission-type-btn = { $is_current ->
        [True] { -current } { commission-type } { -current }
        *[False] { commission-type }
    }
    .status-btn = Стаутс
    .switch-status-btn = { $is_active ->
        [True] ✅ Включено
        *[False] ❌ Выключено
    }

admin-payment-settings-commission = <b>✏️ Введи размер комиссии в процентах</b>
    .zero-percent = <b>❌ Процент должен быть больше нуля</b>