admin-general-settings = <b>⚙️ Главные настройки</b>
    .tech-work-btn = 🛠 Технические работы { $tech_work ->
        [True] ✅
        [False] ❌
        *[other] { unknown.emoji }
    }
    .support-contact-btn = 👨‍💻 Тех.поддержка { $support_username ->
        [None] { unknown.emoji } не указана
        *[other] @{ $support_username }
    }
    .referral-percent-btn = 👥 Реферальный процент { $percent }%

admin-general-settings-support = <b>✏️ Введи контакты тех.поддержки</b>

    <blockquote>ℹ️ Пришли username или ссылку на Telegram поддержки</blockquote>

admin-general-settings-referral-percent = <b>✏️ Введи реферальный процент</b>
