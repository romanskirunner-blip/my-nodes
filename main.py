import urllib.request
import random
import base64
import ssl
import time

# Игнорируем любые проблемы с сертификатами
ctx = ssl._create_unverified_context()

# Список источников через зеркала и прямые агрегаторы
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/ts-sf/fly/main/v2"
]

all_nodes = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

print("Запуск экстренного поиска серверов...")

for url in urls:
    try:
        print(f"Пробую: {url.split('/')[-2 if 'base64' in url else -1]}")
        req = urllib.request.Request(url, headers=headers)
        
        # Добавляем небольшую паузу между запросами, чтобы GitHub не банил
        time.sleep(1) 
        
        with urllib.request.urlopen(req, timeout=20, context=ctx) as response:
            raw_content = response.read().decode('utf-8', errors='ignore').strip()
            
            # Если контент подозрительно короткий - пропускаем
            if len(raw_content) < 10:
                continue

            # Расшифровка, если это Base64
            if "vless://" not in raw_content[:50]:
                try:
                    # Убираем лишние пробелы/символы перед декодом
                    content = base64.b64decode(raw_content).decode('utf-8', errors='ignore')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            
            # Фильтруем рекламу (Farah, OneClick и т.д.)
            clean_nodes = [n for n in nodes if not any(x in n.lower() for x in ["farah", "oneclick", "vpnkeys", "v2free"])]
            
            all_nodes.extend(clean_nodes)
            print(f"Успешно! Найдено: {len(clean_nodes)}")
            
    except Exception as e:
        print(f"Не удалось получить данные из этого источника")

# Если вообще ничего не собралось, добавим один резервный "железный" источник
if not all_nodes:
    print("Внимание: основные источники подвели, пробую резервный...")
    # (Здесь можно добавить еще одну ссылку, если нужно)

# Убираем дубли, мешаем и берем 300
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

# Записываем результат
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"ИТОГО: в ультра_саб записано {len(final_nodes)} прокси.")

