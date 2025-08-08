import os
base_path = "C:\\Projetos\\ProjetoDjango\\frontend"
for root, dirs, _ in os.walk(base_path):
    depth = root[len(base_path):].count(os.sep)
    if depth <= 2:  # 3 níveis (0 = raiz, 1 = subpasta, 2 = sub-subpasta)
        for d in dirs:
            print(f"📂 {os.path.join(root, d)}".replace(base_path, ""))
    if depth >= 2:
        dirs.clear()  # Limita a profundidade