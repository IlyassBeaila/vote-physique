import json
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

votes = Path("vote/urne.jsonl").read_text().splitlines()
results = {}
bureau = "75001"
for v in votes:
    clear_vote = json.loads(v)["vote_chiffre"][::-1]
    results[clear_vote] = results.get(clear_vote, 0) + 1

# Générer l’export
export = {
    "bureau": bureau,
    "resultats": results
}

payload = json.dumps(export, sort_keys=True).encode()

# Signature par la CA
ca_key = serialization.load_pem_private_key(
    Path("authority/ca_key.pem").read_bytes(), password=None
)
signature = ca_key.sign(payload, padding.PKCS1v15(), hashes.SHA256())
export["signature"] = signature.hex()

Path("resultats_signes.json").write_text(json.dumps(export, indent=2))
print("✅ Résultats exportés et signés.")
