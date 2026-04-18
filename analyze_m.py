import json
import re
from collections import Counter

def extract_month(date_str):
    """
    從各種格式的日期字串中提取月份
    """
    if not date_str or date_str == "未取得":
        return "未知月份"
    
    # 使用正規表示式 (Regex) 找尋數字
    # 邏輯：尋找 "年" 後面的數字，或是第一個 "/" 與第二個 "/" 之間的數字
    
    # 格式 1: 2026年05月31日 -> 抓 "年" 後面的數字
    match_year_month = re.search(r'年\s*(\d{1,2})\s*月', date_str)
    if match_year_month:
        return f"{int(match_year_month.group(1))}月"

    # 格式 2: 2026/05/31 -> 抓中間的數字
    match_slash = re.findall(r'\d+', date_str)
    if match_slash:
        # 如果有三個數字 (年/月/日)，月份通常是第二個
        if len(match_slash) >= 2:
            # 判斷第一個數字是否為年份 (4位數)，如果是，取第二個當月份
            if len(match_slash[0]) == 4:
                return f"{int(match_slash[1])}月"
            # 如果第一個數字就是月份 (例如 5/09)
            else:
                return f"{int(match_slash[0])}月"

    return "未知月份"

def run_month_analysis(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        months = []
        for event in data:
            raw_time = event.get("活動時間", "未取得")
            month = extract_month(raw_time)
            months.append(month)

        # 統計次數
        month_counts = Counter(months)

        # 排序：依照月份 1-12 月排序 (而非次數)
        # 定義排序順序
        order = [f"{i}月" for i in range(1, 13)] + ["未知月份"]
        sorted_months = sorted(month_counts.items(), key=lambda x: order.index(x[0]) if x[0] in order else 99)

        print("\n" + "="*40)
        print(f"{'活動月份':<15} | {'活動場次':<5}")
        print("-" * 40)
        
        for m, count in sorted_months:
            if count > 0:
                print(f"{m:<15} | {count:<5}")
            
        print("="*40)
        print(f"統計完成：分析了 {len(data)} 筆活動時間。")

    except FileNotFoundError:
        print(f"❌ 找不到檔案 '{filename}'")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

if __name__ == "__main__":
    run_month_analysis('aaa.json')
