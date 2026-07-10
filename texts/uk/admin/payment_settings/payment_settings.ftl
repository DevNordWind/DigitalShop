admin-payment-methods = <b> { -payment-method-emoji } Платіжні системи</b>
    .btn = { payment-method }

admin-payment-settings =
    { $commission_percent ->
        [None] <b>⚙️ Налаштування { payment-method }</b>
        *[other] <b>⚙️ Налаштування { payment-method }</b>

            <blockquote>ℹ️ Розмір комісії — { $commission_percent }%</blockquote>
    }
    .commission-btn = Комісія:
    .commission-type-btn = { $is_current ->
        [True] { -current } { commission-type } { -current }
        *[False] { commission-type }
    }
    .status-btn = Статус
    .switch-status-btn = { $is_active ->
        [True] ✅ Увімкнено
        *[False] ❌ Вимкнено
    }

admin-payment-settings-commission = <b>✏️ Введи розмір комісії у відсотках</b>
    .zero-percent = <b>❌ Відсоток має бути більшим за нуль</b>
