import json
import csv
from urllib import request

def get_data(url):
    with request.urlopen(url) as response:
        data = response.read()
    return data

def save_attraction_csv(data, attraction_csv):
    # 解析 JSON 資料
    attractions = json.loads(data)["result"]["results"]
    # 創建 CSV 檔案並寫入資料
    with open(attraction_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["景點名稱", "區域", "經度", "緯度", "第一張圖檔網址"])
        for attraction in attractions:
            name = attraction.get('stitle')
            region = attraction.get('address').split("  ")[1][0:3]
            longitude = attraction.get('longitude')
            latitude = attraction.get('latitude')
            image_url = attraction.get('file').split("https://")[1]
            writer.writerow([name, region, longitude, latitude, "https://"+image_url])

def save_mrt_csv(data, mrt_csv):
    attractions = json.loads(data)["result"]["results"]
    group_by_region = {}
    for attraction in attractions:
        name = attraction.get('stitle')
        region = attraction.get('MRT') or "None"
        try:
            group_by_region[region].append(name)
        except:
            group_by_region[region] = [name]
    # print(group_by_region.items())

    with open(mrt_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        header = ['捷運站名稱'] + [f'景點名稱{i}' for i in range(1, len(max(group_by_region.values(), key=len))+1)]
        writer.writerow(header)
        for region, attractions in group_by_region.items():
            writer.writerow([region] + attractions)

if __name__ == "__main__":
    url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
    attraction_csv = "attraction.csv"
    mrt_csv = "mrt.csv"
    data = get_data(url)
    save_attraction_csv(data, attraction_csv)
    save_mrt_csv(data, mrt_csv)
