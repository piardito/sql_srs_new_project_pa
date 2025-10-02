# import io
# pylint: disable=missing-module-docstring
# pylint: disable=line-too-long
from datetime import datetime, timedelta

import duckdb as db
import numpy as np
import pandas as pd

con = db.connect(database="data/exercises_sql_tables.duckdb")

TABLES = "commandes,clients,produits"
LAST_REVIEWED = "1970-01-01"

questions_sql = {
    "Filtres simples": {
        "1": [
            (
                "Quels sont les clients qui habitent à Paris ?",
                "SELECT * FROM clients WHERE ville = 'Paris';",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "2": [
            (
                "Quels produits coûtent plus de 500 € ?",
                "SELECT * FROM produits WHERE prix > 500;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "3": [
            (
                "Quels clients ont moins de 30 ans ?",
                "SELECT * FROM clients WHERE age < 30;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "4": [
            (
                "Quels produits appartiennent à la catégorie 'Informatique' ?",
                "SELECT * FROM produits WHERE categorie = 'Informatique';",
                TABLES,
                LAST_REVIEWED,
            )
        ],
    },
    "Agrégations": {
        "1": [
            (
                "Quel est le chiffre d'affaires total de toutes les commandes ?",
                "SELECT SUM(c.quantite * p.prix) AS total_ventes FROM commandes c JOIN produits p ON c.produit_id = p.produit_id;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "2": [
            (
                "Combien de commandes a passé chaque client ?",
                "SELECT client_id, COUNT(*) as nb_commandes FROM commandes GROUP BY client_id ORDER BY client_id;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "3": [
            (
                "Quelle est la dépense totale de chaque client ?",
                "SELECT cl.nom, SUM(c.quantite * p.prix) AS depense_totale FROM commandes c JOIN clients cl ON c.client_id = cl.client_id JOIN produits p ON c.produit_id = p.produit_id GROUP BY cl.nom;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "4": [
            (
                "Quel produit a été vendu en plus grande quantité ?",
                "SELECT p.nom_produit, SUM(c.quantite) AS total_vendu FROM commandes c JOIN produits p ON c.produit_id = p.produit_id GROUP BY p.nom_produit ORDER BY total_vendu DESC LIMIT 1;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
    },
    "Jointures": {
        "1": [
            (
                "Liste des clients avec les produits qu’ils ont achetés",
                "SELECT cl.nom,pr.produit_id,pr.nom_produit FROM commandes co JOIN clients cl ON co.client_id = cl.client_id JOIN produits pr ON co.produit_id = pr.produit_id",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "2": [
            (
                "Quels sont les clients qui ont acheté un Laptop ?",
                "SELECT DISTINCT cl.nom FROM commandes co JOIN clients cl ON co.client_id = cl.client_id JOIN produits pr ON co.produit_id = pr.produit_id WHERE pr.nom_produit = 'Laptop' ORDER BY cl.nom DESC;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "3": [
            (
                "Quels produits ont été commandés par les clients de Lyon ?",
                "SELECT DISTINCT p.nom_produit FROM commandes c JOIN clients cl ON c.client_id = cl.client_id JOIN produits p ON c.produit_id = p.produit_id WHERE cl.ville = 'Lyon';",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "4": [
            (
                "Donne le nombre total d’unités achetées par produit",
                "SELECT p.nom_produit, SUM(c.quantite) AS total_unites FROM commandes c JOIN produits p ON c.produit_id = p.produit_id GROUP BY p.nom_produit;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
    },
    "Statistiques": {
        "1": [
            (
                "Quel est l’âge moyen des clients ?",
                "SELECT AVG(age) as age_moyen FROM clients;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "2": [
            (
                "Quelle ville compte le plus de clients ?",
                "SELECT ville, COUNT(*) as nb_clients FROM clients GROUP BY ville ORDER BY nb_clients DESC LIMIT 1;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "3": [
            (
                "Quel est le prix moyen des produits par catégorie ?",
                "SELECT categorie, AVG(prix) as prix_moyen FROM produits GROUP BY categorie;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
        "4": [
            (
                "Quel est le client le plus âgé et ce qu’il a commandé ?",
                "SELECT cl.nom, DENSE_RANK()  OVER(ORDER BY age DESC) as rang, p.nom_produit FROM clients cl JOIN commandes c ON cl.client_id = c.client_id JOIN produits p ON c.produit_id = p.produit_id QUALIFY rang = 1;",
                TABLES,
                LAST_REVIEWED,
            )
        ],
    },
}

rows = []
for theme, questions in questions_sql.items():
    for numero, data_list in questions.items():
        # chaque entrée est une liste contenant un tuple
        question, reponse, tables, last_reviewed = data_list[0]
        rows.append(
            {
                "Theme": theme,
                "NumeroQuestion": int(numero),
                "Question": question,
                "Reponse": reponse,
                "Tables": tables,
                "LastReviewed": last_reviewed,
            }
        )

df = pd.DataFrame(rows)

print(df.head())

con.execute("DROP TABLE IF EXISTS memory_state")
con.execute("CREATE TABLE memory_state AS SELECT * FROM df")


# ---------------------------
# Table Clients
# ---------------------------
clients = pd.DataFrame(
    {
        "client_id": range(1, 11),
        "nom": [
            "Alice",
            "Bob",
            "Charlie",
            "Diane",
            "Ethan",
            "Fatima",
            "George",
            "Hélène",
            "Ivan",
            "Julia",
        ],
        "ville": [
            "Paris",
            "Lyon",
            "Marseille",
            "Paris",
            "Toulouse",
            "Lille",
            "Lyon",
            "Nantes",
            "Bordeaux",
            "Paris",
        ],
        "age": [25, 34, 29, 40, 31, 27, 36, 22, 45, 30],
    }
)
con.execute("CREATE TABLE IF NOT EXISTS clients AS SELECT * FROM clients")

# ---------------------------
# Table Produits
# ---------------------------
produits = pd.DataFrame(
    {
        "produit_id": range(1, 6),
        "nom_produit": ["Laptop", "Smartphone", "Casque", "Clavier", "Souris"],
        "categorie": [
            "Informatique",
            "Informatique",
            "Audio",
            "Informatique",
            "Informatique",
        ],
        "prix": [1200, 800, 150, 100, 50],
    }
)

con.execute("CREATE TABLE IF NOT EXISTS produits AS SELECT * FROM produits")


# ---------------------------
# Table Commandes
# ---------------------------
np.random.seed(42)
commandes = pd.DataFrame(
    {
        "commande_id": range(1, 21),
        "client_id": np.random.choice(clients["client_id"], 20),
        "produit_id": np.random.choice(produits["produit_id"], 20),
        "quantite": np.random.randint(1, 5, 20),
        "date_commande": [
            datetime(2023, 1, 1) + timedelta(days=int(x))
            for x in np.random.randint(0, 365, 20)
        ],
    }
)

con.execute("CREATE TABLE IF NOT EXISTS commandes AS SELECT * FROM commandes")


con.close()
