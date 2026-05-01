import urllib.request, base64, os
SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2Ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]
def main():
    nodes = set()
    for url in SOURCES:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                text = r.read().decode('utf-8')
                try:
                    if "://" not in text: text = base64.b64decode(text).decode('utf-8')
                except: pass
                for line in text.splitlines():
                    if line.startswith(('vless://','ss://','trojan://')): nodes.add(line.strip())
        except: continue
    if nodes:
        out = base64.b64encode("\n".join(list(nodes)[:150]).encode()).decode()
        os.makedirs("configs", exist_ok=True)
        with open("configs/list.txt", "w") as f: f.write(out)
if __name__ == "__main__":
    main()
