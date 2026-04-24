sorting-order = { $sorting_order ->
        [DESC] New first
        [ASC] Old first
        *[other] { unknown }
    }

lang = { $lang ->
        [ru] Russian
        [en] English
        [uk] Ukrainian
        *[other] { -unknown }
    }
    .emoji = { $lang ->
        [ru] 🇷🇺
        [en] 🇬🇧
        [uk] 🇺🇦
        *[other] { unknown.emoji }
    }
    .ins = { $lang ->
        [ru] Russian
        [en] English
        [uk] Ukrainian
        *[other] { unknown }
    }
    .ins-lower-case = { $lang ->
        [ru] russian
        [en] english
        [uk] ukrainian
        *[other] { unknown }
    }
    .gen = { $lang ->
        [ru] Russian
        [en] English
        [uk] Ukrainian
        *[other] { unknown }
    }

currency = { $currency ->
        [RUB] Ruble
        [USD] Dollar
        [UAH] Hryvnia
        [KZT] Tenge
        *[other] { unknown }
    }
    .symbol =  { $currency ->
        [RUB] ₽
        [USD] $
        [UAH] ₴
        [KZT] ₸
        *[other] { unknown.emoji }
    }
    .gen = { $currency ->
        [RUB] rubles
        [USD] dollars
        [UAH] hryvnias
        [KZT] tenge
        *[other] { unknown }
    }
    .prep = { $currency ->
        [RUB] rubles
        [USD] dollars
        [UAH] hryvnias
        [KZT] tenge
        *[other] { unknown }
    }

user-role-lower-case = { $role ->
        [USER] user
        [ADMIN] administrator
        [SUPER_ADMIN] super administrator
        *[other] { unknown }
    }
