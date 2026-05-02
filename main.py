import urllib.request
import random
import base64

# Источники, где названия стран обычно подписаны
urls = [
    "https://raw.githubusercontent.com/m-reza-m/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/AzadNet/V2ray-Configs/main/Vless_Configs.txt",
    "https://raw.githubusercontent.com/Leon-K-One/VPN/main/VLESS.txt",
    "https://raw.githubusercontent.com/SadeghHoseini/v2ray-config/main/VLESS.txt",
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64"
]

all_nodes = []
# Заголовок, чтобы сайты думали, что зашел человек из браузера
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

print("Начинаю сбор серверов...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8').strip()
            
            # Проверка на base64 (если в файле каша, пробуем расшифровать)
            if not content.startswith('vless://'):
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            
            nodes = [n.strip() for n in content.split('\n') if n.strip()]
            all_nodes.extend(nodes)
            print(f"Успех! Загружено из {url}: {len(nodes)} шт.")
    except Exception as e:
        print(f"Ошибка на источнике {url}")

# Фильтруем только VLESS и убираем повторы
vless_nodes = list(set([n for n in all_nodes if n.startswith('vless://')]))

# Перемешиваем и берем 300 штук
random.shuffle(vless_nodes)
final_nodes = vless_nodes[:300]

with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Собрано серверов: {len(final_nodes)}")
