import urllib.request
import random

# Источники, которые лучше всего обходят блокировки и всегда полны прокси
urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/coldwater-10/clash_vless/main/vless.txt",
    "https://raw.githubusercontent.com/M-reza7/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/Paimon-V2ray/Paimon-V2ray-Config/main/Proxy.txt",
    "https://raw.githubusercontent.com/V2Ray-VLESS/VLESS-Configs/main/Splitted-By-Protocol/vless.txt"
]

all_nodes = []
headers = {'User-Agent': 'v2rayNG/1.8.5'}

print("Начинаю сбор прокси...")

for url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8').strip()
            
            # Разбиваем на строки и ищем только рабочие vless ссылки
            lines = content.split('\n')
            nodes = [n.strip() for n in lines if n.startswith('vless://')]
            
            if nodes:
                all_nodes.extend(nodes)
                print(f"ОК: {url} (Найдено: {len(nodes)})")
            else:
                print(f"Источник {url} пуст или формат не тот")
    except:
        print(f"Не удалось подключиться к {url}")

# Убираем дубликаты
vless_nodes = list(set(all_nodes))

# Перемешиваем для свежести
random.shuffle(vless_nodes)

# Берем 300 самых свежих
final_nodes = vless_nodes[:300]

# Сохраняем как ЧИСТЫЙ ТЕКСТ (без Base64), так NekoBox точно увидит прокси
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(final_nodes))

print(f"---")
print(f"Успех! В файл записано {len(final_nodes)} прокси.")
