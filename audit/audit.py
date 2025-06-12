import json, hashlib
from pathlib import Path

votes = Path("vote/urne.jsonl").read_text().splitlines()

print("🔎 Audit des bulletins...")
for i, line in enumerate(votes):
    try:
        b = json.loads(line)
        if "hash" not in b or "vote_chiffre" not in b:
            print(f"❌ Ligne {i+1} : bulletin incomplet, ignoré.")
            continue
        recalculated = hashlib.sha256(b["vote_chiffre"].encode()).hexdigest()
        if recalculated != b["hash"]:
            print(f"❌ Ligne {i+1} : hash invalide.")
        else:
            print(f"✅ Ligne {i+1} : hash OK ({recalculated[:8]}...)")
    except Exception as e:
        print(f"❌ Ligne {i+1} : erreur ({e})")
