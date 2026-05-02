import urllib.request
import random
import base64

urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/mohmousavi73/v2ray-configs/main/VLESS.txt",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt"
]

all_nodes = []
headers = {'User-Agent': 'Mozilla/5.0'}

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8').strip()
            if not content.startswith('vless://'):
                try: content = base64.b64decode(content).decode('utf-8')
                except: pass
            all_nodes.extend([n.strip() for n in content.split('\n') if n.strip()])
    except: continue

vless_nodes = list(set([n for n in all_nodes if n.startswith('vless://')]))
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

# ВОТ ТУТ ГЛАВНОЕ ИЗМЕНЕНИЕ: кодируем всё в одну строку Base64
subscription_data = "\n".join(final_nodes)
encoded_data = base64.b64encode(subscription_data.encode('utf-8')).decode('utf-8')

with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write(encoded_data)

print(f"Собрано и закодировано серверов: {len(final_nodes)}")
