referral-award-status = { $status ->
    [PENDING] В обробці
    [COMPLETED] Завершено
    *[other] { unknown }
    }
    .emoji = { $status ->
        [PENDING] ⏳
        [COMPLETED] ✅
        *[other] { unknown.emoji }
}
