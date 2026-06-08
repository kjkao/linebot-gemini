# linebot-gemini

## requirement
### line message API
https://developers.line.biz/
### python3.11
pip install flask
### line-bot-sdk
pip install line-bot-sdk<br>
https://pypi.org/project/line-bot-sdk/
### gemini
pip install google-genai<br>
https://pypi.org/project/google-genai/

## 如何取得 GEMINI API KEY
1. 前往 Google AI Studio 建立或登入帳號：<br>
	https://aistudio.google.com/
2. 到 API Keys 頁面建立金鑰：<br>
	https://aistudio.google.com/apikey
3. 複製新建立的 API Key。
4. 在執行環境設定環境變數 `GEMINI_API_KEY`。

### Linux / macOS
```bash
export GEMINI_API_KEY="你的_api_key"
```

### Windows PowerShell
```powershell
$env:GEMINI_API_KEY="你的_api_key"
```

> 建議：不要把 API Key 寫死在程式碼或提交到 Git。
