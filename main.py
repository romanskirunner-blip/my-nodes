import urllib.request
import random

# Источники с самым высоким шансом обхода блокировок в РФ
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/PeimanH/Vless-Configs/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/m-reza-m/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Zizifusi/v2ray-configs/main/vless.txt"
]

all_nodes = []
headers = {'User-Agent': 'v2rayNG/1.9.1'} # Новая версия агента

print("Начинаю сбор 'бронебойных' конфигов...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8').strip()
            
            # Если в источнике Base64 (как у yebekhe), декодируем его
            import base64
            if not content.startswith('vless://'):
                try:
                    content = base64.b64decode(content).decode('utf-8')
                except:
                    pass
            
            nodes = [n.strip() for n in content.split('\n') if n.startswith('vless://')]
            all_nodes.extend(nodes)
            print(f"Загружено: {len(nodes)} из {url}")
    except:
        print(f"Пропуск источника")

# Убираем повторы
vless_nodes = list(set(all_nodes))

# Перемешиваем
random.shuffle(vless_nodes)

# Берем 300 штук
final_nodes = vless_nodes[:300]

# Сохраняем чистым текстом для NekoBox
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Готово! Собрано {len(final_nodes)} серверов.")
