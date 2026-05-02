import urllib.request, base64, os

def main():
    # Список только лучших VLESS источников
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/RealSreN/Free-V2ray-Config/main/Splited/vless.txt"
    ]
    
    # Метка-проверка
    nodes = ["vless://check@1.1.1.1:443?encryption=none&security=reality#VPN_WORKS_100_PERCENT"]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                d = r.read().decode('utf-8')
                if "://" not in d:
                    try: d = base64.b64decode(d).decode('utf-8')
                    except: pass
                for line in d.splitlines():
                    line = line.strip()
                    # Строгий фильтр: ТОЛЬКО vless
                    if line.startswith('vless://') and 'trojan' not in line.lower():
                        nodes.append(line)
        except: continue
    
    if len(nodes) > 1:
        # Убираем дубликаты и берем топ-100
        res = base64.b64encode("\n".join(list(dict.fromkeys(nodes))[:100]).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        # НОВОЕ ИМЯ ФАЙЛА
        with open("configs/ultra.txt", "w", encoding="utf-8") as f:
            f.write(res)
        print("Done! ultra.txt created.")

if __name__ == "__main__":
    main()
