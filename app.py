
import streamlit as st
import pandas as pd

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Dashboard Studio - Consulenza del Lavoro",
    page_icon="💼",
    layout="wide"
)

# 2. Barra Laterale - Menu Principale
st.sidebar.title("🏢 Studio Consulenza")
st.sidebar.caption("Benvenuto, Dottore")

menu = st.sidebar.radio(
    "Seleziona Sezione:",
    [
        "📌 Vista Generale & Scadenze",
        "🏢 Dichiarazioni Aziende",
        "👤 Dichiarazioni Privati",
        "💼 Fatturazione Studio",
        "🤖 Agente AI Normativo",
        "📝 Annotazioni & Note Clienti"
    ]
)

# Area Caricamento File Excel Condivisa
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Gestione Dati Excel")
uploaded_file = st.sidebar.file_uploader(
    "Carica il file Excel dello studio (.xlsx)", 
    type=["xlsx", "xls"]
)

# 3. Gestione della Sezione: Vista Generale & Scadenze
if menu == "📌 Vista Generale & Scadenze":
    st.header("📌 Quadro Generale Scadenze Studio")
    
    if uploaded_file is not None:
        try:
            # Legge i nomi dei fogli direttamente dal file caricato
            excel_data = pd.ExcelFile(uploaded_file)
            sheet_names = excel_data.sheet_names
            
            st.success(f"File caricato con successo! Rilevati {len(sheet_names)} fogli di lavoro.")
            
            # Scelta del foglio specifico
            selected_sheet = st.selectbox("Seleziona l'adempimento / foglio da consultare:", sheet_names)
            
            # Carica il foglio selezionato
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            
            # Filtro di ricerca per cliente / nome / cognome
            ricerca_cliente = st.text_input("🔍 Cerca per Nome, Cognome o Cliente:")
            
            if ricerca_cliente:
                df = df[df.astype(str).apply(lambda row: row.str.contains(ricerca_cliente, case=False).any(), axis=1)]

            # Visualizzazione della tabella interattiva
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Errore nella lettura del file Excel: {e}")
    else:
        st.info("👈 Carica il file Excel dello studio tramite la barra laterale per visualizzare tutte le scadenze e i fogli di lavoro.")

# 4. Sezione: Dichiarazioni Aziende
elif menu == "🏢 Dichiarazioni Aziende":
    st.header("🏢 Dichiarazioni e Adempimenti Aziendali")
    if uploaded_file is not None:
        try:
            excel_data = pd.ExcelFile(uploaded_file)
            sheets_aziende = [s for s in excel_data.sheet_names if any(k in s.lower() for k in ['unico', 'soci', 'professionisti', 'forfettari', 'irap', 'iva', 'cu', '770'])]
            
            if sheets_aziende:
                sel_sheet = st.selectbox("Seleziona registro aziendale:", sheets_aziende)
                df_az = pd.read_excel(uploaded_file, sheet_name=sel_sheet)
                st.dataframe(df_az, use_container_width=True)
            else:
                st.warning("Nessun foglio aziendale specifico trovato nel file.")
        except Exception as e:
            st.error(f"Errore: {e}")
    else:
        st.info("Carica prima il file Excel dalla barra laterale.")

# 5. Sezione: Dichiarazioni Privati
elif menu == "👤 Dichiarazioni Privati":
    st.header("👤 Dichiarazioni Privati (730 e IMU)")
    if uploaded_file is not None:
        try:
            excel_data = pd.ExcelFile(uploaded_file)
            sheets_privati = [s for s in excel_data.sheet_names if any(k in s.lower() for k in ['730', 'privati', 'imu'])]
            
            if sheets_privati:
                sel_sheet = st.selectbox("Seleziona registro privati:", sheets_privati)
                df_pr = pd.read_excel(uploaded_file, sheet_name=sel_sheet)
                st.dataframe(df_pr, use_container_width=True)
            else:
                st.info("Nessun foglio dedicato ai privati trovato.")
        except Exception as e:
            st.error(f"Errore: {e}")
    else:
        st.info("Carica prima il file Excel dalla barra laterale.")

# 6. Sezione: Fatturazione Studio
elif menu == "💼 Fatturazione Studio":
    st.header("💼 Fatturazione e Parcelle Studio")
    if uploaded_file is not None:
        try:
            excel_data = pd.ExcelFile(uploaded_file)
            if 'SITUAZ_FATTURAZIONE' in excel_data.sheet_names:
                df_fatt = pd.read_excel(uploaded_file, sheet_name='SITUAZ_FATTURAZIONE')
                st.dataframe(df_fatt, use_container_width=True)
            else:
                st.info("Foglio 'SITUAZ_FATTURAZIONE' non trovato nel file Excel.")
        except Exception as e:
            st.error(f"Errore: {e}")
    else:
        st.info("Carica prima il file Excel dalla barra laterale.")

# 7. Sezione: Agente AI Normativo
elif menu == "🤖 Agente AI Normativo":
    st.header("🤖 Assistente Normativo AI")
    st.write("Poni una domanda sulle ultime circolari, Decreti Legge o scadenze tributarie in campo di consulenza del lavoro.")
    domanda = st.text_input("Chiedi all'Agente AI:")
    if domanda:
        st.info(f"Analisi normativa in corso per: '{domanda}'... (Modulo in fase di attivazione)")

# 8. Sezione: Annotazioni & Note Clienti
elif menu == "📝 Annotazioni & Note Clienti":
    st.header("📝 Note & Annotazioni")
    cliente_nota = st.text_input("Nome Cliente o Pratica di riferimento:")
    nota_testo = st.text_area("Inserisci annotazione o promemoria di servizio:")
    if st.button("Salva Nota"):
        if cliente_nota and nota_testo:
            st.success(f"Nota salvata correttamente per il cliente: {cliente_nota}")
        else:
            st.warning("Inserisci sia il nome del cliente che il testo della nota.")
