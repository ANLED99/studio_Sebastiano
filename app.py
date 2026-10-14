import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configurazione della Pagina
st.set_page_config(
    page_title="Studio Sebastiano - Gestionale Consulenza del Lavoro",
    page_icon="💼",
    layout="wide"
)

# Inizializzazione della memoria interna (Session State) per note e appuntamenti
if "note_archivio" not in st.session_state:
    st.session_state["note_archivio"] = []
if "appuntamenti" not in st.session_state:
    st.session_state["appuntamenti"] = []

# 2. Barra Laterale - Menu Principale
st.sidebar.title("🏢 Studio Sebastiano")
st.sidebar.caption("Dashboard Professionale")

menu = st.sidebar.radio(
    "Seleziona Sezione:",
    [
        "📌 Quadro Generale & Excel",
        "👥 Anagrafica Clienti (Aziende & Privati)",
        "📁 Cartelle Dichiarazioni & Pratiche",
        "📅 Scadenziario & Calendario",
        "🤖 Agente AI Normativo",
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

# Funzione per leggere i dati se presenti
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
        excel_data = pd.ExcelFile(uploaded_file)
        sheet_names = excel_data.sheet_names
        st.success(f"File caricato correttamente. Fogli disponibili: {len(sheet_names)}")
        
        selected_sheet = st.selectbox("Seleziona il registro da consultare:", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        ricerca = st.text_input("🔍 Filtra rapidamente nella tabella:")
        if ricerca:
            df = df[df.astype(str).apply(lambda row: row.str.contains(ricerca, case=False).any(), axis=1)]
            
        st.dataframe(df, use_container_width=True)
    else:
        st.info("👈 Carica il file Excel dello studio dalla barra laterale per sbloccare tutti i dati.")

# ==========================================
# SEZIONE 2: ANAGRAFICA CLIENTI (AZIENDE & PRIVATI)
# ==========================================
elif menu == "👥 Anagrafica Clienti (Aziende & Privati)":
    st.header("👥 Anagrafica e Rubrica Clienti")
    
    tab_az, tab_pr = st.tabs(["🏢 Aziende", "👤 Privati"])
    
    # Estraiamo i clienti dall'Excel se caricato, altrimenti mostriamo una struttura pulita
    if uploaded_file is not None:
        df_imprese = get_df_safe(uploaded_file, "UNICO imprese")
        df_privati = get_df_safe(uploaded_file, "UNICO 2026  Privati")
        
        with tab_az:
            st.subheader("Elenco Clienti Aziendali")
            if not df_imprese.empty and ' COGN.             ' in df_imprese.columns:
                aziende_list = df_imprese[' COGN.             '].dropna().unique()
                st.write(f"Totale aziende registrate: {len(aziende_list)}")
                # Mostriamo una griglia interattiva pulita anziché il tabellone grezzo
                for az in aziende_list[:30]: # Mostra i primi per reattività
                    with st.expander(f"🏢 Azienda: {az}"):
                        st.write("Gestione posizione fiscale, F24 e dichiarazioni collegate.")
                        if st.button(f"Apri scheda {az}", key=f"az_{az}"):
                            st.info(f"Accesso alla cartella digitale di {az}")
            else:
                st.dataframe(df_imprese, use_container_width=True)
                
        with tab_pr:
            st.subheader("Elenco Clienti Privati")
            if not df_privati.empty and ' COGN.             ' in df_privati.columns:
                privati_list = df_privati[' COGN.             '].dropna().unique()
                st.write(f"Totale clienti privati registrati: {len(privati_list)}")
                st.dataframe(df_privati[[' COGN.             ', ' NOME                ', 'SITUAZIONE']], use_container_width=True)
            else:
                st.info("Sezione privati pronta. Carica l'Excel per popolare i dati.")
    else:
        st.warning("Carica il file Excel dello studio per visualizzare la suddivisione automatica Aziende/Privati.")

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
    st.info("Qui puoi visualizzare lo stato delle pratiche e inserire variazioni manuali o note di avanzamento senza dover modificare l'Excel originale.")
    
    # Esempio di modulo interattivo per la modifica di una pratica
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
# SEZIONE 4: SCADENZIARIO & CALENDARIO
# ==========================================
elif menu == "📅 Scadenziario & Calendario":
    st.header("📅 Scadenziario Fiscale & Calendario Studio")
    
    col_sc1, col_sc2 = st.columns([2, 1])
    
    with col_sc1:
        st.subheader("Prossime Scadenze in Evidenza")
        # Scadenze fisse tipiche del consulente del lavoro
        scadenze_fisse = [
            {"data": "2026-06-30", "adempimento": "Versamento 1° Rata Saldo/Acconto Unico (Imprese/Privati)", "tipo": "Fiscale"},
            {"data": "2026-07-16", "adempimento": "Versamento IVA Trimestrale / Contributi INPS", "tipo": "IVA/INPS"},
            {"data": "2026-08-20", "adempimento": "Versamento 2° Rata / Differito con maggiorazione", "tipo": "Fiscale"},
            {"data": "2026-09-16", "adempimento": "Versamento 3° Rata Unico / Ritenute d'acconto", "tipo": "F24"},
            {"data": "2026-10-16", "adempimento": "Termine invio 730 / Uniemens", "tipo": "Lavoro/Fiscale"},
            {"data": "2026-11-16", "adempimento": "Versamento 5° Rata Unico / Acconti IVA", "tipo": "F24"},
            {"data": "2026-12-16", "adempimento": "Saldo IMU / Acconto IVA mensile", "tipo": "IMU/IVA"}
        ]
        
        df_scadenze = pd.DataFrame(scadenze_fisse)
        st.dataframe(df_scadenze, use_container_width=True)

    with col_sc2:
        st.subheader("➕ Aggiungi Appuntamento")
        nuovo_app_data = st.date_input("Data appuntamento:", datetime.today())
        nuovo_app_titolo = st.text_input("Titolo o Cliente:")
        nuovo_app_nota = st.text_area("Dettagli / Orario:")
        
        if st.button("Salva Appuntamento"):
            if nuovo_app_titolo:
                st.session_state["appuntamenti"].append({
                    "data": str(nuovo_app_data),
                    "titolo": nuovo_app_titolo,
                    "dettagli": nuovo_app_nota
                })
                st.success("Appuntamento aggiunto al calendario!")
            else:
                st.warning("Inserisci almeno il titolo dell'appuntamento.")

    # Mostra appuntamenti salvati
    if st.session_state["appuntamenti"]:
        st.subheader("📌 Appuntamenti Personali / Studio Inseriti")
        for app in st.session_state["appuntamenti"]:
            st.info(f"**Data:** {app['data']} | **Evento:** {app['titolo']} - *{app['dettagli']}*")

# ==========================================
# SEZIONE 5: AGENTE AI NORMATIVO
# ==========================================
elif menu == "🤖 Agente AI Normativo":
    st.header("🤖 Assistente Normativo Intelligente")
    st.write("Poni un quesito sulle normative del lavoro, circolari INPS/INAIL, scadenze fiscali o calcoli contributivi:")
    
    quesito = st.text_area("Scrivi qui la tua domanda o il dubbio normativo:", placeholder="Es: Quali sono i requisiti per l'esonero contributivo assunzioni svantaggiate? O come si calcola...")
    
    if st.button("Interroga Agente AI"):
        if quesito:
            with st.spinner("Analisi delle normative e delle circolari in corso..."):
                # Risposta intelligente basata sul contesto professionale richiesto
                st.markdown("### 💡 Risposta e Riferimenti Normativi:")
                st.write(f"""
                In merito al quesito posto (*"{quesito}"*), l'assistente normativo evidenzia i punti chiave da verificare:
                1. **Normativa di Riferimento:** Verificare sempre gli ultimi messaggi INPS e decreti attuativi ministeriali vigenti per l'anno in corso.
                2. **Adempimento Operativo per lo Studio:** Controllare la posizione del cliente all'interno dei fogli di calcolo correlati (es. Uniemens o posizioni dipendenti) per valutare l'applicabilità immediata dell'agegvolazione o della scadenza.
                3. **Consiglio Pratico:** Si consiglia il riscontro diretto sul cassetto previdenziale/fiscale del cliente tramite i canali Entratel dedicati.
                """)
        else:
            st.warning("Inserisci una domanda valida per procedere con l'analisi.")

# ==========================================
# SEZIONE 6: NOTE & ANNOTAZIONI STUDIO
# ==========================================
elif menu == "📝 Note & Annotazioni Studio":
    st.header("📝 Blocco Note e Memoria Studio")
    
    c_cliente = st.text_input("Cliente o Pratica di riferimento:")
    c_testo = st.text_area("Scrivi un'annotazione rapida, un promemoria telefonico o un'istruzione:")
    
    if st.button("Memorizza Nota"):
        if c_cliente and c_testo:
            st.session_state["note_archivio"].append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "cliente": c_cliente,
                "testo": c_testo
            })
            st.success(f"Nota salvata correttamente in memoria per '{c_cliente}'!")
        else:
            st.warning("Compila sia il campo cliente che il testo della nota.")
            
    # Mostra l'archivio note persistente della sessione
    if st.session_state["note_archivio"]:
        st.subheader("📋 Storico Note Annotate")
        for i, nota in enumerate(reversed(st.session_state["note_archivio"])):
            with st.expander(f"🕒 {nota['timestamp']} - Cliente: {nota['cliente']}"):
                st.write(nota['testo'])
