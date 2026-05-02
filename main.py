import urllib.request
import random
import base64

# Источники, которые сейчас лучше всего работают в РФ (Reality + VLESS)
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt",
    "https://raw.githubusercontent.com/BardiaFA/Free-V2ray-Config/main/Splitted-By-Protocol/VLESS.txt",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless"
]

all_nodes = []
headers = {'User-Agent': 'v2rayNG/1.9.1'}

print("Сбор прокси для обхода блокировок...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            raw_content = response.read().decode('utf-8').strip()
            
            # Пробуем расшифровать Base64, если это не прямые ссылки
            if not raw_content.startswith('vless://'):
                try:
                    content = base64.b64decode(raw_content).decode('utf-8')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            # Вытаскиваем только vless
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            all_nodes.extend(nodes)
            print(f"Загружено из {url}: {len(nodes)}")
    except Exception as e:
        print(f"Ошибка на {url}")

# Удаляем дубликаты и перемешиваем
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)

# Берем 300 штук
final_nodes = vless_nodes[:300]

# Записываем ЧИСТЫМ ТЕКСТОМ (NekoBox так лучше видит)
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Успех! В файле ultra_sub.txt теперь {len(final_nodes)} прокси.")
