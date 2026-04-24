user-select-lang = <b>{ -langs-emoji } Смена языка</b>
    .btn = { $is_current ->
        [True] { -current } { lang.emoji } { lang } { -current }
        *[False] { lang.emoji } { lang }
    }
