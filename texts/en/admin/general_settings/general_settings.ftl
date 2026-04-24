admin-general-settings = <b>⚙️ Main settings</b>
    .tech-work-btn = 🛠 Maintenance mode { $tech_work ->
        [True] ✅
        [False] ❌
        *[other] { unknown.emoji }
    }
    .support-contact-btn = 👨‍💻 Support { $support_username ->
        [None] { unknown.emoji } not set
        *[other] @{ $support_username }
    }
    .referral-percent-btn = 👥 Referral percent { $percent }%

admin-general-settings-support = <b>✏️ Enter support contact</b>

    <blockquote>ℹ️ Send username or Telegram support link</blockquote>

admin-general-settings-referral-percent = <b>✏️ Enter referral percent</b>
