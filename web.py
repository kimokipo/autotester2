import streamlit as st
import subprocess as sp
import sqlite3
import pandas as pd

# Add a selectbox to the sidebar:
etudiant = st.sidebar.selectbox(
    'Espace',
    ('Etudiant', 'Professeur')
)

# Récupérer les matières du fichier variables.json
import json
f = open('src/variables.json',)
data = json.load(f)

if etudiant == 'Etudiant':

    st.title('Autotester')

    slot_id = st.empty()
    slot_password = st.empty()

    slot_id.text_input("Identifiant", key="id")

    pwd = slot_password.text_input("Mot de passe", value="", type="password", key="password") 

    if (st.session_state.id == st.session_state.password) & (st.session_state.id != "" or st.session_state.password != ""):
        slot_id.empty()
        slot_password.empty()

        matieres = {matiere for matiere in data.keys()}

        matiere = st.selectbox("Matière", matieres)

        if matiere == "tob":
            tp = st.selectbox("TP", {"tp01", "tp02", "mini-projet", "projet-court"})
        elif matiere == "pim":
            tp = st.selectbox("TP", {"tp10", "tp06", "tp07"})

        "Veuillez choisir les scenarios à lancer:"
        file_scenarios = open('scenarios.json',)
        scenarios = json.load(file_scenarios)
        SCENARIOS = scenarios[matiere][tp]

        scenarios = ""

        for scenario in SCENARIOS:
            st.checkbox(scenario, key = scenario)

        for scenario in SCENARIOS:
            scenarios += scenario + " " if st.session_state[scenario] else ""

        cmd = "./featpp evaluate " + matiere + " " + st.session_state.id + " " + tp + " " + scenarios

        slot_run = st.empty()

        test = slot_run.button("Run")

        if test:
            if st.session_state.id != st.session_state.password:
                "Erreur d'authentification"
            else:
                slot_msg = st.empty()
                slot_msg.text('Lancement des tests du ' + tp + ' de ' + st.session_state.id)
                slot_run.empty()
                sp.run(cmd.split())
                slot_msg.empty()

    elif (st.session_state.id != st.session_state.password):
        "Erreur d'authentification"

else:
    st.title('Autotester')

    slot_id = st.empty()
    slot_password = st.empty()
    slot_signup = st.empty()

    slot_id.text_input("Identifiant", key="id_prof")

    pwd = slot_password.text_input("Mot de passe", value="", type="password", key="password_prof") 

    if (st.session_state["id_prof"] == 'cregut') & (st.session_state["id_prof"] == st.session_state["password_prof"]) & (st.session_state["id_prof"] != "" or st.session_state["password_prof"] != ""):
        slot_id.empty()
        slot_password.empty()
        slot_signup.empty()

        matieres = {matiere for matiere in data.keys()}

        matiere = st.selectbox("Matière", matieres)

        if matiere == "tob":
            tp = st.selectbox("TP", {"tp01", "tp02", "mini-projet", "projet-court"})
        elif matiere == "pim":
            tp = st.selectbox("TP", {"tp10", "tp06", "tp07"})

        groupe_tp = st.selectbox("Groupe de TP", {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'})

        file_scenarios = open('scenarios.json',)
        scenarios = json.load(file_scenarios)
        SCENARIOS = scenarios[matiere][tp]

        scenario = st.selectbox("Scenario", {scenario for scenario in SCENARIOS})

        # Récupération des informations en bdd
        database_address = data[matiere]["config_path"]+"/"+tp+"/database_test.db"
        con = sqlite3.connect(database_address)
        cur = con.cursor()
        cur.execute("SELECT Students, Attempts, Date, Mark, Penalty, Attempts_Done FROM " + scenario + " WHERE Groupe = \'%s\'" % groupe_tp)
        df = pd.DataFrame(cur.fetchall(), columns = ('Id', 'Max Attempts', 'Last test date', 'Mark', 'Penalty', 'Attempts'))
        df.sort_values(by=['Penalty'], inplace=True, ascending=False)
        st.table(df)
    elif (st.session_state["id_prof"] != "" or st.session_state["password_prof"] != ""):
        "Erreur d'authentification"