<div align="center">

# 🛒 DigitalShop

**A platform for selling digital goods**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-latest-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-2A6DB2?logo=python&logoColor=white)](https://mypy-lang.org)

[🇷🇺 Russian](docs/README_ru.md) | [🇬🇧 English](#)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Todo](#-todo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running](#-running)
- [Configuration](#-configuration)

---

## 💡 About

**DigitalShop** is a platform for selling digital goods. It supports a flexible product hierarchy, Crypto Pay integration via <a href="https://t.me/send">@send</a>, a referral program, and bulk messaging. The presentation layer is currently implemented as a fully functional Telegram bot.

---

## ✨ Features

<details>
<summary><b>🌐 Multi-language & Multi-currency</b></summary>

- **Languages:** Russian, English
- **Currencies:** USD, RUB, UAH, KZT

</details>

<details>
<summary><b>📦 Flexible Product Management</b></summary>

- Three-level hierarchy: **Category** → **Item** → **Product**
  *(e.g. Subscriptions → Netflix → specific activation key)*
- Fixed products and exhaustible inventory
- Media attachments for categories and items — up to 10 files (photos, videos, GIFs)

</details>

<details>
<summary><b>👥 Referral System</b></summary>

- Configurable percentage reward based on the referred user's order amount

</details>

<details>
<summary><b>🎟️ Coupons</b></summary>

- Applied at checkout
- Two discount types: fixed amount or percentage off the order total
- Configurable start and expiration dates

</details>

<details>
<summary><b>💳 Payment Systems</b></summary>

- Built-in **CryptoBot** integration
- Enable or disable individual payment methods
- Custom commission rate per payment method

</details>

<details>
<summary><b>👤 User Management</b></summary>

Role hierarchy: **Super Admin** → **Admin** → **User**

Admins can:
- Search for users
- Promote and demote roles
- View a user's full order history
- Top up user balance

</details>

<details>
<summary><b>📣 Broadcasting</b></summary>

- Send broadcasts in multiple languages simultaneously
- Attach URL buttons to broadcast messages
- Real-time progress notifications

</details>

---

## 📌 Todo

- [ ] CI setup
- [ ] Unit and integration tests for the domain and service layers
- [ ] Architectural decisions overview
- [ ] REST API

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| **Language / Package Manager** | Python 3.14, uv |
| **Telegram** | Aiogram, Aiogram-Dialog |
| **Web** | FastAPI |
| **Queues & Scheduler** | TaskIQ |
| **DI / Serialization** | Dishka, Adaptix |
| **Database** | PostgreSQL 18, SQLAlchemy, Alembic |
| **Cache / Broker** | Redis |
| **Linting** | Ruff, mypy |
| **Infrastructure** | Docker |

---

## 📦 Installation

**1. Clone the repository:**
```bash
https://github.com/DevNordWind/DigitalShop
cd DigitalShop
```

**2. Fill in the configuration file:**
```bash
cp config.yaml.example config.yaml
# Edit config.yaml for your environment
```

**3. Build Docker images:**
```bash
make build
```

---

## 🚀 Running

DigitalShop consists of several independent services. Run only the ones you need.

### Telegram Bot

```bash
make polling-up   # Polling mode (recommended for development)
make webhook-up   # Webhook mode (requires the webhook section to be filled in the config)
```

### Payment Webhooks

```bash
make payment-up   # FastAPI server for receiving CryptoPay webhooks
```

### TaskIQ Services

| Entrypoint | Purpose |
|---|---|
| `taskiq.broker` | Processes Telegram broadcasts |
| `taskiq.priority_broker` | Notifications and background tasks (e.g. order cancellation) |
| `taskiq.scheduler` | Task scheduler |

---

## ⚙️ Configuration

All settings are stored in `config.yaml`. A full example with all available parameters can be found in [`config.yaml.example`](config.yaml.example).

> [!IMPORTANT]
> Fill in `config.yaml` before the first run. The bot will not start without a valid bot token and database credentials.

> [!NOTE]
> Webhook mode requires the `webhook` section to be filled in the configuration file.

> [!WARNING]
> This is a pet project built for learning purposes. I am not responsible for any losses, data corruption, or other consequences resulting from use in a production environment. **Use at your own risk.**
