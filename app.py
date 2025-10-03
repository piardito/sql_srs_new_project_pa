# pylint: disable=missing-module-docstring
# pylint: disable=consider-using-with
# pylint: disable=unspecified-encoding
# pylint: disable=exec-used
# pylint: disable=broad-exception-caught
# pylint: disable=line-too-long
# import pandas as pd
import logging
import os
# import numpy as np
from datetime import date, timedelta

import duckdb as db
import streamlit as st

st.markdown(
    """
    <style>
    
    /* Sidebar */
    [data-testid="stSidebar"] {
    background-color: #e0f7fa; /* fond clair */
    border-right: 2px solid #d1d5db; /* bordure droite */
    padding: 1.5rem;
    border-radius: 0 12px 12px 0;
    }
    
    [data-testid="stAppViewContainer"] {
    background-color: #f0f4f8;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Ctext x='0' y='40' font-size='18' fill='rgba(93,109,126,0.15)' font-family='Roboto' transform='rotate(-45 0 40)'%3ESQL%3C/text%3E%3Ctext x='0' y='120' font-size='18' fill='rgba(93,109,126,0.15)' font-family='Roboto' transform='rotate(-45 0 120)'%3ESQL%3C/text%3E%3C/svg%3E");
    background-repeat: repeat;
    }
    
    /* Import Roboto */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    :root {
        --mozart-bg: #f0f4f8;
        --mozart-card: #ffffff;
        --mozart-primary: #5d6d7e;
        --mozart-secondary: #9aa5b1;
        --mozart-accent: #f6d186;
        --mozart-hover: #d3e0ea;
        --mozart-border: #d1d5db;
    }

    /* Global */
    body, textarea, input, select, button, .stDataFrame th, .stDataFrame td {
        font-family: 'Roboto', sans-serif !important;
        color: var(--mozart-primary);
    }

    body {
        background-color: var(--mozart-bg);
    }

    /* Main container */
    .main {
        padding: 2rem 3rem;
    }

    /* Titles */
    h1, h2, h3 {
        color: var(--mozart-primary);
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    h1 { font-size: 2.5rem; }
    h2 { font-size: 2rem; }
    h3 { font-size: 1.5rem; }

    /* Textarea */
    textarea {
        width: 100% !important;
        padding: 0.8rem !important;
        border-radius: 10px !important;
        border: 2px solid var(--mozart-border) !important;
        background-color: var(--mozart-card) !important;
        transition: all 0.2s ease;
    }

    textarea:focus {
        outline: none !important;
        border-color: var(--mozart-accent) !important;
        box-shadow: 0 0 8px rgba(246,209,134,0.4);
        background-color: var(--mozart-hover) !important;
    }

    /* Selectbox */
    div.stSelectbox > div > div {
        border: 2px solid var(--mozart-border) !important;
        border-radius: 10px !important;
        background-color: var(--mozart-card) !important;
        padding: 0.08rem 0.5rem !important;
        color: var(--mozart-primary) !important;
    }

    /* Texte de la sélection */
    div.stSelectbox div.css-1hwfws3 { /* classe interne générée par Streamlit */
        font-family: 'Roboto', sans-serif !important;
        color: var(--mozart-primary) !important;
    }

    /* Dropdown list hover */
    div.stSelectbox div[role="listbox"] div[role="option"]:hover {
        background-color: var(--mozart-accent) !important;
        color: var(--mozart-primary) !important;
    }

    /* Button */
    .stButton>button {
        background-color: #ffffff !important;
        color: var(--mozart-primary) !important;
        padding: 0.6rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #9aa5b1 !important;
    }

    /* DataFrame stylisé avec contour */
    .stDataFrame table {
    width: 100%;
    border-collapse: collapse;
    border: 2px solid #5d6d7e; /* contour principal */
    background-color: #ffffff;
    border: 2px solid #5d6d7e;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }

    /* Cellules */
    .stDataFrame th, .stDataFrame td {
    padding: 0.75rem 1rem;
    text-align: left;
    border-bottom: 1px solid #d1d5db;
    }

    /* Header */
    .stDataFrame th {
    background-color: #d3e0ea;
    font-weight: 600;
    }

   /* Hover sur les lignes */
   .stDataFrame tr:hover {
    background-color: #f6d186;
    transition: all 0.2s ease;
    }

    /* Scroll horizontal si nécessaire */
    .stDataFrame div[role="table"] {
    overflow-x: auto;
     }
    </style>
    """,
    unsafe_allow_html=True,
)


if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

st.markdown("# Exercices sur SQL")

con = db.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

df = con.execute("SELECT * FROM memory_state").df()

print(df)

query = st.text_area("Text")

with st.sidebar:
    Themes = st.selectbox("Choisi le thème", df["Theme"].unique())
    numero_questions = st.selectbox(
        "Choisi le numéro de la question", df["NumeroQuestion"].unique()
    )
    questions = st.write(
        f"Question  {numero_questions} : ",
        df[
            (df["Theme"] == Themes)
            & (
                df["NumeroQuestion"] == numero_questions
            )  # ici c'est un entier, pas une string
        ]["Question"],
    )

requete = df[(df["Theme"] == Themes) & (df["NumeroQuestion"] == numero_questions)][
    "Reponse"
].values[0]
st.markdown("## Resultat attendue")
response = con.execute(f"{requete}").df()
st.dataframe(response)

st.markdown("## Votre réponse")
try:
    if query is not None:
        user_reponse = con.execute(query).df()[response.columns.to_list()]
        st.dataframe(user_reponse)

except Exception as e:
    st.error(f"la requete n'est pas correcte ou vide {e}")


expander = st.expander("regarde la requete attendue")
expander.write(requete)


try:
    if user_reponse is not None:
        st.markdown(f"## La réponse à la question est {user_reponse.equals(response)}")
        if user_reponse.equals(response) is True:
            st.write("## Bravo!!!")
        else:
            st.write("Recommence, tu vas y arriver")
        st.write("## Différences")
        st.dataframe(user_reponse.compare(response))

except Exception as e:
    st.error(
        f"Il n'y a rien ou la syntaxe est incorrecte ou la requete n'est pas correcte {e}"
    )


for n_days in [2, 7, 21]:
    st.write("Double cliquez pour changer la date")
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET LastReviewed = '{next_review}' WHERE Theme = '{Themes}' and NumeroQuestion ='{numero_questions}'"
        )

st.write("Double cliquez pour Reset")
if st.button("Reset"):
    con.execute("UPDATE memory_state SET LastReviewed = '1970-01-01'")

with st.sidebar:
    st.dataframe(
        df[(df["Theme"] == Themes) & (df["NumeroQuestion"] == numero_questions)][
            ["Tables", "LastReviewed"]
        ]
    )


tables = df["Tables"].values[0].split(",")
for table in tables:
    st.write(f"table : {table}")
    df_table = con.execute(f"SELECT * FROM {table}").df()
    st.dataframe(df_table)
