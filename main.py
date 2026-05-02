import urllib.request
import random
import base64
import ssl

# Игнорируем ошибки SSL
context = ssl._create_unverified_context()

# Новые источники: только свежие агрегаторы без Farah/OneClick
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless",
    "https://raw.githubusercontent.com/m-reza-m/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Zizifusi/v2ray-configs/main/vless.txt"
]

all_nodes = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Сбор 'чистых' источников...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20, context=context) as response:
            raw_content = response.read().decode('utf-8').strip()
            
            # Авто-декодирование Base64
            if "vless://" not in raw_content[:50]:
                try:
                    content = base64.b64decode(raw_content).decode('utf-8')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            # Фильтруем только vless и отсеиваем мусор
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            
            # Дополнительный фильтр: убираем Farah и OneClick, если они вдруг просочились
            clean_nodes = [n for n in nodes if "Farah" not in n and "oneclick" not in n]
            
            all_nodes.extend(clean_nodes)
            print(f"Загружено из {url}: {len(clean_nodes)}")
    except Exception as e:
        print(f"Пропуск {url}")

# Убираем дубликаты
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)

# Берем 300 штук
final_nodes = vless_nodes[:300]

with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Готово! В файле {len(final_nodes)} серверов без лишнего мусора.")
