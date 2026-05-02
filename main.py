import urllib.request, base64, os

def main():
    urls = [
        "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless",
        "https://raw.githubusercontent.com/Paimon-v2ray/Paimon-VLESS-Reality/main/v2ray.txt",
        "https://raw.githubusercontent.com/RealSreN/Free-V2ray-Config/main/Splited/vless.txt"
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
                    # ОСТАВЛЯЕМ ТОЛЬКО VLESS. Если в строке есть trojan или vmess - удаляем.
                    if line.startswith('vless://') and 'trojan' not in line.lower() and 'vmess' not in line.lower():
                        nodes.append(line)
        except: continue
    if nodes:
        nodes = list(dict.fromkeys(nodes))
        eu_keys = ['germany', 'de', 'netherlands', 'nl', 'poland', 'pl', 'frankfurt', 'amsterdam']
        eu_nodes = [n for n in nodes if any(k in n.lower() for k in eu_keys)]
        other_nodes = [n for n in nodes if n not in eu_nodes]
        final_list = (eu_nodes + other_nodes)[:100]
        res = base64.b64encode("\n".join(final_list).encode()).decode()
        
        # ВОТ ТУТ Я ПОМЕНЯЛ ИМЯ ФАЙЛА НА SUB.TXT
        os.makedirs("configs", exist_ok=True)
        with open("configs/sub.txt", "w") as f: f.write(res)

if __name__ == "__main__": main()
