[繁體中文](README_zh-TW.md)

## Table of Contents

  - [Project Structure](#project-structure)
  - [About](#about)
  - [Configuration](#configuration)
  - [Installation](#installation)
  - [Development Philosophy](#development-philosophy)
  - [Commands](#commands)

## Project Structure

```text
discord-bot
├─ .dockerignore
├─ bot.py                               # Main entry point
├─ cogs                                 # Command modules (Cogs)
│  ├─ Advanced_Subjects_Test_calculate
│  │  └─ cog.py
│  ├─ ping
│  │  └─ cog.py
│  ├─ problem_report
│  │  └─ cog.py
│  └─ weather
│     └─ cog.py
├─ compose.debug.yaml
├─ compose.yaml                         # Docker Compose config
├─ core
│  └─ classes.py                        # Shared logic & base classes
├─ Dockerfile                           # Container definition
├─ location.json                        # Weather location data
└─ requirements.txt                     # Python dependencies
```

## About

A personal utility bot designed to simplify daily tasks and gaming calculations:

  * **HSR Damage Calculator**: Precise direct damage estimation for Honkai: Star Rail.
  * **Academic Tools**: Scoring calculations for the Advanced Subjects Test (AST).
  * **Weather Service**: Real-time weather data for specific localized areas.
  * **System Diagnostics**: Real-time status and problem reporting.

## Configuration

The bot requires the following **Environment Variables** to function. Create a `.env` file in the root directory:

```env
# Discord Bot Token
TOKEN=your_discord_bot_token

# Developer's Discord User ID
AUTHORIZED_USER_ID=your_discord_id

# CWA Weather API Key (Apply at: https://opendata.cwa.gov.tw/user/authkey)
api_key=your_api_key

# Target Channel ID for problem reports
REPORT_CHANNEL_ID=your_report_channel_id
```


> **Security Note:** Always add `.env` to your `.gitignore` to avoid leaking sensitive credentials.

## Development Philosophy

This project is **strictly passion-driven**. Features are implemented exclusively at the developer's whim—I build what I want, when I want.

> **Note:** If you're looking for a roadmap, there isn't one. It's just me and my vibes.

## Installation

Click the link below to authorize the bot to your account (User Install):

👉 [**Install Bot to My Account**](https://discord.com/oauth2/authorize?client_id=1332233736053592115&response_type=code&redirect_uri=https%3A%2F%2Fdiscord.com%2Fchannels%2F%40me%2F1332256421894557750&integration_type=1&scope=applications.commands+dm_channels.messages.read)

## Commands

  * `/ast_calculate`: Calculate the highest score for the Advanced Subjects Test.
  * `/check_online`: Verify the bot's current status.
  * `/get_server_ip`: Retrieve the bot's host IP (Restricted to Developer).
  * `/problem_report`: Submit bug reports or feedback.
  * `/weather_location_select`: Get weather updates for preset locations.
  * `/hsr_direct_damage_calculate`: HSR damage estimation (Work in progress).