import json
import random
import hashlib
from pathlib import Path

# Obtenir le chemin absolu du dossier contenant ce script
base_dir = Path(__file__).resolve().parent

# Lire la liste des candidats
candidats_path = base_dir / "candidats.json"
if not candidats_path.exists():
    print("❌ Fichier 'candidats.json' introuvable.")
    exit(1)

candidats = json.loads(candidats_path.read_text())["candidats"]

# Afficher la liste
print("🗳️ Candidats disponibles :")
for i, nom in enumerate(candidats):
    print(f"{i + 1}. {nom}")

# Choix de l'utilisateur
choix = input("Entrez le numéro de votre choix : ")
try:
    index = int(choix) - 1
    if index < 0 or index >= len(candidats):
        raise ValueError()
except:
    print("❌ Choix invalide.")
    exit(1)

# Vote sélectionné
vote = candidats[index]
vote_chiffre = vote[::-1]  # chiffrement simulé
hash_vote = hashlib.sha256(vote_chiffre.encode()).hexdigest()

# Simulation de signature de cercle
anneau = ["voter1", "voter2", "voter3"]
signataire = random.choice(anneau)

bulletin = {
    "vote_chiffre": vote_chiffre,
    "hash": hash_vote,
    "ring": anneau,
    "signataire_simule": f"{signataire} (anonyme)",
    "signature_de_cercle": "ring-signature-simulee"
}

# Enregistrer le bulletin dans l’urne
urne_path = base_dir / "urne.jsonl"
with open(urne_path, "a") as f:
    f.write(json.dumps(bulletin) + "\n")

print(f"✅ Vote enregistré anonymement dans l’urne. Hash : {hash_vote[:10]}…")
