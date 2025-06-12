import json
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

ca_key = serialization.load_pem_private_key(
    Path("authority/ca_key.pem").read_bytes(), password=None
)

# Liste d'électeurs autorisés (id uniquement)
electeurs = ["voter1", "voter2", "voter3"]
data = {
    "electeurs": electeurs
}

payload = json.dumps(data, sort_keys=True).encode()
signature = ca_key.sign(payload, padding.PKCS1v15(), hashes.SHA256())

data["signature"] = signature.hex()
Path("electeurs.json").write_text(json.dumps(data, indent=2))
print("✅ Liste électorale signée générée.")
