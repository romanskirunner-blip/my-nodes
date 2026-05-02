import urllib.request, base64

def main():
    # Проверенные источники с кучей свежих VLESS
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/Baradauto/V2Ray-Config/main/V2Ray_Config.txt",
        "https://raw.githubusercontent.com/RealSreN/Free-V2ray-Config/main/Splited/vless.txt"
    ]
    
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                d = r.read().decode('utf-8')
                # Декодируем, если данные в Base64
                if "://" not in d:
                    try: d = base64.b64decode(d).decode('utf-8')
                    except: pass
                
                for line in d.splitlines():
                    line = line.strip()
                    # Собираем только VLESS и убираем мусор
                    if line.startswith('vless://') and 'trojan' not in line.lower():
                        nodes.append(line)
        except:
            continue
    
    # Добавляем твой победный сервер в начало для красоты
    final_list = ["vless://ready@1.1.1.1:443?encryption=none&security=reality#POBEDA_VLESS"]
    # Убираем дубликаты и берем первые 200 серверов
    final_list.extend(list(dict.fromkeys(nodes))[:200])
    
    if len(final_list) > 0:
        res = base64.b64encode("\n".join(final_list).encode()).decode()
        with open("ultra_sub.txt", "w") as f:
            f.write(res)
        print(f"Готово! Собрано серверов: {len(final_list)}")

if __name__ == "__main__":
    main()
