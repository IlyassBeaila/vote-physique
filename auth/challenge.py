import os, json
from pathlib import Path
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from datetime import datetime
# Charger le certificat
cert = json.loads(Path("register/voter1_cert.json").read_text())
pubkey = serialization.load_pem_public_key(cert["pubkey"].encode())

# Vérifie la plage horaire 8h–20h
heure = datetime.now().hour
if not (8 <= heure < 20):
    print("⛔ Vote refusé : en dehors de la plage horaire (8h–20h).")
    exit(1)

# Vérifie que l'électeur est bien inscrit sur la liste électorale
electeurs = json.loads(Path("register/electeurs.json").read_text())
if cert["id"] not in electeurs["electeurs"]:
    print("❌ ID non inscrit sur la liste électorale.")
    exit(1)
# Vérifier procuration
mandats = json.loads(Path("register/mandats.json").read_text())
mandataire = mandats.get(cert["id"])
if mandataire:
    print(f"📩 Vous votez en procuration pour : {mandataire}")
    cert["id"] = mandataire

# Challenge
challenge = os.urandom(16)
print("🔐 Challenge généré :", challenge.hex())

privkey = serialization.load_pem_private_key(
    Path("register/voter1_key.pem").read_bytes(), password=None
)

signature = privkey.sign(challenge, padding.PKCS1v15(), hashes.SHA256())

try:
    pubkey.verify(signature, challenge, padding.PKCS1v15(), hashes.SHA256())
except:
    print("❌ Échec d’authentification.")
    exit(1)

# Vérifie s’il a déjà voté
voted_path = Path("register/voted_ids.json")
voted_ids = json.loads(voted_path.read_text() or "[]")

if cert["id"] in voted_ids:
    print("⚠️ Cet électeur a déjà voté.")
    exit(1)

# Ajoute à la liste
voted_ids.append(cert["id"])
voted_path.write_text(json.dumps(voted_ids))

print("✅ Authentification réussie.")
