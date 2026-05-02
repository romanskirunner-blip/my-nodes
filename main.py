import urllib.request

# Прямые ссылки на подписки
urls = [
    "https://raw.githubusercontent.com/barry-far/V2ray-config/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/ebrasha/free-v2ray-public-list/main/vless_configs.txt",
    "https://raw.githubusercontent.com/SoliSpirit/v2ray-configs/main/all_configs.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/sevcator/5ubscrpt10n/main/protocols/vl.txt"
]

all_nodes = []

for url in urls:
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            nodes = data.strip().split('\n')
            all_nodes.extend(nodes)
    except Exception as e:
        print(f"Ошибка при загрузке {url}: {e}")

# Убираем дубликаты и пустые строки
unique_nodes = list(set([n for n in all_nodes if n.strip()]))

# Сохраняем в файл
with open("ultra_sub.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(unique_nodes))

print(f"Готово! Собрано серверов: {len(unique_nodes)}")
