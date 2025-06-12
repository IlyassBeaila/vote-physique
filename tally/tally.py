import json
from pathlib import Path

votes = Path("vote/urne.jsonl").read_text().splitlines()
counts = {}

for v in votes:
    clear_vote = json.loads(v)["vote_chiffre"][::-1]
    counts[clear_vote] = counts.get(clear_vote, 0) + 1
validators = json.loads(Path(__file__).parent.joinpath("tally_validators.json").read_text())
if list(validators["signatures"].values()).count("OK") < 2:
    print("❌ Le dépouillement est bloqué : signatures manquantes.")
    exit(1)

print("🧮 Résultats :")
for k, v in counts.items():
    print(f"  {k} : {v} vote(s)")
