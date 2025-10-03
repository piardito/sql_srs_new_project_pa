# pylint: disable=missing-module-docstring
# pylint: disable=unused-import
# pylint: disable=broad-exception-caught
import duckdb
import streamlit as st

from app import app_page
from login import login_page
from users import conn  # <-- on réutilise la connexion existante

# Initialisation
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "email" not in st.session_state:
    st.session_state.email = ""

if not st.session_state.authenticated:
    login_page()
else:
    app_page()

    with st.sidebar:
        st.markdown("---")
        st.markdown("## Gestion des utilisateurs (admin/test)")

        try:
            # On utilise la connexion existante

            if st.session_state.email:
                st.markdown(f"### Utilisateur connecté : `{st.session_state.email}`")
                user_info = conn.execute(
                    "SELECT id,email FROM users WHERE email = ?",
                    (st.session_state.email,),
                ).fetchdf()
                st.write(user_info)

        except Exception as e:
            st.error(f"Erreur lors de l'accès à la base users : {e}")
