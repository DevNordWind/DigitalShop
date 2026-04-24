sorting-order = { $sorting_order ->
        [DESC] Сначала новые
        [ASC] Сначала старые
        *[other] { unknown }
    }

lang = { $lang ->
    [ru] Русский
    [en] Английский
    [uk] Украинский
    *[other] { -unknown }
}
    .emoji = { $lang ->
        [ru] 🇷🇺
        [en] 🇬🇧
        [uk] 🇺🇦
        *[other] { unknown.emoji }
    }
    .ins = { $lang ->
        [ru] Русском
        [en] Английском
        [uk] Украинском
        *[other] { unknown }
    }
    .ins-lower-case = { $lang ->
        [ru] русском
        [en] Английском
        [uk] украинском
        *[other] { unknown }
    }
    .gen = { $lang ->
        [ru] Русского
        [en] Английского
        [uk] Украинского
        *[other] { unknown }
    }

currency = { $currency ->
    [RUB] Рубль
    [USD] Доллар
    [UAH] Гривна
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
        [RUB] рублей
        [USD] долларов
        [UAH] гривен
        [KZT] тенге
        *[other] { unknown }
    }
    .prep = { $currency ->
        [RUB] рублях
        [USD] долларах
        [UAH] гривнах
        [KZT] тенге
        *[other] { unknown }
    }

user-role-lower-case = { $role ->
    [USER] пользователь
    [ADMIN] администратор
    [SUPER_ADMIN] супер администратор
    *[other] { unknown }
}
