user-select-lang = <b>{ -langs-emoji } Зміна мови</b>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
