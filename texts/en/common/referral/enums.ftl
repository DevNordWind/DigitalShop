referral-award-status = { $status ->
    [PENDING] Processing
    [COMPLETED] Completed
    *[other] { unknown }
    }
    .emoji = { $status ->
        [PENDING] ⏳
        [COMPLETED] ✅
        *[other] { unknown.emoji }
}
