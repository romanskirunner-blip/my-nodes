import urllib.request
import random
import base64
import ssl

# Игнорируем проверку SSL
ctx = ssl._create_unverified_context()

# Используем зеркало 'jsDelivr', чтобы GitHub не блокировал запросы от ботов
urls = [
    "https://cdn.jsdelivr.net/gh/yebekhe/TVC@main/subscriptions/vless/base64",
    "https://cdn.jsdelivr.net/gh/mahdibland/V2RayAggregator@master/Eternity",
    "https://cdn.jsdelivr.net/gh/NiREAs/v2ray-collector@main/sub/vless",
    "https://cdn.jsdelivr.net/gh/SoliSpirit/v2ray-configs@main/all_configs.txt",
    "https://cdn.jsdelivr.net/gh/BardiaFA/Free-V2ray-Config@main/Splitted-By-Protocol/VLESS.txt"
]

all_nodes = []
headers = {'User-Agent': 'Mozilla/5.0'}

print("Запуск через зеркала для обхода блокировок GitHub...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20, context=ctx) as response:
            raw_content = response.read().decode('utf-8', errors='ignore').strip()
            
            # Если контент в Base64, декодируем
            if "vless://" not in raw_content[:50]:
                try:
                    content = base64.b64decode(raw_content).decode('utf-8', errors='ignore')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            # Собираем только VLESS, убираем Farah и OneClick
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            clean_nodes = [n for n in nodes if not any(x in n.lower() for x in ["farah", "oneclick", "vpnkeys"])]
            
            all_nodes.extend(clean_nodes)
            print(f"ОК: Получено {len(clean_nodes)} серверов")
    except Exception as e:
        print(f"Ошибка на зеркале {url}")

# Удаляем дубликаты и берем 300 штук
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

# Сохраняем результат
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"ФИНАЛ: В файл записано {len(final_nodes)} прокси.")
