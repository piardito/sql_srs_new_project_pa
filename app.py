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
        df[(df["Theme"] == Themes) & (df["NumeroQuestion"] == numero_questions)]
    )


tables = df["Tables"].values[0].split(",")
for table in tables:
    st.write(f"table : {table}")
    df_table = con.execute(f"SELECT * FROM {table}").df()
    st.dataframe(df_table)
