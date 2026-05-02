import urllib.request
import random
import base64
import re

# Самые стабильные источники с флагами и странами
urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/mohmousavi73/v2ray-configs/main/VLESS.txt",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt"
]

all_nodes = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("Запуск финальной сборки...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8').strip()
            
            # Пробуем расшифровать, если это base64
            if not content.startswith('vless://'):
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            
            nodes = [n.strip() for n in content.split('\n') if n.strip()]
            all_nodes.extend(nodes)
            print(f"ОК: {url} (Найдено: {len(nodes)})")
    except:
        print(f"Ошибка доступа к источнику")

# Убираем дубликаты и оставляем только VLESS
vless_nodes = list(set([n for n in all_nodes if n.startswith('vless://')]))

# Перемешиваем и ограничиваем до 300
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Успех! Собрано серверов: {len(final_nodes)}")
