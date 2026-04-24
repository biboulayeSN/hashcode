import streamlit as st
import hashlib
from datetime import datetime
from weasyprint import HTML

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Générateur DGID - SENTAX",
    page_icon="🇸🇳",
    layout="wide"
)

# Identifiants par défaut
DEFAULT_MATRICULE = "123456A"
DEFAULT_PASSWORD = "passer"
CENTRE_FISCAL = "CME Dakar 1"


# ============================================================
# FONCTIONS MÉTIER
# ============================================================
def generate_secure_code(nom, prenom, id_num, ninea, num_courrier):
    """Génère un code d'authentification sécurisé basé sur SHA-256."""
    raw_data = f"{nom}|{prenom}|{id_num}|{ninea}|{num_courrier}".strip().upper()
    hash_hex = hashlib.sha256(raw_data.encode()).hexdigest()
    num = int(hash_hex, 16)
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    while num > 0 and len(code) < 12:
        num, i = divmod(num, 36)
        code = chars[i] + code
    return code.zfill(12)[:12]


def create_official_pdf_bytes(data_input):
    """Génère un PDF officiel en mémoire."""
    auth_code = generate_secure_code(
        data_input['nom'], data_input['prenom'],
        data_input['id_num'], data_input['ninea'], data_input['num_courrier']
    )
    current_date = datetime.now().strftime("%d/%m/%Y")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{ size: A4; margin: 20mm; }}
            body {{ font-family: 'Times New Roman', serif; line-height: 1.5; text-align: justify; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .republique {{ font-weight: bold; font-size: 14pt; text-transform: uppercase; }}
            .motto {{ font-style: italic; font-size: 10pt; margin-bottom: 20px; }}
            .ministry {{ font-weight: bold; font-size: 12pt; border-top: 1px solid #000; padding-top: 10px; }}
            .title-box {{ text-align: center; margin: 40px 0; border: 2px solid #000; padding: 15px; }}
            .hash-section {{ background-color: #f4f4f4; border: 1px dashed #333; padding: 20px; text-align: center; margin: 30px 0; }}
            .hash-value {{ font-family: monospace; font-size: 22pt; letter-spacing: 5px; color: #004a99; }}
            .info-contact {{ margin: 20px 0; padding: 10px; background-color: #fafafa; border-left: 3px solid #004a99; }}
            .footer {{ margin-top: 50px; text-align: right; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="republique">République du Sénégal</div>
            <div class="motto">Un Peuple – Un But – Une Foi</div>
            <div class="ministry">MINISTÈRE DES FINANCES ET DU BUDGET<br>DIRECTION GÉNÉRALE DES IMPÔTS ET DES DOMAINES</div>
        </div>
        <div class="title-box">
            <h1>Note d'information officielle</h1>
        </div>
        <div class="content">
            <p>Dans le cadre de la sécurisation de vos déclarations, une nouvelle plateforme est opérationnelle, SENTAX.</p>
            <p>Veuillez accéder au site esentax.dgid.sn en utilisant le code suivant pour vous authentifier.</p>
            <div class="hash-section">
                <strong>🔐 Code d'authentification sécurisé</strong>
                <p>Identifiant unique généré pour : {data_input['ninea']}</p>
                <div class="hash-value">{auth_code}</div>
            </div>
            <div class="info-contact">
                <strong>Coordonnées du destinataire :</strong><br>
                Nom complet : {data_input['prenom']} {data_input['nom']}<br>
                Téléphone : {data_input['telephone']}<br>
                Email : {data_input['email']}<br>
                N° Courrier : {data_input['num_courrier']}
            </div>
        </div>
        <div class="footer">Fait à Dakar, le {current_date}</div>
    </body>
    </html>
    """
    return HTML(string=html_content).write_pdf()


# ============================================================
# INITIALISATION DE L'ÉTAT
# ============================================================
if "authentifie" not in st.session_state:
    st.session_state.authentifie = False
if "matricule_connecte" not in st.session_state:
    st.session_state.matricule_connecte = ""
if "donnees_saisies" not in st.session_state:
    st.session_state.donnees_saisies = None
if "etape" not in st.session_state:
    st.session_state.etape = "saisie"  # saisie -> confirmation -> genere


# ============================================================
# PAGE DE CONNEXION
# ============================================================
def afficher_connexion():
    st.title("Plateforme GENERATION DE CODE SENTAX - DGID")
    st.markdown("### Connexion agent")

    col_gauche, col_droite = st.columns([1, 1])

    with col_gauche:
        with st.form("form_login"):
            matricule = st.text_input("Matricule", placeholder="Ex : 123456A")
            mot_de_passe = st.text_input("Mot de passe", type="password")
            bouton_connexion = st.form_submit_button("Se connecter", type="primary")

        if bouton_connexion:
            if matricule == DEFAULT_MATRICULE and mot_de_passe == DEFAULT_PASSWORD:
                st.session_state.authentifie = True
                st.session_state.matricule_connecte = matricule
                st.rerun()
            else:
                st.error("❌ Matricule ou mot de passe incorrect.")

    with col_droite:
        st.info(
            "**Identifiants par défaut :**\n\n"
            f"- Matricule : `{DEFAULT_MATRICULE}`\n"
            f"- Mot de passe : `{DEFAULT_PASSWORD}`"
        )


# ============================================================
# BANDEAU INFOS CONNEXION
# ============================================================
def afficher_bandeau_connexion():
    """Affiche les informations de connexion en haut à gauche."""
    with st.container():
        col_info, col_spacer, col_logout = st.columns([2, 3, 1])
        with col_info:
            st.markdown(
                f"""
                <div style="
                    background-color: #2a2a2b;
                    border-left: 4px solid #004a99;
                    padding: 10px 15px;
                    border-radius: 4px;
                    font-size: 14px;
                ">
                    <strong>👤 Matricule :</strong> {st.session_state.matricule_connecte}<br>
                    <strong>🏢 Centre fiscal :</strong> {CENTRE_FISCAL}
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_logout:
            if st.button("🚪 Déconnexion"):
                for key in ["authentifie", "matricule_connecte", "donnees_saisies", "etape"]:
                    st.session_state.pop(key, None)
                st.rerun()
    st.markdown("---")


# ============================================================
# ÉTAPE 1 : SAISIE DU FORMULAIRE
# ============================================================
def afficher_formulaire():
    st.title("📝 Génération de Note d'Information")
    st.caption("Étape 1/2 : Saisie des informations")

    with st.form("formulaire_dgid"):
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom *")
            id_num = st.text_input("Numéro ID (14 car. max) *", max_chars=14)
            telephone = st.text_input("Numéro de téléphone *", placeholder="Ex : +221 77 123 45 67")
        with col2:
            prenom = st.text_input("Prénom *")
            ninea = st.text_input("NINEA (9 car. max) *", max_chars=9)
            email = st.text_input("Adresse e-mail *", placeholder="exemple@domaine.sn")

        num_courrier = st.text_input("N° courrier / Lettre d'acceptation *")

        st.caption("Les champs marqués d'un * sont obligatoires.")
        soumettre = st.form_submit_button("Valider et prévisualiser", type="primary")

    if soumettre:
        # Validation des champs obligatoires
        champs = {
            "Nom": nom, "Prénom": prenom, "Numéro ID": id_num,
            "NINEA": ninea, "Téléphone": telephone,
            "Email": email, "N° courrier": num_courrier
        }
        manquants = [k for k, v in champs.items() if not v.strip()]

        if manquants:
            st.error(f"❌ Champs obligatoires manquants : {', '.join(manquants)}")
            return

        # Validation simple de l'email
        if "@" not in email or "." not in email:
            st.error("❌ L'adresse e-mail n'est pas valide.")
            return

        # Enregistrement et passage à la confirmation
        st.session_state.donnees_saisies = {
            "nom": nom.strip(),
            "prenom": prenom.strip(),
            "id_num": id_num.strip(),
            "ninea": ninea.strip(),
            "telephone": telephone.strip(),
            "email": email.strip(),
            "num_courrier": num_courrier.strip(),
        }
        st.session_state.etape = "confirmation"
        st.rerun()


# ============================================================
# ÉTAPE 2 : CONFIRMATION AVANT GÉNÉRATION
# ============================================================
def afficher_confirmation():
    st.title("✅ Confirmation des informations")
    st.caption("Étape 2/2 : Vérifiez les données avant génération du PDF")

    d = st.session_state.donnees_saisies

    st.markdown(
        f"""
        <div style="
            background-color: #2a2a2b;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 20px;
            margin: 20px 0;
        ">
            <h4 style="margin-top: 0; color: #004a99;">📋 Récapitulatif</h4>
            <table style="width: 100%; font-size: 15px;">
                <tr><td style="padding: 6px 0;"><strong>Nom :</strong></td><td>{d['nom']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Prénom :</strong></td><td>{d['prenom']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Numéro ID :</strong></td><td>{d['id_num']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>NINEA :</strong></td><td>{d['ninea']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Téléphone :</strong></td><td>{d['telephone']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>Email :</strong></td><td>{d['email']}</td></tr>
                <tr><td style="padding: 6px 0;"><strong>N° courrier :</strong></td><td>{d['num_courrier']}</td></tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.warning("⚠️ Vérifiez attentivement les informations. Une fois le PDF généré, le code d'authentification sera définitif.")

    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        if st.button("↩️ Modifier", use_container_width=True):
            st.session_state.etape = "saisie"
            st.rerun()
    with col2:
        if st.button("✅ Confirmer et générer", type="primary", use_container_width=True):
            st.session_state.etape = "genere"
            st.rerun()


# ============================================================
# ÉTAPE 3 : GÉNÉRATION DU PDF
# ============================================================
def afficher_generation():
    st.title("📄 Document généré")

    d = st.session_state.donnees_saisies

    with st.spinner("Génération du PDF en cours..."):
        pdf_bytes = create_official_pdf_bytes(d)

    st.success("✅ Document généré avec succès !")

    # Affichage du code d'authentification généré
    auth_code = generate_secure_code(
        d['nom'], d['prenom'], d['id_num'], d['ninea'], d['num_courrier']
    )
    st.markdown(
        f"""
        <div style="
            background-color: #2a2a2b;
            border: 1px dashed #2e7d32;
            border-radius: 6px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        ">
            <strong>🔐 Code d'authentification :</strong>
            <div style="
                font-family: monospace;
                font-size: 26px;
                letter-spacing: 4px;
                color: #004a99;
                margin-top: 10px;
            ">{auth_code}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Télécharger le PDF officiel",
            data=pdf_bytes,
            file_name=f"note_securitaire_{d['nom']}_{d['prenom']}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    with col2:
        if st.button("🆕 Nouvelle génération", use_container_width=True):
            st.session_state.donnees_saisies = None
            st.session_state.etape = "saisie"
            st.rerun()


# ============================================================
# ROUTAGE PRINCIPAL
# ============================================================
if not st.session_state.authentifie:
    afficher_connexion()
else:
    afficher_bandeau_connexion()

    if st.session_state.etape == "saisie":
        afficher_formulaire()
    elif st.session_state.etape == "confirmation":
        afficher_confirmation()
    elif st.session_state.etape == "genere":
        afficher_generation()
