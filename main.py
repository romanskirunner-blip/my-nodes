import urllib.request
import base64
import random
import ssl
import re

# Настройка "невидимости" для GitHub
def get_proxies():
    # Отключаем все проверки безопасности, которые мешают сбору
    ctx = ssl._create_unverified_context()
    
    # Репозитории-тяжеловесы (Reality, VLESS, No-Ads)
    sources = [
        "https://raw.githubusercontent.com/yebekhe/TVC/main/subscriptions/vless/base64",
        "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity",
        "https://raw.githubusercontent.com/BardiaFA/Free-V2ray-Config/main/Splitted-By-Protocol/VLESS.txt",
        "https://raw.githubusercontent.com/NiREAs/v2ray-collector/main/sub/vless",
        "https://raw.githubusercontent.com/LalatinaHub/Mineral/master/vless.txt"
    ]
    
    all_vless = []
    
    # Заголовки, имитирующие последний Chrome на Windows 11
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://github.com/'
    }

    for url in sources:
        try:
            print(f"Штурмуем: {url}")
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                data = resp.read().decode('utf-8', errors='ignore').strip()
                
                # Если это Base64, ломаем его
                if not data.startswith('vless://'):
                    try:
                        # Убираем возможный мусор по краям для чистого декода
                        data = base64.b64decode(data + "==").decode('utf-8', errors='ignore')
                    except:
                        pass
                
                # Ищем все, что похоже на vless ссылки через регулярные выражения
                found = re.findall(r'vless://[^\s]+', data)
                
                # Жёсткий фильтр: удаляем Farah, OneClick и прочую рекламную чепуху
                clean = [link for link in found if not any(bad in link.lower() for bad in ["farah", "oneclick", "vpnkeys", "v2free"])]
                
                all_vless.extend(clean)
                print(f"Захвачено: {len(clean)} серверов")
        except Exception as e:
            print(f"Источник временно недоступен, идем дальше...")

    # Чистка дублей и перемешивание колоды
    unique_vless = list(set(all_vless))
    random.shuffle(unique_vless)
    
    # Отбираем 300 самых сочных конфигов
    final_list = unique_vless[:300]
    
    # Сохраняем в файл чистым текстом (так NekoBox понимает лучше всего)
    with open("ultra_sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(final_list))
    
    print("-" * 30)
    print(f"ИТОГ: В ультра_саб загружено {len(final_list)} серверов!")

if __name__ == "__main__":
    get_proxies()
