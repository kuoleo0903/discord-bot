## 專案目錄
```
discord-bot
├─ .dockerignore
├─ bot.py
├─ cogs
│  ├─ Advanced_Subjects_Test_calculate
│  │  └─ cog.py
│  ├─ ping
│  │  └─ cog.py
│  ├─ problem_report
│  │  └─ cog.py
│  └─ weather
│     └─ cog.py
├─ compose.debug.yaml
├─ compose.yaml
├─ core
│  └─ classes.py
├─ Dockerfile
├─ location.json
└─ requirements.txt

```

## .env格式
```
# Discord Bot 的認證 Token
TOKEN=your_token

# 開發者ID
AUTHORIZED_USER_ID=123123123123123123

# 天氣api 請至 https://opendata.cwa.gov.tw/user/authkey 申請
api_key=your_api_key

# 要顯示回報問題的頻道ID
REPORT_CHANNEL_ID=123123123123123
```