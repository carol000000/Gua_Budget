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
print("('x' 存檔離開）\n('q'查詢)\n('n'記帳)\n('e'查詢目前所有資訊)\n('d'刪除資料)")

# 2. 開啟無限循環，直到你不想記為止
while True:
    date = input("功能:")
    
    # 就跳出迴圈，準備存檔
    if date.lower() == 'x':
        break

#------------------查詢------------------------
if date.lower() == 'q':
    q_type = input("[查詢模式] 輸入想查詢的日期\n(xxxx 或 xxxx-xx 或 xxxx-xx-xx): ")
    print(f"\n--- 以下是 {q_type} 的查詢結果 ---")
        
    q_total = 0
    found_any = False
    for r in records:
        # 【修正點】使用 startswith() 代替 ==，這樣就能做到前方一致的模糊查詢
        if r["日期"].startswith(q_type):
            print(f"{r['日期']} | {r['項目']} | {r['金額']} 元")
            q_total += r['金額']
            found_any = True
        
        if not found_any:
            print(f"沒有找到符合「{q_type}」的紀錄。")
        else:
            print("-----------------------------------------")
            print(f"{q_type} 總共花費： {q_total} 元")
        print("-----------------------------------------\n")
        continue # 查詢完畢，回到主選單

#------------------記帳--------------------------------       
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
        

#----------------------查看所有------------------------------------    
    if date.lower() == 'e':
        total_spend = 0
        print("\n--- 目前所有消費明細 ---")
        for r in records:
            print(f"{r['日期']} | {r['項目']} |  {r['金額']} 元")
            total_spend = total_spend + r['金額']

        print("-----------------------")
        print(f"總共累計花費： {total_spend} 元")
        

#--------------------------刪除-------------------------------    
    if date.lower() == 'd':
        while True:
            del_data = input("[刪除模式] 輸入想刪除的日期 (輸入 'x' 退出刪除模式): ")
            if del_data.lower() == 'x':
                print("已退出刪除模式。\n")
                break
 
            match_records = [] 

            for index, r in enumerate(records):
                if r["日期"] == del_data: 
                    # 這裡一樣可以保留 index，方便未來的其他擴充
                    match_records.append((index, r))
            
            # 如果沒找到任何紀錄，直接重新詢問日期
            if not match_records:
                print(f"\n--- 沒有找到 {del_data} 的紀錄 ---")
                print("-----------------------------------------\n")
                continue

            # 印出當天所有紀錄，並加上編號
            print(f"\n--- 以下是 {del_data} 的所有紀錄 ---")
            for i, (original_index, r) in enumerate(match_records):
                print(f"[{i + 1}] {r['項目']} | {r['金額']} 元")
            print("-----------------------------------------")
    
            choice = input("請輸入想刪除的【項目編號】(輸入任意鍵取消): ")
    
            try:
                choice_idx = int(choice) - 1
                # 關鍵防呆：確保 choice_idx 沒有變成負數（例如輸入 0 會變成 -1 抓到最後一筆）
                if choice_idx < 0:
                    raise IndexError
                
                target_data = match_records[choice_idx][1]
            
            except (ValueError, IndexError):
                print("\n【取消】輸入錯誤或取消")
            
            else:
                YN_del = input(f"確定要刪除「{target_data['項目']} {target_data['金額']}元」嗎？(Y/N): ")
        
                if YN_del.lower() == 'y':
                    # 【核心修正】改用 remove 直接刪除物件內容，避開索引位移的地雷！
                    records.remove(target_data)
                    print(f"\n【成功】已刪除該筆紀錄")
                else:
                    print("\n【取消】已取消刪除操作")
        
            print("-----------------------------------------\n")
            # 刪除完一筆後，會回到刪除模式的開頭，讓你可以繼續輸入日期或輸入 'x' 離開
            continue

#--------------------------------------------------------------------

# 5. 當你打 x 跳出最外層迴圈後，才會來到這一步：一次性存檔
with open("budget.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=4)

print("\n【系統提示】所有資料已寫入 budget.json")