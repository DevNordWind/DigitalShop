sorting-order = { $sorting_order ->
        [DESC] Спочатку нові
        [ASC] Спочатку старі
        *[other] { unknown }
    }

lang = { $lang ->
    [ru] Російська
    [en] Англійська
    [uk] Українська
    *[other] { -unknown }
}
    .emoji = { $lang ->
        [ru] 🇷🇺
        [en] 🇬🇧
        [uk] 🇺🇦
        *[other] { unknown.emoji }
    }
    .ins = { $lang ->
        [ru] Російською
        [en] Англійською
        [uk] Українською
        *[other] { unknown }
    }
    .ins-lower-case = { $lang ->
        [ru] російською
        [en] англійською
        [uk] українською
        *[other] { unknown }
    }
    .gen = { $lang ->
        [ru] Російської
        [en] Англійської
        [uk] Української
        *[other] { unknown }
    }

currency = { $currency ->
    [RUB] Рубль
    [USD] Долар
    [UAH] Гривня
    [KZT] Тенге
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
        [RUB] рублів
        [USD] доларів
        [UAH] гривень
        [KZT] тенге
        *[other] { unknown }
    }
    .prep = { $currency ->
        [RUB] рублях
        [USD] доларах
        [UAH] гривнях
        [KZT] тенге
        *[other] { unknown }
    }

user-role-lower-case = { $role ->
    [USER] користувач
    [ADMIN] адміністратор
    [SUPER_ADMIN] супер адміністратор
    *[other] { unknown }
}
