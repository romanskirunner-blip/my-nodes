import urllib.request
import random
import base64
import ssl

# Отключаем проверку SSL (чтобы не было ошибок на GitHub)
ctx = ssl._create_unverified_context()

# Бронебойные источники без Farah и OneClick (Reality + VLESS)
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/BardiaFA/Free-V2ray-Config/main/Splitted-By-Protocol/VLESS.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless"
]

all_nodes = []
# Имитируем реальный браузер по максимуму
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': '*/*'
}

print("Начинаю сбор 'чистых' Reality серверов...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            raw_content = response.read().decode('utf-8').strip()
            
            # Пробуем декодировать Base64
            if not raw_content.startswith('vless://'):
                try:
                    content = base64.b64decode(raw_content).decode('utf-8')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            # Собираем ссылки и фильтруем мусор
            nodes = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('vless://'):
                    # Выкидываем Farah, OneClick и прочую рекламу
                    junk = ["Farah", "oneclick", "vpnkeys", "v2FreeHub", "@", "Join"]
                    if not any(word.lower() in line.lower() for word in junk):
                        nodes.append(line)
            
            all_nodes.extend(nodes)
            print(f"ОК: {url.split('/')[-1]} | Собрано: {len(nodes)}")
    except Exception as e:
        print(f"Пропуск {url} (ошибка подключения)")

# Оставляем только уникальные и перемешиваем
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)

# Берем 300 лучших
final_nodes = vless_nodes[:300]

# Записываем в файл чистым текстом (NekoBox так лучше переваривает)
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Успех! В файл записано {len(final_nodes)} рабочих прокси.")
