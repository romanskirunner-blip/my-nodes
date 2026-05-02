import urllib.request, base64, os

def main():
    # Только источники с чистым VLESS
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/mansorid/free-v2ray-config/main/sub.txt",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt"
    ]
    
    nodes = []
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
                    # СТРОЖАЙШИЙ ФИЛЬТР: оставляем ТОЛЬКО vless
                    if line.startswith('vless://'):
                        nodes.append(line)
        except: continue
    
    if nodes:
        # Убираем дубликаты
        nodes = list(dict.fromkeys(nodes))
        
        # Фильтр по Европе (Германия, Нидерланды, Польша)
        eu_keywords = ['germany', 'de', 'netherlands', 'nl', 'poland', 'pl', 'frankfurt', 'amsterdam', 'warsaw']
        
        eu_nodes = [n for n in nodes if any(key in n.lower() for key in eu_keywords)]
        other_nodes = [n for n in nodes if n not in eu_nodes]
        
        # Сначала Европа, потом всё остальное до лимита 100 (чтобы не было мусора)
        final_list = (eu_nodes + other_nodes)[:100]
        
        res = base64.b64encode("\n".join(final_list).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w") as f: f.write(res)

if __name__ == "__main__": main()
