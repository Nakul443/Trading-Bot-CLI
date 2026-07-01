# Trading Bot CLI

A command-line cryptocurrency trading bot built in Python that places orders on the **Binance Futures Testnet**. The project follows a modular architecture where each component has a single responsibility, making the codebase easy to understand, extend, and maintain.

> **Note:** This bot is configured for the Binance Futures Testnet only. No real funds are used.

---

# Features

- Command-line interface using Click
- Supports both **MARKET** and **LIMIT** orders
- Input validation before making API requests
- Secure API credential management using environment variables
- Modular architecture with clear separation of concerns
- Logging to both terminal and log file
- Error handling for Binance API and network failures

---

# Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.x | Programming Language |
| Click | Command Line Interface |
| python-binance | Binance Futures API SDK |
| python-dotenv | Environment Variable Management |
| Logging | Debugging and Monitoring |

---

# Project Architecture

The project follows a layered architecture.

```
                User

                  │
                  ▼

          Command Line (cli.py)

                  │
                  ▼

     Input Validation (validators.py)

                  │
                  ▼

     Order Execution (orders.py)

                  │
                  ▼

 Authentication Layer (client.py)

                  │
                  ▼

 Binance Futures Testnet API
```

---

# How Everything Connects

The execution flow is as follows:

```
User

 │

 ▼

cli.py
 │
 │ Parses CLI arguments
 │ Displays order summary
 │
 ▼

validators.py
 │
 │ Validates symbol
 │ Validates order type
 │ Validates quantity
 │ Validates price
 │
 ▼

orders.py
 │
 │ Builds Binance request
 │ Handles exceptions
 │
 ▼

client.py
 │
 │ Loads .env
 │ Creates authenticated Binance client
 │
 ▼

Binance Futures Testnet

```

Logging is available throughout every layer of the application.

```
Every Module
      │
      ▼
logging_config.py
      │
      ▼
 bot.log
```

---

# Folder Structure

```
Trading-Bot-CLI/
│
├── bot/
│   ├── __init__.py
│   ├── cli.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

# File Breakdown

## bot/

Contains all application logic.

---

### cli.py

Entry point of the application.

Responsibilities:

- Parses command-line arguments
- Displays order summary
- Calls input validation
- Calls order execution
- Displays success/error messages

Think of it as the controller of the application.

---

### validators.py

Acts as the application's validation layer.

Responsibilities:

- Normalize inputs
- Validate trading symbol
- Validate order side
- Validate order type
- Validate quantity
- Validate limit price

If validation fails, execution stops before contacting Binance.

---

### orders.py

Contains the core business logic.

Responsibilities:

- Requests authenticated Binance client
- Builds Binance API payload
- Sends order request
- Handles Binance API exceptions
- Logs requests and responses

This file is responsible for communicating with Binance.

---

### client.py

Responsible for authentication.

Responsibilities:

- Loads environment variables
- Reads API Key
- Reads Secret Key
- Creates Binance client
- Connects to Binance Futures Testnet

No business logic exists here.

---

### logging_config.py

Central logging configuration.

Creates two logging handlers:

### Console Logger

Displays clean messages to the user.

Example

```
INFO: Sending order...
ERROR: Invalid quantity
```

### File Logger

Stores detailed debugging information.

Example

```
Timestamp
Module Name
Log Level
Message
```

Logs are written to

```
bot.log
```

---

### __init__.py

Marks the directory as a Python package.

---

# Root Files

## requirements.txt

Contains all project dependencies.

```
python-binance
python-dotenv
click
```

---

## .env.example

Template for storing API credentials.

Example

```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_secret_key
```

Copy this file and rename it to

```
.env
```

before running the application.

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>

cd Trading-Bot-CLI
```

---

## 2. Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Copy

```
.env.example
```

Rename it to

```
.env
```

Add your Binance Futures Testnet credentials.

```
BINANCE_API_KEY=YOUR_API_KEY
BINANCE_API_SECRET=YOUR_SECRET_KEY
```

---

# Running the Application

## Market Order

```bash
python -m bot.cli \
--symbol BTCUSDT \
--side BUY \
--order-type MARKET \
--quantity 0.001
```

---

## Limit Order

```bash
python -m bot.cli \
--symbol BTCUSDT \
--side SELL \
--order-type LIMIT \
--quantity 0.001 \
--price 65000
```

---

# Logging

The application generates logs in

```
bot.log
```

Logs include

- API requests
- Validation failures
- Successful trades
- API responses
- Network errors
- Authentication failures

---

# Error Handling

The application safely handles

- Missing API credentials
- Invalid order parameters
- Invalid quantity
- Invalid price
- Missing limit price
- Binance API exceptions
- Authentication failures
- Network failures

---

# Design Principles

The project follows several software engineering best practices:

- Separation of Concerns (each module has a single responsibility)
- Modular Architecture
- Defensive Input Validation
- Environment-based Configuration
- Centralized Logging
- Structured Error Handling
- Reusable Components

---

# Future Improvements

Possible enhancements include:

- Stop Loss orders
- Take Profit orders
- OCO orders
- Position management
- Trade history
- Balance checking
- WebSocket price streaming
- Strategy engine
- Unit tests
- Docker support
- Configuration file support
- CI/CD pipeline
- Support for multiple exchanges

---

# Disclaimer

This project is intended for educational purposes and uses the Binance Futures Testnet. Always test trading strategies in a simulated environment before deploying them to a live trading account.
