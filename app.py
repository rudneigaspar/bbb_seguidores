import streamlit as st
import instaloader
import time

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="BBB 26 - Monitor de Seguidores",
    page_icon="👁️",
    layout="wide"
)

# Estilo CSS para melhorar o visual
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #00d4ff; }
    div[data-testid="stMetricLabel"] { font-weight: bold; font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("👁️ BBB 26: Seguidores em Tempo Real")
st.subheader("Acompanhe o crescimento dos participantes no Instagram")

# 2. CONFIGURAÇÃO DOS PARTICIPANTES (Ajuste os nomes de usuário aqui)
# Chave: Nome exibido no site | Valor: @ do Instagram (sem o @)
participantes = {
    "👑 Líder": "samira_sagr",
    "🔥 No Paredão": "nome_emparedado_1",
    "🔥 No Paredão 2": "nome_emparedado_2",
    "Participante 4": "usuario_4",
    "Participante 5": "usuario_5",
    "Participante 6": "usuario_6",
    "Participante 7": "usuario_7",
    "Participante 8": "usuario_8",
    "Participante 9": "usuario_9",
    "Participante 10": "usuario_10",
    # Adicione todos os outros aqui seguindo o padrão
}

# 3. FUNÇÃO PARA BUSCAR DADOS
@st.cache_data(ttl=600) # Guarda os dados por 10 min para evitar bloqueio
def buscar_seguidores(username):
    L = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        return profile.followers
    except Exception as e:
        return None

# 4. INTERFACE EM TEMPO REAL
placeholder = st.empty()

while True:
    with placeholder.container():
        # Divide em 4 colunas para não ficar uma lista gigante vertical
        cols = st.columns(4)
        
        lista_nomes = list(participantes.keys())
        
        for index, nome in enumerate(lista_nomes):
            usuario = participantes[nome]
            qtd = buscar_seguidores(usuario)
            
            # Distribui os cards entre as colunas
            with cols[index % 4]:
                if qtd is not None:
                    # Formata número com ponto (Ex: 1.500.200)
                    valor = f"{qtd:,}".replace(",", ".")
                    st.metric(label=nome, value=valor, delta=f"@{usuario}")
                else:
                    st.metric(label=nome, value="Lidando...", delta="Insta instável")

        st.divider()
        st.caption(f"🔄 Última atualização: {time.strftime('%H:%M:%S')} (Atualiza a cada 10 min)")
        
        # 5. TEMPO DE ESPERA (ESSENCIAL)
        # 600 segundos = 10 minutos. Menos que isso o Instagram bloqueia o site.
        time.sleep(600)
        st.rerun()
