"""
Module de gestion des utilisateurs pour l'application Streamlit avec DuckDB et Pydantic.

Fonctionnalités :
- Gestion d'une base d'utilisateurs (DuckDB)
- Validation des emails avec Pydantic (EmailStr)
- Hachage sécurisé des mots de passe en SHA-256
- Vérification d'authentification
"""

import hashlib

import duckdb
from pydantic import BaseModel, EmailStr, ValidationError

# Connexion à la base de données DuckDB
conn = duckdb.connect("users.duckdb")

# Création de la table si elle n'existe pas
conn.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT,
    email VARCHAR UNIQUE,
    password VARCHAR
)
"""
)


class User(BaseModel):
    """
    Modèle d'utilisateur validé par Pydantic.

    Attributs
    ---------
    email : EmailStr
        Adresse email valide de l'utilisateur.
    password : str
        Mot de passe en clair (sera haché avant stockage).
    """

    email: EmailStr
    password: str


def hash_password(password: str) -> str:
    """
    Génère un hash SHA-256 à partir d'un mot de passe.

    Paramètres
    ----------
    password : str
        Mot de passe en clair.

    Retour
    ------
    str
        Mot de passe haché en SHA-256 (hexadécimal).
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    Vérifie si un mot de passe correspond à son hash SHA-256.

    Paramètres
    ----------
    password : str
        Mot de passe en clair.
    hashed : str
        Mot de passe haché stocké en base.

    Retour
    ------
    bool
        True si correspondance, False sinon.
    """
    return hash_password(password) == hashed


def add_user(email: str, password: str) -> bool:
    """
    Ajoute un nouvel utilisateur dans la base de données.

    Paramètres
    ----------
    email : str
        Adresse email de l'utilisateur (sera validée par Pydantic).
    password : str
        Mot de passe en clair (sera haché avant insertion).

    Retour
    ------
    bool
        True si l'utilisateur est ajouté avec succès,
        False si l'email est invalide ou déjà utilisé.
    """
    try:
        # Validation email avec Pydantic
        user = User(email=email, password=password)

        # Génération manuelle de l'ID incrémenté
        last_id = (
            conn.execute("SELECT COALESCE(MAX(id), 0) FROM users").fetchone()[0] + 1
        )
        hashed_pw = hash_password(user.password)

        conn.execute(
            "INSERT INTO users (id, email, password) VALUES (?, ?, ?)",
            (last_id, user.email, hashed_pw),
        )
        return True

    except ValidationError:
        # Email invalide
        return False
    except Exception as e:
        if "unique" in str(e).lower():
            return False  # Email déjà existant
        raise


def verify_user(email: str, password: str) -> bool:
    """
    Vérifie les identifiants d'un utilisateur.

    Paramètres
    ----------
    email : str
        Adresse email de l'utilisateur.
    password : str
        Mot de passe en clair à vérifier.

    Retour
    ------
    bool
        True si les identifiants sont corrects, False sinon.
    """
    result = conn.execute(
        "SELECT password FROM users WHERE email = ?", (email,)
    ).fetchone()
    if result:
        return verify_password(password, result[0])
    return False
