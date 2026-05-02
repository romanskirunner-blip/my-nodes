import urllib.request, base64, os

def main():
    # Прямые ссылки на VLESS/Reality конфиги
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/RealSreN/Free-V2ray-Config/main/Splited/vless.txt"
    ]
    
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
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
                    # ЖЕСТКИЙ ФИЛЬТР: Только vless, и НИКАКИХ троянов внутри строки
                    if line.startswith('vless://') and 'trojan' not in line.lower():
                        nodes.append(line)
        except: continue
    
    if nodes:
        nodes = list(dict.fromkeys(nodes)) # Удаляем дубликаты
        
        # Приоритет на Германию, Нидерланды и Польшу
        eu_keys = ['germany', 'de', 'netherlands', 'nl', 'poland', 'pl', 'frankfurt', 'amsterdam']
        eu_nodes = [n for n in nodes if any(k in n.lower() for k in eu_keys)]
        other_nodes = [n for n in nodes if n not in eu_nodes]
        
        # Собираем 100 лучших
        final_list = (eu_nodes + other_nodes)[:100]
        
        res = base64.b64encode("\n".join(final_list).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w") as f: f.write(res)

if __name__ == "__main__": main()
