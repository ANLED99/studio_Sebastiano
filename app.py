import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Studio Sebastiano - Gestionale Consulenza del Lavoro",
    page_icon="💼",
    layout="wide"
)

# Inizializzazione della memoria interna (Session State)
if "note_archivio" not in st.session_state:
    st.session_state["note_archivio"] = []
if "appuntamenti" not in st.session_state:
    st.session_state["appuntamenti"] = []
if "cronologia_ai" not in st.session_state:
    st.session_state["cronologia_ai"] = []

# 2. Barra Laterale - Menu Principale
st.sidebar.title("🏢 Studio Sebastiano")
st.sidebar.caption("Dashboard Professionale")

menu = st.sidebar.radio(
    "Seleziona Sezione:",
    [
        "📌 Quadro Generale & Excel",
        "👥 Anagrafica Clienti (Aziende & Privati)",
        "📁 Cartelle Dichiarazioni & Pratiche",
        "💼 Fatturazione & Storico Studio",
        "📅 Scadenziario & Calendario",
        "🤖 Agente AI Normativo & Cronologia",
        "📝 Note & Annotazioni Studio"
    ]
)

# Caricamento file Excel globale nella sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📁 Database Excel Studio")
uploaded_file = st.sidebar.file_uploader(
    "Carica o aggiorna il file Excel (.xlsx)", 
    type=["xlsx", "xls"]
)

# Funzione per leggere in sicurezza i fogli
def get_df_safe(file, sheet):
    try:
        return pd.read_excel(file, sheet_name=sheet)
    except:
        return pd.DataFrame()

# ==========================================
# SEZIONE 1: QUADRO GENERALE & EXCEL
# ==========================================
if menu == "📌 Quadro Generale & Excel":
    st.header("📌 Quadro Generale Scadenze Studio")
    
    if uploaded_file is not None:
        try:
            excel_data = pd.ExcelFile(uploaded_file)
            sheet_names = excel_data.sheet_names
            st.success(f"File caricato correttamente. Fogli disponibili: {len(sheet_names)}")
            
            selected_sheet = st.selectbox("Seleziona il registro da consultare:", sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            
            ricerca = st.text_input("🔍 Filtra rapidamente nella tabella:")
            if ricerca:
                df = df[df.astype(str).apply(lambda row: row.str.contains(ricerca, case=False).any(), axis=1)]
                
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Errore nella lettura del file: {e}")
    else:
        st.info("👈 Carica il file Excel dello studio dalla barra laterale per sbloccare tutti i dati.")

# ==========================================
# SEZIONE 2: ANAGRAFICA CLIENTI (AZIENDE & PRIVATI)
# ==========================================
elif menu == "👥 Anagrafica Clienti (Aziende & Privati)":
    st.header("👥 Anagrafica e Rubrica Clienti")
    
    tab_az, tab_pr = st.tabs(["🏢 Aziende", "👤 Privati"])
    
    if uploaded_file is not None:
        df_imprese = get_df_safe(uploaded_file, "UNICO imprese")
        df_privati = get_df_safe(uploaded_file, "UNICO 2026  Privati")
        
        with tab_az:
            st.subheader("Elenco Clienti Aziendali")
            if not df_imprese.empty and ' COGN.             ' in df_imprese.columns:
                aziende_list = df_imprese[' COGN.             '].dropna().unique()
                st.write(f"Totale aziende registrate: **{len(aziende_list)}**")
                for az in aziende_list[:30]:
                    with st.expander(f"🏢 Azienda: {str(az).strip()}"):
                        st.write("Gestione posizione fiscale, F24 e dichiarazioni collegate.")
            else:
                st.dataframe(df_imprese, use_container_width=True)
                
        with tab_pr:
            st.subheader("Elenco Clienti Privati")
            if not df_privati.empty and ' COGN.             ' in df_privati.columns:
                privati_list = df_privati[' COGN.             '].dropna().unique()
                st.write(f"Totale clienti privati registrati: **{len(privati_list)}**")
                st.dataframe(df_privati[[' COGN.             ', ' NOME                ', 'SITUAZIONE']], use_container_width=True)
            else:
                st.info("Sezione privati pronta. Carica l'Excel per popolare i dati.")
    else:
        st.warning("Carica il file Excel dello studio dalla barra laterale per visualizzare l'anagrafica automatica.")

# ==========================================
# SEZIONE 3: CARTELLE DICHIARAZIONI & PRATICHE
# ==========================================
elif menu == "📁 Cartelle Dichiarazioni & Pratiche":
    st.header("📁 Cartelle Digitali per Adempimento")
    st.write("Seleziona una categoria per gestire le pratiche in modo agevole e modificabile:")
    
    categoria = st.selectbox(
        "Scegli la tipologia di dichiarazione/pratica:",
        ["Unico Imprese & Soci", "Unico Professionisti / Forfettari", "Modello 730 & Privati", "Dichiarazioni IVA & LIPE", "CU & Modello 770", "IMU"]
    )
    
    st.markdown(f"### Gestione Cartella: **{categoria}**")
    st.info("Qui puoi visualizzare lo stato delle pratiche e inserire variazioni manuali o note di avanzamento.")
    
    col1, col2 = st.columns(2)
    with col1:
        cli_sel = st.text_input("Nome Cliente / Ragione Sociale:")
        stato_pratica = st.selectbox("Stato Lavorazione:", ["Da Richiedere", "Documenti Ricevuti", "In Lavorazione", "Pronto / Verificato", "Spedito / Archiviato"])
    with col2:
        note_pratica = st.text_area("Note specifiche sulla pratica:")
        if st.button("Aggiorna / Salva Posizione Pratica"):
            if cli_sel:
                st.success(f"Posizione per '{cli_sel}' aggiornata con successo a: [{stato_pratica}]")
            else:
                st.error("Inserisci il nome del cliente.")

# ==========================================
# SEZIONE 4: FATTURAZIONE & STORICO STUDIO
# ==========================================
elif menu == "💼 Fatturazione & Storico Studio":
    st.header("💼 Fatturazione, Parcelle e Storico Produttività")
    st.write("Analisi della fatturazione ai clienti, corrispettivi e andamento storico della produzione dello studio.")
    
    if uploaded_file is not None:
        df_fatt = get_df_safe(uploaded_file, "SITUAZ_FATTURAZIONE")
        df_foglio1 = get_df_safe(uploaded_file, "Foglio1")
        
        tab_f1, tab_f2 = st.tabs(["📊 Situazione Fatture / Clienti", "📈 Storico Mensile & Annuale"])
        
        with tab_f1:
            st.subheader("Riepilogo Posizioni di Fatturazione")
            if not df_fatt.empty:
                ricerca_fatt = st.text_input("🔍 Cerca cliente nel registro fatturazione:")
                if ricerca_fatt:
                    df_fatt = df_fatt[df_fatt.astype(str).apply(lambda row: row.str.contains(ricerca_fatt, case=False).any(), axis=1)]
                st.dataframe(df_fatt, use_container_width=True)
            else:
                st.info("Foglio 'SITUAZ_FATTURAZIONE' vuoto o non trovato.")
                
        with
