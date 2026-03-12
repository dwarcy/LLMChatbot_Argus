import streamlit as st
import time
from twophased_argus import rag_answer

st.markdown("""
<style>
    /* 1. RESET DE FUNDO E CABEÇALHO */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0); 
    }

    [data-testid="stAppViewContainer"] {
        background-image: url("https://images.unsplash.com/photo-1615715410008-3883e21f8c7c?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }

    /* 2. EFEITO VIDRO NAS MENSAGENS (Blur + Transparência) */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.2) !important; 
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
    }

    /* Força cor preta em todos os textos de chat */
    [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] div {
        color: #000000 !important;
    }

    /* 3. CAIXA DE INPUT (Fundo Branco e Texto Preto) */
    [data-testid="stChatInput"] textarea {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        caret-color: #000000 !important;
    }

    [data-testid="stChatInput"] {
        background-color: transparent !important;
    }

    /* 4. CABEÇALHO FIXO */
    .fixed-header {
        position: fixed;
        top: 0; left: 0; width: 100%;
        background-color: rgba(255, 255, 255, 0.35); 
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        z-index: 1000; 
        padding: 3rem 1rem 0.6rem 5rem; 
        border-bottom: 1px solid rgba(0, 0, 0, 0.1); 
    }

    .fixed-header h1 {
        color: #000000 !important;
        margin-bottom: 0;
    }

    .block-container {
        padding-top: 180px; 
    }
    
</style>

<div class="fixed-header">
    <h1>👁️ Argus</h1>
    <p style="color: #000000; font-size: 14px; margin-top: 0; opacity: 0.8;">Your all-seeing oracle. Ask me anything about Greek mythology, gods, and legends.</p>
</div>
""", unsafe_allow_html=True)

# Adaptador para fazer a resposta real do LLM aparecer digitando aos poucos
def stream_llm_response(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.05)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome! I am Argus, your oracle for Greek mythology. What would you like to know?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about a god, hero, or myth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consulting the ancient scrolls..."):
            # 1. Chama a sua função RAG com a pergunta do usuário
            resposta_real = rag_answer(prompt)
            
        # 2. Passa a resposta do modelo para o gerador de streaming visual
        response = st.write_stream(stream_llm_response(resposta_real))
        
    st.session_state.messages.append({"role": "assistant", "content": response})
