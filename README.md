<div align="center">

# 🛒 DigitalShop

**A flexible solution for launching a digital goods store on Telegram**

[![Python](https://img.shields.io/badge/Python-3.14.6-3776AB?logo=python\&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18.4-4169E1?logo=postgresql\&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-8.8.0-DC382D?logo=redis\&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker\&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Pyrefly](https://img.shields.io/badge/Pyrefly-checked-1F425F?logo=python\&logoColor=white)](https://github.com/facebook/pyrefly)

[🇬🇧 English](README.md) | [🇷🇺 Russian](docs/README_ru.md)

</div>

---

## 📋 Table of Contents

* [About the Project](#-about-the-project)
* [Business Features](#-business-features)
* [Todo](#-todo)
* [Technology Stack](#-technology-stack)
* [Installation](#-installation)
* [Running](#-running)
* [Configuration](#-configuration)

---

## 💡 About the Project

**DigitalShop** is a platform for selling digital goods. It supports a flexible product hierarchy, **Crypto Pay** integration by <a href="https://t.me/send">@CryptoBot</a>, a referral program, and bulk messaging. At the moment, the presentation layer is implemented as a fully functional Telegram bot.

<p align="center">
  <img src="docs/screenshots/root.png" width="320">
</p>

---

## ✨ Business Features

<details>
<summary><b>🇷🇺🇬🇧🇺🇦 Multi-language & Multi-currency Support</b></summary>

* **Languages:** Russian, English, Ukrainian
* **Currencies:** USD, RUB, UAH, KZT

</details>

<details>
<summary><b>📦 Flexible Product Management</b></summary>

* Three-level hierarchy: **Category** → **Item** → **Product**
  *(e.g. 🎮 Steam Accounts → Half-Life 2 → Activation Key)*
* Support for both unlimited (fixed) and stock-based products
* Media attachments for categories and items — up to 10 files (photos, videos, GIFs)

</details>

<details>
<summary><b>👥 Referral System</b></summary>

* Reward users with a configurable percentage of each referred customer's order amount

</details>

<details>
<summary><b>🎟️ Coupons</b></summary>

* Applied during checkout
* Two discount types: fixed amount or percentage
* Configurable start and expiration dates

</details>

<details>
<summary><b>💳 Payment Systems</b></summary>

* Built-in **Crypto Pay** integration
* Enable or disable individual payment methods
* Custom commission for each payment method

</details>

<details>
<summary><b>👤 User Management</b></summary>

Role hierarchy: **Super Administrator** → **Administrator** → **User**. Each role inherits the permissions of the lower role (for example, a `Super Administrator` has access to all `Administrator` permissions) while also having its own exclusive permissions.

</details>

<details>
<summary><b>📣 Broadcast Messaging</b></summary>

* Send broadcasts in multiple languages simultaneously
* Attach URL buttons to messages
* Real-time progress notifications

</details>

> [!NOTE]
> You can read more about the bot's architecture and business features [here](docs/features/en.md).

---

## 📌 Todo

* [ ] Write unit and integration tests
* [ ] Set up CI
* [ ] Document architectural decisions
* [ ] Implement a REST API

---

## 🛠 Technology Stack

| Category                                 | Technologies                       |
| ---------------------------------------- | ---------------------------------- |
| **Language / Package Manager**           | Python 3.14, uv                    |
| **Telegram**                             | Aiogram, Aiogram-Dialog            |
| **Web**                                  | FastAPI                            |
| **Task Queue & Scheduler**               | TaskIQ                             |
| **Dependency Injection / Serialization** | Dishka, Adaptix                    |
| **Database**                             | PostgreSQL 18, SQLAlchemy, Alembic |
| **Cache / Message Broker**               | Redis                              |
| **Linting**                              | Ruff, Pyrefly                      |
| **Infrastructure**                       | Docker                             |

---

## 📦 Installation

**1. Clone the repository:**

```bash
git clone https://github.com/DevNordWind/DigitalShop.git
cd DigitalShop
```

**2. Create and configure the configuration file:**

```bash
cp config.yaml.example config.yaml
# Edit config.yaml to match your environment
```

**3. Build the Docker images:**

```bash
make build
```

---

## 🚀 Running

DigitalShop consists of several independent services. Start only the ones you need.

### Telegram Bot

```bash
make polling-up   # Polling mode (recommended for development)
make webhook-up   # Webhook mode (requires the webhook section to be configured)
```

### Payment Webhooks

```bash
make payment-up   # FastAPI server for receiving Crypto Pay webhooks
```

### TaskIQ Services

| Entrypoint               | Purpose                                                                |
| ------------------------ | ---------------------------------------------------------------------- |
| `taskiq.broker`          | Processes Telegram broadcast messages                                  |
| `taskiq.priority_broker` | Notifications and background tasks (e.g. automatic order cancellation) |
| `taskiq.scheduler`       | Task scheduler                                                         |

---

## ⚙️ Configuration

All settings are stored in `config.yaml`. A complete example with all available options can be found in [`config.yaml.example`](config.yaml.example).

> [!IMPORTANT]
> Before running the project for the first time, make sure to configure `config.yaml`. The bot will not start without a valid bot token and database configuration.

> [!NOTE]
> To use webhook mode, you must also configure the `webhook` section in `config.yaml`.

> [!WARNING]
> This is a pet project created for educational purposes. I am not responsible for any losses, data corruption, or other consequences resulting from its use in a production environment. **Use it at your own risk.**
