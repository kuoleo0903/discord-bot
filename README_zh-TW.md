[English](README.md)

## 目錄

  - [專案結構](#專案結構)
  - [關於本專案](#關於本專案)
  - [環境變數設定](#環境變數設定)
  - [安裝方式](#安裝方式)
  - [開發理念](#開發理念)
  - [指令列表](#指令列表)

## 專案結構

```text
discord-bot
├─ .dockerignore
├─ bot.py                               # 程式主入口
├─ cogs                                 # 指令模組 (Cogs)
│  ├─ Advanced_Subjects_Test_calculate
│  │  └─ cog.py
│  ├─ ping
│  │  └─ cog.py
│  ├─ problem_report
│  │  └─ cog.py
│  └─ weather
│     └─ cog.py
├─ compose.debug.yaml
├─ compose.yaml                         # Docker Compose 配置文件
├─ core
│  └─ classes.py                        # 核心邏輯與基底類別
├─ Dockerfile                           # 容器定義檔
├─ location.json                        # 天氣地區對照表
└─ requirements.txt                     # Python 依賴清單
```

## 關於本專案

這是一個為了簡化日常任務與遊戲計算而設計的個人工具機器人：

  * **崩鐵傷害計算機**：精確估算《崩壞：星穹鐵道》的直傷數據。
  * **算分工具**：分科測驗 (AST) 最高分數計算。
  * **天氣服務**：提供特定地區的即時天氣資訊。
  * **系統診斷**：即時狀態檢查與問題回報功能。

## 環境變數設定

本機器人需要以下環境變數方可運作。請在根目錄建立 `.env` 檔案：

```env
# Discord Bot 認證 Token
TOKEN=your_discord_bot_token

# 開發者 Discord ID
AUTHORIZED_USER_ID=your_discord_id

# 氣象局 API Key (請至 https://opendata.cwa.gov.tw/user/authkey 申請)
api_key=your_api_key

# 問題回報預設頻道 ID
REPORT_CHANNEL_ID=your_report_channel_id
```

請將location_example.json改你要的地區

> **安全提醒：** 務必將 `.env` 加入 `.gitignore` 中，以免洩漏敏感憑證。

## 開發理念

本專案**純粹由興趣驅動**。功能開發完全取決於開發者的心情與需求——我只在我想要的時間，做我想做的功能。

> **註：** 這裡沒有開發路線圖（Roadmap）。

## 安裝方式

點擊下方連結將機器人安裝至你的個人帳號（使用者安裝）：

👉 [**安裝機器人至個人帳號**](https://discord.com/oauth2/authorize?client_id=1332233736053592115&response_type=code&redirect_uri=https%3A%2F%2Fdiscord.com%2Fchannels%2F%40me%2F1332256421894557750&integration_type=1&scope=applications.commands+dm_channels.messages.read)

## 指令列表

  * `/ast_calculate`: 分科測驗最高分數計算。
  * `/check_online`: 查看機器人目前是否在線。
  * `/get_server_ip`: 查詢 Bot 所在主機 IP (僅限開發者使用)。
  * `/problem_report`: 提交問題回報或建議。
  * `/weather_location_select`: 查詢預設地點之天氣。
  * `/hsr_direct_damage_calculate`: 崩鐵直傷計算（持續更新中）。