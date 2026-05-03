import urllib.request
import random
import base64
import ssl

# Отключаем проверку SSL, чтобы не было ошибок рукопожатия
context = ssl._create_unverified_context()

# Свежие и "чистые" источники (без Farah и прочих)
urls = [
    "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
    "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless",
    "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt",
    "https://raw.githubusercontent.com/Epodonios/v2ray-configs/main/vless.txt"
]

all_nodes = []

# Мощный заголовок, чтобы GitHub не блокировал скрипт
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}

print("Запуск глубокого сканирования источников...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20, context=context) as response:
            raw_content = response.read().decode('utf-8').strip()
            
            # Пробуем декодировать Base64 (некоторые источники зашифрованы)
            if "vless://" not in raw_content[:100]:
                try:
                    content = base64.b64decode(raw_content).decode('utf-8')
                except:
                    content = raw_content
            else:
                content = raw_content
            
            # Собираем узлы и убираем рекламу
            nodes = []
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('vless://'):
                    # Фильтруем Farah, OneClick и другие рекламные метки
                    bad_words = ["Farah", "oneclick", "vpnkeys", "v2FreeHub"]
                    if not any(word.lower() in line.lower() for word in bad_words):
                        nodes.append(line)
            
            all_nodes.extend(nodes)
            print(f"ОК: {url.split('/')[-2]} -> Найдено: {len(nodes)}")
    except Exception as e:
        print(f"Ошибка на источнике {url}: {e}")

# Убираем дубликаты
vless_nodes = list(set(all_nodes))
random.shuffle(vless_nodes)

# Ограничиваем до 300
final_nodes = vless_nodes[:300]

# Сохраняем в файл чистым текстом
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Успех! В файл записано {len(final_nodes)} серверов.")
