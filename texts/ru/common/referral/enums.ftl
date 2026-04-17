referral-award-status = { $status ->
    [PENDING] В обработке
    [COMPLETED] Завершено
    *[other] { unknown }
    }
    .emoji = { $status ->
        [PENDING] ⏳
        [COMPLETED] ✅
        *[other] { unknown.emoji }
}