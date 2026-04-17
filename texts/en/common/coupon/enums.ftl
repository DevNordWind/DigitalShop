coupon-status = { $status ->
    [ACTIVE] Active
    [EXPIRED] Expired
    [REVOKED] Revoked
    [NOT_STARTED] Pending
    *[other] { unknown }
    }

coupon-type = { $type ->
    [FIXED] Fixed amount
    [COEFFICIENT] Percentage of order total
    *[other] { unknown }
}