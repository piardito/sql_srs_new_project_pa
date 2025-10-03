# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=too-many-branches
import streamlit as st

from users import add_user, verify_user


def login_page():
    """
    Page de connexion et d'inscription pour l'application.
    - Permet à l'utilisateur de créer un compte (email validé + mot de passe confirmé)
    - Permet à l'utilisateur de se connecter si compte déjà existant
    - Sauvegarde l'état d'authentification dans `st.session_state`
    """

    # Initialisation de l'état de session
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "email" not in st.session_state:
        st.session_state.email = ""

    st.title("Authentification")

    # Choix entre login et inscription
    option = st.radio("Choisissez une action :", ["Se connecter", "Créer un compte"])

    # ----------------------
    # Création de compte
    # ----------------------
    if option == "Créer un compte":
        st.subheader("Créer un nouveau compte")
        email = st.text_input(
            "Email", key="signup_email", placeholder="exemple@domaine.com"
        )
        password = st.text_input(" Mot de passe", type="password", key="signup_pw")
        password_confirm = st.text_input(
            " Confirmer le mot de passe", type="password", key="signup_pw2"
        )

        if st.button("Créer mon compte"):
            if not email or not password:
                st.error(" Veuillez remplir tous les champs")
            elif password != password_confirm:
                st.error(" Les mots de passe ne correspondent pas !")
            elif add_user(email, password):
                st.success(
                    " Compte créé avec succès ! Vous pouvez maintenant vous connecter."
                )
            else:
                st.error("Email invalide ou déjà utilisé !")

    # ----------------------
    # Connexion
    # ----------------------
    elif option == "Se connecter":
        st.subheader("Connexion à votre compte")
        email = st.text_input(
            "Email", key="login_email", placeholder="exemple@domaine.com"
        )
        password = st.text_input("Mot de passe", type="password", key="login_pw")

        if st.button("Se connecter"):
            if not email or not password:
                st.error("Veuillez remplir tous les champs")
            elif verify_user(email, password):
                st.session_state.authenticated = True
                st.session_state.email = email
                st.success(f"Bienvenue {email}")
                st.rerun()
            else:
                st.error("Email invalide ou mot de passe incorrect !")
