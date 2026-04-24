<div align="center">

# 🛒 DigitalShop

**Платформа для продажи цифровых товаров**

[![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-4169E1?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-latest-DC382D?logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-22c55e)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://img.shields.io/badge/mypy-checked-2A6DB2?logo=python&logoColor=white)](https://mypy-lang.org)

[🇷🇺 Русский](docs/README_ru.md) | [🇬🇧 English](README.en.md)

</div>

---

## 📋 Содержание

- [О проекте](#-о-проекте)
- [Todo](#-todo)
- [Возможности](#-возможности)
- [Стек технологий](#-стек-технологий)
- [Установка](#-установка)
- [Запуск](#-запуск)
- [Конфигурация](#-конфигурация)

---

## 💡 О проекте

**DigitalShop** — платформа для продажи цифровых товаров. Поддерживает гибкую иерархию товаров, платёжную систему Crypto Pay от <a href="https://t.me/send">@send</a>, реферальную программу и массовые рассылки. На данный момент, в презентационном слое реализован полноценный Telegram-бот.

---

## ✨ Возможности

<details>
<summary><b>🌐 Мультиязычность и мультивалютность</b></summary>

- **Языки:** русский, английский
- **Валюты:** USD, RUB, UAH, KZT

</details>

<details>
<summary><b>📦 Гибкое управление товарами</b></summary>

- Трёхуровневая иерархия: **Категория** → **Позиция** → **Товар**
  *(например: Подписки → Netflix → конкретный ключ активации)*
- Фиксированные товары и исчерпаемые (инвентарь)
- Медиавложения к категориям и позициям — до 10 файлов (фото, видео, GIF)

</details>

<details>
<summary><b>👥 Реферальная система</b></summary>

- Вознаграждение в виде настраиваемого процента от суммы заказа реферала

</details>

<details>
<summary><b>🎟️ Купоны</b></summary>

- Применяются на этапе оформления заказа
- Два типа скидки: фиксированная сумма или процент от заказа
- Настраиваемые даты начала и окончания действия

</details>

<details>
<summary><b>💳 Платёжные системы</b></summary>

- Встроенная интеграция с **CryptoBot**
- Возможность включать и отключать отдельные платёжные системы
- Индивидуальная комиссия для каждой платёжной системы

</details>

<details>
<summary><b>👤 Управление пользователями</b></summary>

Иерархия ролей: **Супер-администратор** → **Администратор** → **Пользователь**

Администраторам доступны:
- Поиск пользователей
- Повышение и понижение роли
- Просмотр всех заказов пользователя
- Пополнение баланса

</details>

<details>
<summary><b>📣 Рассылки</b></summary>

- Рассылки на нескольких языках одновременно
- Добавление URL-кнопок к сообщению
- Уведомления о прогрессе в реальном времени

</details>

---

## 📌 Todo

- [ ] Настройка CI
- [ ] Написание unit и integration тестов для доменного и сервисного слоя
- [ ] Обзор архитектурных решений
- [ ] Написание REST API

---

## 🛠 Стек технологий

| Категория | Технологии |
|-----------|------------|
| **Язык / пакетный менеджер** | Python 3.14, uv |
| **Telegram** | Aiogram, Aiogram-Dialog |
| **Web** | FastAPI |
| **Очереди и планировщик** | TaskIQ |
| **DI / Сериализация** | Dishka, Adaptix |
| **База данных** | PostgreSQL 18, SQLAlchemy, Alembic |
| **Кэш / Брокер** | Redis |
| **Линтинг** | Ruff, mypy |
| **Инфраструктура** | Docker |

---

## 📦 Установка

**1. Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/digitalshop.git
cd digitalshop
```

**2. Заполните конфигурационный файл:**
```bash
cp config.yaml.example config.yaml
# Отредактируйте config.yaml под своё окружение
```

**3. Соберите Docker-образы:**
```bash
make build
```

---

## 🚀 Запуск

DigitalShop состоит из нескольких независимых сервисов. Запускайте только те, которые нужны.

### Telegram-бот

```bash
make polling-up   # Polling-режим (рекомендуется для разработки)
make webhook-up   # Webhook-режим (требует заполнения секции webhook в конфиге)
```

### Платёжные вебхуки

```bash
make payment-up   # FastAPI-сервер для получения вебхуков от CryptoPay
```

### Сервисы TaskIQ

| Entrypoint | Назначение |
|---|---|
| `taskiq.broker` | Обработка Telegram-рассылок |
| `taskiq.priority_broker` | Уведомления и фоновые задачи (например, отмена заказа) |
| `taskiq.scheduler` | Планировщик задач |

---

## ⚙️ Конфигурация

Все настройки хранятся в `config.yaml`. Пример со всеми доступными параметрами — в [`config.yaml.example`](config.yaml.example).

> [!IMPORTANT]
> Перед первым запуском обязательно заполните `config.yaml`. Бот не запустится без корректно заданных токена и параметров базы данных.

> [!NOTE]
> Для webhook-режима необходимо дополнительно заполнить секцию `webhook` в конфигурационном файле.
>

> [!WARNING]
> Это пет-проект, созданный в учебных целях. Я не несу ответственности за любые убытки, потерю данных или иные последствия, возникшие в результате использования в продакшен-среде. **Используйте на свой страх и риск.**
