import json
from collections import Counter

def run_promoter_analysis(filename):
    try:
        # 1. 讀取 JSON 檔案
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        all_promoters = []
        for event in data:
            # 取得主辦單位欄位，若無則標記為未知
            raw_p = event.get("主辦單位", "未知").strip()
            
            # 資料清洗：處理多家主辦的情況
            # 1. 將換行符號取代為逗號，統一分隔符
            p_clean = raw_p.replace('\n', '、')
            
            # 2. 依照「、」拆分，只取第一家作為「主要主辦」
            # (如果你想統計所有參與的公司，可以把 split 之後的結果用 extend 加進清單)
            main_promoter = p_clean.split('、')[0].split(' ')[0]
            
            all_promoters.append(main_promoter)

        # 2. 統計各主辦單位出現次數
        p_counts = Counter(all_promoters)

        # 3. 依照場次從多到少排序
        sorted_p = sorted(p_counts.items(), key=lambda x: x[1], reverse=True)

        # 4. 印出結果表格
        print("\n" + "="*50)
        print(f"{'主辦單位 (主要)':<30} | {'活動場次':<5}")
        print("-" * 50)
        
        for name, count in sorted_p:
            # 限制名稱長度避免破壞表格格式
            display_name = (name[:28] + '..') if len(name) > 28 else name
            print(f"{display_name:<30} | {count:<5}")
            
        print("="*50)
        print(f"統計完成：共分析了 {len(data)} 筆資料，發現 {len(p_counts)} 家主辦單位。")

    except FileNotFoundError:
        print(f"❌ 找不到檔案 '{filename}'")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

# 執行程式
if __name__ == "__main__":
    run_analysis_file = '檔案'
    run_promoter_analysis(run_analysis_file)
