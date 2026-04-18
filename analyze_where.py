import json
from collections import Counter

def clean_venue_name(name):
    """
    此函式負責將多種不同的寫法歸類為同一個場館名稱
    """
    if not name or name == "未取得" or name == "未標註地點":
        return "未知/未取得"
    
    # 先轉為大寫並去掉前後空白
    n = name.upper().strip()
    
    # --- 歸類邏輯開始 ---
    if "WESTAR" in n:
        return "WESTAR"
    
    if "高雄流行音樂中心" in n:
        return "高雄流行音樂中心"
    
    if "LEGACY TERA" in n:
        return "Legacy TERA"
    
    if "LEGACY TAIPEI" in n:
        return "Legacy Taipei"
    
    if "HANASPACE" in n or "花漾展演空間" in n:
        return "HANASPACE (花漾展演空間)"
        
    if "THE WALL" in n:
        return "The Wall Live House"
    # --- 歸類邏輯結束 ---

    return name  # 若不符合上述規則，則維持原樣

def run_analysis(filename):
    try:
        # 1. 讀取資料
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 2. 提取並清洗地點資料
        cleaned_venues = []
        for event in data:
            raw_location = event.get("地點", "未標註地點")
            # 執行歸類函式
            final_name = clean_venue_name(raw_location)
            cleaned_venues.append(final_name)

        # 3. 統計次數
        venue_stats = Counter(cleaned_venues)

        # 4. 排序 (依照次數從大到小)
        sorted_stats = sorted(venue_stats.items(), key=lambda x: x[1], reverse=True)

        # 5. 印出整齊的表格
        print("\n" + "="*50)
        print(f"{'場館名稱 (已歸類)':<35} | {'活動場次':<5}")
        print("-" * 50)
        
        for name, count in sorted_stats:
            print(f"{name:<35} | {count:<5}")
            
        print("="*50)
        print(f"總計分析了 {len(data)} 筆活動，歸類出 {len(venue_stats)} 個場館。")

    except FileNotFoundError:
        print(f"❌ 找不到檔案 '{filename}'，請確認它是否在同一個資料夾。")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")

# 程式啟動
if __name__ == "__main__":
    run_analysis('檔案')
