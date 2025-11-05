# 💼 WalletMint – 自動化建立代理 / 商戶與驗證流程

本專案提供完整的自動化流程，用於批次建立代理與商戶帳號，
同時驗證所有設定檔內容、API 流程與錯誤碼回傳。
所有模組皆可獨立執行與測試，並支援 CLI 參數控制除錯輸出。

---

## ⚡ 快速開始（Quick Start）
```bash
# 1️⃣ 切換到專案目錄
cd WalletMint

# 2️⃣ 建立虛擬環境（Windows）
python -m venv venv

# 3️⃣ 啟用虛擬環境
venv\Scripts\activate

# 4️⃣ 安裝套件依賴
pip install -r requirements.txt

# ✅ 執行主控制器（預設 debug 模式）
python main.py controller main --debug

# ❌ 關閉除錯輸出
python main.py controller main --no-debug
```

## 📦 專案流程概觀
```bash
1. 讀取系統設定（.env）
2. 讀取名稱設定檔（.csv / .env / .json）
3. 組合 Context（COMMON + INDEX + API）
4. 呼叫 OPS 控制器執行批次新增與查詢作業
5. 任務模組回傳非 SUCCESS (ResultCode != 0) 時會立即中止流程。
```

## 🧱 設定檔說明
```bash
workspace/profiles/examples/profile_spec.yml
```

## 🧩 錯誤碼比對方式
```bash
錯誤碼定義於：
workspace/config/error_code.py

執行時若顯示：
❌ 任務失敗 ResultCode = 2031

請開啟 error_code.py 搜尋：
task_email_invalid_format = 2031  # 信箱格式錯誤

若錯誤與設定檔內容或欄位格式有關，
請同時參考：
workspace/profiles/examples/profile_spec.yml
```

## 🧠 偵錯與除錯建議
```bash
想看完整流程輸出：使用 --debug
只想驗證設定檔格式：使用 --step 1
執行時出現錯誤碼：到 workspace/config/error_code.py 搜尋代碼
設定檔欄位錯誤或格式異常：參考 workspace/profiles/examples/profile_spec.yml
```

## 🧪 測試內容
```bash
測試指令：
pytest -m "unit and tool and loader" -v
pytest -m "unit and task and loader" -v

測試覆蓋範圍：
工具層 (loader.py)：驗證 .env / .csv / .json、錯誤格式與權限處理
任務層：load_system_context_task、load_profile_context_task、assemble_context_task
整合測試：驗證三任務串接產生完整 Context
錯誤碼覆蓋：所有任務錯誤碼皆有對應測試案例 ✅
覆蓋率：100% 錯誤碼命中率
```

## 🧱 專案結構
```bash
workspace/
 ├─ tools/loader/
 │   └─ loader.py
 ├─ tasks/loader/
 │   ├─ load_system_context_task.py
 │   ├─ load_profile_context_task.py
 │   └─ assemble_context_task.py
 ├─ controllers/
 │   ├─ main_controller.py
 │   └─ ops_controller.py
 ├─ config/
 │   ├─ error_code.py
 │   └─ paths.py
 └─ profiles/
     ├─ names.csv                （客戶實際使用，僅允許一份）
     └─ examples/
         ├─ names_example.csv
         ├─ names_example.env
         ├─ names_example.json
         └─ profile_spec.yml     （設定檔規範說明文件）
```

## ⚠️ 注意事項

```bash
- .xlsx 格式已移除支援，請改用 .csv（Excel 可直接開啟）
- workspace/profiles/ 資料夾內僅允許一份設定檔
- modetype 僅允許 1（手續費）或 2（月租費）
- 若新增任務模組或錯誤碼，請同步更新 error_code.py 與測試檔
- 若修改設定檔欄位或規範，請同步更新 profile_spec.yml
```

## 📄 版權宣告
© 2025 WalletMint Automation Framework