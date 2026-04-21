import streamlit as st
import hashlib
from datetime import datetime
from weasyprint import HTML

def generate_secure_code(nom, prenom, id_num, ninea, num_courrier):
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
            <h1>Note d’information officielle</h1>
        </div>
        <div class="content">
            <p>Dans le cadre de la sécurisation de vos declarations, une nouvelle plateforme est opérationnelle, SENTAX. </p>
            <p>Veuillez acceder au site esentax.dgid.sn en utilisant le code suivant pour vous authentifier.</p>
            <div class="hash-section">
                <strong>🔐 Code d’authentification sécurisé</strong>
                <p>Identifiant unique généré pour : {data_input['ninea']}</p>
                <div class="hash-value">{auth_code}</div>
            </div>
        </div>
        <div class="footer">Fait à Dakar, le {current_date}</div>
    </body>
    </html>
    """
    # Retourne le PDF en mémoire (bytes) au lieu d'un fichier local
    return HTML(string=html_content).write_pdf()

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Générateur DGID", page_icon="🇸🇳")
st.title("Génération de Note d'Information")

with st.form("formulaire_dgid"):
    nom = st.text_input("Nom")
    prenom = st.text_input("Prénom")
    id_num = st.text_input("Numéro ID (14 car. max)", max_chars=14)
    ninea = st.text_input("NINEA (9 car. max)", max_chars=9)
    num_courrier = st.text_input("N° courrier / Lettre d'acceptation")
    
    submit_button = st.form_submit_button("Générer le document PDF")

if submit_button:
    if not (nom and prenom and id_num and ninea and num_courrier):
        st.error("Tous les champs sont obligatoires.")
    else:
        donnees = {
            "nom": nom, "prenom": prenom, "id_num": id_num,
            "ninea": ninea, "num_courrier": num_courrier
        }
        
        with st.spinner("Génération du PDF..."):
            pdf_bytes = create_official_pdf_bytes(donnees)
            
        st.success("Document généré avec succès !")
        st.download_button(
            label="📄 Télécharger le PDF officiel",
            data=pdf_bytes,
            file_name=f"note_securitaire_{nom}_{prenom}.pdf",
            mime="application/pdf"
        )
