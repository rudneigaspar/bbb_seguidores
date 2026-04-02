import streamlit as st
import instaloader
import pandas as pd
import time

# Configuração da página
st.set_page_config(page_title="BBB Tracker 2026", page_icon="👁️")

st.title("👁️ BBB Tracker - Seguidores Real-Time")
st.write("Atualizando dados diretamente do Instagram...")

# Inicializa o Instaloader (o robô que lê o Instagram)
L = instaloader.Instaloader()

# Lista de participantes (Substitua pelos nomes reais do Instagram)
participantes = {
    "Participante 1": "boninho",
    "Participante 2": "tadeuschmidt",
    "Participante 3": "bbb"
}

def buscar_seguidores(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        return profile.followers
    except:
        return "Erro"

# Criar a interface
col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

# Loop de atualização
placeholder = st.empty()

while True:
    with placeholder.container():
        dados_lista = []
        
        # Criando os cards
        for i, (nome, user) in enumerate(participantes.items()):
            qtd = buscar_seguidores(user)
            
            with cols[i % 3]:
                st.metric(label=nome, value=f"{qtd:,}".replace(",", "."), delta=user)
                dados_lista.append({"Nome": nome, "Seguidores": qtd})
        
        st.write("---")
        st.caption("Próxima atualização em 60 segundos... (Para evitar bloqueios)")
        
        # Espera 1 minuto antes de atualizar de novo (importante!)
        time.sleep(60)
        st.rerun()