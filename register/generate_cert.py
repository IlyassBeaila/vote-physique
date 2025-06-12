import json
from pathlib import Path
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

ca_key = serialization.load_pem_private_key(
    Path("authority/ca_key.pem").read_bytes(), password=None
)

user_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pubkey = user_key.public_key()

pub_pem = pubkey.public_bytes(
    serialization.Encoding.PEM,
    serialization.PublicFormat.SubjectPublicKeyInfo
).decode()

cert = {
    "id": "voter1",
    "pubkey": pub_pem,
    "bureau": "75001"
}

to_sign = json.dumps(cert, sort_keys=True).encode()
signature = ca_key.sign(to_sign, padding.PKCS1v15(), hashes.SHA256())
cert["signature"] = signature.hex()

Path("voter1_cert.json").write_text(json.dumps(cert, indent=2))

with open("voter1_key.pem", "wb") as f:
    f.write(user_key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.PKCS8,
        serialization.NoEncryption()
    ))

print("✅ Certificat et clé générés.")
