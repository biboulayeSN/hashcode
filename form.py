import hashlib
from datetime import datetime
from weasyprint import HTML

def generate_secure_code(nom, prenom, id_num, ninea, num_courrier):
    """Génère un hash alphanumérique de 12 caractères basé sur les informations saisies."""
    raw_data = f"{nom}|{prenom}|{id_num}|{ninea}|{num_courrier}".strip().upper()
    hash_hex = hashlib.sha256(raw_data.encode()).hexdigest()
    
    num = int(hash_hex, 16)
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = ""
    while num > 0 and len(code) < 12:
        num, i = divmod(num, 36)
        code = chars[i] + code
    return code.zfill(12)[:12]

def create_official_pdf(data_input, output_filename="note_information_dgid.pdf"):
    """Génère le document PDF officiel avec le code de hachage intégré."""
    auth_code = generate_secure_code(
        data_input['nom'], 
        data_input['prenom'], 
        data_input['id_num'], 
        data_input['ninea'], 
        data_input['num_courrier']
    )
    
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <style>
            @page {{
                size: A4;
                margin: 20mm;
                background-color: #ffffff;
            }}
            body {{
                font-family: 'Times New Roman', serif;
                line-height: 1.5;
                color: #333;
                text-align: justify;
            }}
            .header {{
                text-align: center;
                margin-bottom: 30px;
            }}
            .republique {{
                font-weight: bold;
                font-size: 14pt;
                text-transform: uppercase;
            }}
            .motto {{
                font-style: italic;
                font-size: 10pt;
                margin-bottom: 20px;
            }}
            .ministry {{
                font-weight: bold;
                font-size: 12pt;
                border-top: 1px solid #000;
                padding-top: 10px;
            }}
            .title-box {{
                text-align: center;
                margin: 40px 0;
                border: 2px solid #000;
                padding: 15px;
            }}
            .title-box h1 {{
                font-size: 16pt;
                margin: 0;
                text-transform: uppercase;
            }}
            .content p {{
                margin-bottom: 15px;
            }}
            .hash-section {{
                background-color: #f4f4f4;
                border: 1px dashed #333;
                padding: 20px;
                text-align: center;
                margin: 30px 0;
            }}
            .hash-label {{
                font-weight: bold;
                display: block;
                margin-bottom: 10px;
            }}
            .hash-value {{
                font-family: monospace;
                font-size: 22pt;
                letter-spacing: 5px;
                color: #004a99;
            }}
            .footer {{
                margin-top: 50px;
                text-align: right;
            }}
            .signature {{
                margin-top: 20px;
                font-weight: bold;
                text-align: right;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="republique">République du Sénégal</div>
            <div class="motto">Un Peuple – Un But – Une Foi</div>
            <div class="ministry">
                MINISTÈRE DES FINANCES ET DU BUDGET<br>
                DIRECTION GÉNÉRALE DES IMPÔTS ET DES DOMAINES
            </div>
        </div>

        <div class="title-box">
            <h1>Note d’information officielle</h1>
            <div style="font-size: 10pt; margin-top: 5px;">Relative aux nouvelles dispositions sécuritaires et à la plateforme déclarative</div>
        </div>

        <div class="content">
            <p>Dans le cadre du renforcement de la sécurité des procédures fiscales et de la modernisation de l’administration, la Direction Générale des Impôts et des Domaines (DGID) informe l’ensemble des contribuables et partenaires institutionnels de la mise en œuvre de nouvelles dispositions sécuritaires.</p>
            
            <p>Ces mesures visent notamment :</p>
            <ul>
                <li>La sécurisation des échanges numériques avec l’administration fiscale ;</li>
                <li>La fiabilisation des données déclaratives ;</li>
                <li>La prévention des risques de fraude et d’usurpation d’identité fiscale.</li>
            </ul>

            <p>À cet effet, une nouvelle plateforme déclarative sécurisée est désormais opérationnelle. Elle s’appuie sur une architecture avancée et sur l’intervention d’experts spécialisés opérant dans huit (08) pays membres de la CEDEAO.</p>

            <div class="hash-section">
                <span class="hash-label">🔐 Code d’authentification sécurisé</span>
                <p style="font-size: 10pt; margin-bottom: 15px;">Identifiant unique généré pour : {data_input['prenom']} {data_input['nom']}</p>
                <div class="hash-value">{auth_code}</div>
            </div>

            <p>Ce code, strictement confidentiel, est requis pour l’accès à la plateforme, la validation des opérations sensibles et la vérification de l’authenticité des échanges. Toute divulgation non autorisée engage la responsabilité du titulaire.</p>
        </div>

        <div class="footer">
            Fait à Dakar, le {current_date}
        </div>

        <div class="signature">
            Le Directeur Général<br>
            Direction Générale des Impôts et des Domaines<br>
            <span style="font-size: 9pt; font-weight: normal; font-style: italic;">(Signature numérique certifiée)</span>
        </div>
    </body>
    </html>
    """
    
    # Génération du fichier PDF
    HTML(string=html_content).write_pdf(output_filename)
    print(f"Succès : Le fichier '{output_filename}' a été généré avec le code {auth_code}.")

# --- Bloc d'exécution principal ---
if __name__ == "__main__":
    # Vous pouvez modifier ces valeurs pour tester avec vos propres données
    mes_donnees = {
        "nom": "VOTRE_NOM",
        "prenom": "VOTRE_PRENOM",
        "id_num": "12345678901234", # 14 caractères max
        "ninea": "123456789",       # 9 caractères
        "num_courrier": "DGID-2026-001"
    }
    
    create_official_pdf(mes_donnees)