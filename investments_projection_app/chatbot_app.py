# chatbot_app.py
import streamlit as st
import os
from llama_cpp import Llama
import torch  # para detectar GPU


def chat_bot_app():
    """
    Função principal do Chatbot usando Streamlit + llama.cpp.
    Detecta GPU disponível e ajusta n_gpu_layers automaticamente.
    """

    # Configurações do modelo
    MODEL_PATH = os.environ.get(
        "LLM_MODEL_PATH", "models/Phi-3-mini-4k-instruct-fp16.gguf"
    )
    N_CTX = int(os.environ.get("LLM_CTX", "4096"))
    N_THREADS = os.cpu_count()/2 or 4

    # Detecta GPU disponível
    if torch.cuda.is_available():
        n_gpu_layers = 99  # número alto para aproveitar a GPU inteira
        device_info = f"GPU detectada: {torch.cuda.get_device_name(0)}"
    else:
        n_gpu_layers = 0  # CPU puro
        device_info = "Nenhuma GPU detectada, usando CPU"

    st.sidebar.info(device_info)

    # Configuração da página Streamlit
    st.set_page_config(
        page_title="Chatbot Local (Streamlit + llama.cpp)",
        page_icon="🤖",
        layout="centered"
    )

    # Carrega o modelo com cache
    @st.cache_resource(show_spinner=True)
    def load_model(model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Modelo não encontrado em: {model_path}")
        llm = Llama(
            model_path=model_path,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            n_gpu_layers=n_gpu_layers,
            verbose=False
        )
        return llm

    llm = load_model(MODEL_PATH)

    # ---------------- UI ----------------
    st.title("🤖 Chatbot Local (Streamlit + llama.cpp)")

    # Configurações do sistema e parâmetros do modelo
    with st.expander("⚙️ Configurações", expanded=False):
        system_prompt = st.text_area(
            "System prompt",
            value=(
                "Você é um assistente de IA que fala só em português. "
                "Você é um professor de investimentos que ensina conceitos básicos "
                "de forma clara e didática para iniciantes. Explique termos financeiros "
            ),
            height=120
        )
        temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
        top_p = st.slider("Top P", 0.1, 1.0, 0.95, 0.05)
        max_tokens = st.slider("Max tokens (resposta)", 64, 2048, 512, 64)

    # Botão para limpar conversa
    cols = st.columns(3)
    with cols[0]:
        if st.button("🧹 Limpar conversa"):
            st.session_state.messages = []

    # Inicializa estado da conversa
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Exibe histórico
    for msg in st.session_state.messages:
        role = "🧑 Você" if msg["role"] == "user" else "🤖 Assistente"
        st.markdown(f"**{role}:** {msg['content']}")

    # Entrada do usuário
    user_input = st.chat_input("Digite sua mensagem...")

    # Função para montar mensagens no formato chat
    def build_messages(system_prompt: str, history: list[dict]):
        msgs = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        msgs.extend(history)
        return msgs

    # Processa input do usuário
    if user_input:
        # Adiciona pergunta ao histórico
        st.session_state.messages.append(
            {"role": "user", "content": user_input})

        # Constrói lista de mensagens
        chat_messages = build_messages(
            system_prompt, st.session_state.messages)

        # Chamada ao modelo com streaming
        with st.spinner("Gerando resposta..."):
            stream = llm.create_chat_completion(
                messages=chat_messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
                stream=True
            )

            # Renderiza resposta enquanto o modelo gera tokens
            assistant_text = ""
            placeholder = st.empty()
            for chunk in stream:
                delta = chunk.get("choices", [{}])[0].get("delta", {})
                token = delta.get("content", "")
                if token:
                    assistant_text += token
                    placeholder.markdown(f"**🤖 Assistente:** {assistant_text}")

            # Salva resposta completa no histórico
            st.session_state.messages.append(
                {"role": "assistant", "content": assistant_text})
            placeholder.markdown(f"**🤖 Assistente:** {assistant_text}")


# Permite execução direta para teste local
# if __name__ == "__main__":
#     chat_bot_app()
