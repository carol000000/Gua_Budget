import json
import os

# 1. 讀取舊的記帳檔案
if os.path.exists("budget.json"):
    try:
        with open("budget.json", "r", encoding="utf-8") as f:
            records = json.load(f)
    except json.JSONDecodeError:
        records = []
else:
    records = []

print(f"=== 歡迎回來！目前已紀錄了 {len(records)} 筆消費 ===")
print("('x' 存檔離開）\n('q'查詢)\n('n'記帳)")

# 2. 開啟無限循環，直到你不想記為止
while True:
    date = input("功能:")
    
    # 防呆機制：如果你輸入 q，就跳出迴圈，準備存檔
    if date.lower() == 'x':
        break

    if date.lower() == 'q':
        q_type = input("[查詢模式] 輸入想查詢的年份或月份\n(年份輸入'y')(月份輸入'd'): ")
        if q_type.lower() == 'y':
                q_year = input("請輸入想查詢的【年份】(例如 2026): ")
                print(f"\n--- 以下是 {q_year} 年的查詢結果 ---")
            
                q_total = 0
                found_any = False
                for r in records:
                # 檢查這筆日期的「前 4 個字」是不是等於輸入的年份
                    if r["日期"][:4] == q_year:
                        print(f"{r['日期']} | {r['項目']} | {r['金額']} 元")
                        q_total += r["金額"]
                        found_any = True
            
                if not found_any:
                    print(f"沒有找到 {q_year} 年的紀錄。")
                else:
                    print("-----------------------------------------")
                    print(f"{q_year} 年總共花費： {q_total} 元")
                print("-----------------------------------------\n")

        elif q_type.lower() == 'd':
                q_mon = input("請輸入想查詢【哪一年】的【月份】(例如 2025-05): ")
                print(f"\n--- 以下是 {q_mon} 月的查詢結果 ---")
            
                q_total = 0
                found_any = False
                for r in records:
                # 如果你的日期格式是 20260524，月份會在第 5,6 個字 (也就是索引 4:6)
                # 如果你記帳時只打 4 位數 0524，月份就是前兩個字 [:2]
                # 這裡我們用最安全的「包含檢查」：
                    if q_mon in r["日期"]:
                        print(f"{r['日期']} | {r['項目']} | {r['金額']} 元")
                        q_total += r["金額"]
                        found_any = True
            
                if not found_any:
                    print(f"沒有找到 {q_mon} 月的紀錄。")
                else:
                    print("-----------------------------------------")
                    print(f"{q_mon} 月總共花費： {q_total} 元")
                print("-----------------------------------------\n")
            
        else:
                print("輸入錯誤！請輸入 'y' 或 'd'。")
            
                continue # 查詢完畢，回到主選單
       
    if date.lower() == 'n': 
        day = input("請輸入日期(xxxx-xx-xx): ")
        item = input("請輸入消費項目: ")
        amount = int(input("請輸入花費金額: "))

        # 3. 把這一筆新資料打包
        new_record = {
            "日期": day,
            "項目": item,
            "金額": amount
        }

        # 4. 塞進清單裡
        records.append(new_record)
        print("【已暫存】成功加入一筆，繼續下一筆...\n")

#--------------------------------------------------------------------

# 5. 當你打 x 跳出迴圈後，才會來到這一步：一次性存檔
with open("budget.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=4)

print("\n【系統提示】所有資料已寫入 budget.json")

# 6. 計算並輸出總花費
total_spend = 0
print("\n--- 目前所有消費明細 ---")
for r in records:
    print(f"{r['日期']} | {r['項目']} |  {r['金額']} 元")
    total_spend = total_spend + r['金額']

print("-----------------------")
print(f"總共累計花費： {total_spend} 元")