# General

---

### 👥 Role Hierarchy and Access Levels

The bot uses a three-level role hierarchy: `Super Administrator`, `Administrator`, and `User`.

Each role inherits all permissions of the lower role (for example, a `Super Administrator` has access to all `Administrator` permissions) while also having its own exclusive privileges.

* **Super Administrator:** The highest level of access. Unlike a regular administrator, a Super Administrator can grant, modify, or revoke roles and permissions for other users. A user can only become a Super Administrator if their Telegram ID is specified in `config.yaml` (excluding direct database modifications).
* **Administrator:** Manages store content, products, and settings, but cannot assign administrator roles.
* **User:** A regular customer of the bot.

### 🇷🇺🇬🇧🇺🇦 Multi-language Support

The bot fully supports three languages: **English**, **Russian**, and **Ukrainian**. Localization is implemented on two levels:

1. **Bot Interface (System Localization):** All built-in messages, buttons, and menus are pre-translated and stored in Fluent localization files (`texts/` directory). Each user sees the interface in their selected language.
2. **Store Content (Dynamic Localization):** Category and Item names and descriptions created by administrators during normal operation.

   * **Content creation:** When creating a new category or item, only the **default language** is required. Translations into the remaining languages are automatically generated based on the default language.

### 💳 Multi-currency Support and Finance

The financial system is designed for multiple markets and supports four currencies: **USD**, **RUB**, **UAH**, and **KZT**.

* **Exchange rates** are provided by the Crypto Pay API (@CryptoBot) and are updated every 6 hours.
* **Calculation precision:** All balances and financial operations use precise decimal arithmetic with banker's rounding.
* **Pricing:** Every `Item` must have prices specified for all supported currencies. The default currency serves as the base currency, from which prices are converted into the remaining currencies during setup.
* **User wallets:** Every customer has four independent balances (one for each supported currency). The currency selected in the user's settings is used both for displaying prices and for charging purchases.

# 🛠 Admin Panel

---

### 🗃 Categories

* **Statuses:** Categories can have one of two statuses: `Available` and `Archived`.

  * `Available` categories can be edited but cannot be deleted.
  * `Archived` categories cannot be edited, can be deleted, and are hidden from users.
* **Media:** Each category supports a single media attachment (photo, video, or GIF).
* **Description:** Category descriptions are optional.

###### ⚙️ Category Settings

* **🇷🇺🇬🇧🇺🇦 Default Language:** Required when creating a new category. All remaining translations are generated automatically based on this language.

* **📦 Empty Categories:** If set to `🚫 Hide`, the category will not be displayed if none of its `Items` contain any products.

### 📁 Items

* **Statuses:** Items can have one of two statuses: `Available` and `Archived`.

  * `Available` items can be edited but cannot be deleted.
  * `Archived` items cannot be edited, can be deleted, and are hidden from users.
* **Media:** Each item supports up to 10 media attachments (photos, videos, or GIFs).
* **Description:** Item descriptions are optional.
* **Pricing:** Prices must be explicitly specified for all four supported currencies.

###### ⚙️ Item Settings

* **🇷🇺🇬🇧🇺🇦 Default Language:** Required when creating a new item. All remaining translations are automatically generated from it.

* **📦 Empty Items:** If set to `🚫 Hide`, the item will not be displayed unless it contains at least one product.

* **🪙 Default Currency:** Used as the base currency when converting prices into the remaining currencies.

### 🎫 Coupons

* **Statuses:** Coupons can have four statuses:

  * `Active`
  * `Revoked`
  * `Expired`
  * `Pending`

  Status descriptions:

  1. **Active** — the coupon can currently be redeemed.
  2. **Revoked** — the coupon has been manually disabled by the administration.
  3. **Expired** — the coupon's validity period has ended.
  4. **Pending** — the coupon's validity period has not yet started.

* **Coupon Code:** Must be unique.

* **Validity Period:** Consists of an optional start and end date.

  1. If no start date is specified, the coupon becomes active immediately after creation.
  2. If no expiration date is specified, the coupon never expires.

* **Coupon Type:** Two types are supported:

  * `Fixed Amount`
  * `Percentage`

  Additional behavior:

  1. Percentage coupons work regardless of the selected currency.
  2. Fixed-amount coupons are valid only for the currencies they were configured for.
  3. If a coupon fully covers the order total, the customer can complete the purchase without making a payment.

### 🔎 User Search

* Users can be searched from **👥 Users → 🔎 Search** using either their Telegram ID or an internal UUID such as `019f3e33-19df-77de-8988-cb332e54e35d`.
* For a found user, administrators can:

  * assign a new role (Super Administrators only);
  * credit account balances;
  * view the user's complete order history.

### 📢 Broadcast Messaging

* Broadcasts can be sent in all three supported languages simultaneously. Users receive only the version matching their selected language.
* **Media:** One media attachment is supported.
* **Buttons:** The close button can be disabled, and custom URL buttons can be added.

### ⚙️ General Settings

* **Maintenance Mode:** Enabled by default. While active, regular users cannot use the bot and will receive a maintenance notice.
* **Support Contacts:** Configured contact information is displayed in the `ℹ️ Information` menu.

### 💳 Payment Systems

* The payment system from @CryptoBot is supported.
* Each payment provider can be enabled or disabled independently.
* A separate processing fee can be configured for each payment provider.
