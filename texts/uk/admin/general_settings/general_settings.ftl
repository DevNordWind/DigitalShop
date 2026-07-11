admin-general-settings = <b>⚙️ Головні налаштування</b>
    .tech-work-btn = 🛠 Технічні роботи { $tech_work ->
        [True] ✅
        [False] ❌
        *[other] { unknown.emoji }
    }
    .support-contact-btn = 👨‍💻 Техпідтримка { $support_username ->
        [None] { unknown.emoji } не вказано
        *[other] @{ $support_username }
    }
    .referral-percent-btn = 👥 Реферальний відсоток { $percent }%

admin-general-settings-support = <b>✏️ Введи контакти техпідтримки</b>

    <blockquote>ℹ️ Надішли username або посилання на Telegram-підтримку</blockquote>

admin-general-settings-referral-percent = <b>✏️ Введи реферальний відсоток</b>
