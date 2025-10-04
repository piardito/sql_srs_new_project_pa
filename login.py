# pylint: disable=missing-module-docstring
# pylint: disable=missing-final-newline
# pylint: disable=too-many-branches
import streamlit as st

from users import add_user, verify_user


def _local_css():
    """Applique fond bleu clair, police Roboto,
    boutons noirs et design clair moderne."""

    st.markdown(
        """
        <style>
        /* Importer Roboto */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

        /* Fond bleu clair pour toute la page */
        .stApp {
            background: linear-gradient(180deg, #e0f2fe 0%, #f0f9ff 100%);
            font-family: 'Roboto', sans-serif;
        }

        /* Container principal */
        .main-container {
            max-width: 900px;
            margin: 60px auto;
            background: rgba(255, 255, 255, 0.97);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            font-family: 'Roboto', sans-serif;
        }

        h1 {
            color: #0f172a;
            text-align: left;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: #334155;
            margin-bottom: 32px;
            font-size: 1.1rem;
        }

        /* Boutons avec bordure noire et texte noir */
        .stButton>button {
            width: 100%;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            color: #000000;
            border: 2px solid #000000;
            border-radius: 8px;
            height: 42px;
            font-weight: 500;
            font-family: 'Roboto', sans-serif;
            transition: all 0.25s ease;
        }

        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(59,130,246,0.3);
        }

        .card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 3px 8px rgba(0,0,0,0.04);
            font-family: 'Roboto', sans-serif;
        }

        .footer {
            margin-top: 40px;
            font-size: 0.9rem;
            color: #334155;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


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

    _local_css()

    st.markdown("# SQL SRS : Connexion")

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
