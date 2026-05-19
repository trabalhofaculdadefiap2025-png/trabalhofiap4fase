import streamlit as st
import json
import os
from datetime import datetime

# Importações dos seus módulos de IA
try:
    from scripts.audio_analyzer import AudioAnalyzer
    from scripts.video_analyzer import VideoAnalyzer
except ImportError as e:
    st.error(f"Erro ao importar scripts: {e}")

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="HealthTech | Portal Feminino",
    page_icon="🏥",
    layout="wide"
)

# --- ESTILIZAÇÃO CUSTOMIZADA (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 3em; 
        background-color: #e86e1b; 
        color: white; 
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover { background-color: #d35400; border: none; }
    .patient-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #e86e1b; 
        margin-bottom: 20px; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05); 
    }
    .sidebar-info { 
        padding: 15px; 
        background-color: #e3f2fd; 
        border-radius: 10px; 
        color: #0d47a1; 
        font-size: 0.9em; 
    }
    </style>
    """, unsafe_allow_html=True)


# --- FUNÇÕES DE DADOS ---
def salvar_no_historico(dados):
    arquivo = 'historico_pacientes.json'
    historico = []
    if os.path.exists(arquivo):
        with open(arquivo, 'r', encoding='utf-8') as f:
            try:
                historico = json.load(f)
            except:
                historico = []
    historico.append(dados)
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)


def carregar_historico():
    if os.path.exists('historico_pacientes.json'):
        with open('historico_pacientes.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []


def main():
    # --- BARRA LATERAL (ACESSO E IDENTIFICAÇÃO) ---
    with st.sidebar:
        st.markdown("### 🔐 Acesso Restrito")
        st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)

        id_acesso = st.text_input("🔑 ID de Acesso do Hospital:", placeholder="Ex: HT-12345")

        st.markdown(
            '<div class="sidebar-info">O seu ID foi fornecido pela recepção no primeiro atendimento para garantir sua privacidade.</div>',
            unsafe_allow_html=True)

        st.divider()
        st.caption("🚀 Fase 4 - Tech Challenge")
        st.caption("Versão 1.0.4 - IA Multimodal")

    # --- TÍTULO PRINCIPAL ---
    st.title("🏥 Sistema de Monitoramento e Apoio à Saúde Feminina")
    st.subheader("Integração Multimodal: Visão Computacional e IA Generativa")
    st.markdown("---")

    # --- NAVEGAÇÃO POR ABAS ---
    aba_paciente, aba_medico = st.tabs(["🚺 Área da Paciente (Triagem)", "👨‍⚕️ Área do Médico (Dashboard)"])

    # --- ABA DA PACIENTE ---
    with aba_paciente:
        if not id_acesso:
            st.warning("⚠️ Por favor, insira seu **ID de Acesso** na barra lateral para liberar as funcionalidades.")
        else:
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 📝 Relato de Sintomas")
                nome_paciente = st.text_input("Nome Completo:", "Alessandra Rodrigues")

                st.markdown('<div class="patient-card">', unsafe_allow_html=True)
                audio_file = st.file_uploader("Suba seu áudio relatando sintomas (.wav ou .mp3)", type=["wav", "mp3"])
                st.markdown('</div>', unsafe_allow_html=True)

                if audio_file and st.button("🚀 Enviar para Análise Prioritária"):
                    with st.spinner("Enviando relato para a equipe médica..."):
                        temp_path = os.path.join(os.getcwd(), "temp_atendimento.wav")

                        try:
                            with open(temp_path, "wb") as f:
                                f.write(audio_file.getvalue())

                            # A IA processa nos bastidores
                            analyzer = AudioAnalyzer()
                            resultado_texto = analyzer.analyze_audio_clinical(temp_path)

                            # Salva os dados no prontuário (JSON)
                            registro = {
                                "paciente": nome_paciente,
                                "id_hospital": id_acesso,
                                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                "ia_output": resultado_texto,  # O médico verá isso
                                "status": "Pendente"
                            }
                            salvar_no_historico(registro)

                            # MENSAGEM PARA A PACIENTE: Apenas confirmação de sucesso
                            st.success("✅ Relato enviado com sucesso!")
                            st.info(
                                "Sua análise foi encaminhada ao Dashboard do médico responsável. Por favor, aguarde o atendimento.")

                            # Note que REMOVEMOS o st.markdown(f"Análise da IA: {resultado_texto}") daqui!

                        except Exception as e:
                            st.error(f"Erro no envio: {e}")

            with col2:
                st.info("""
                **Como funciona o atendimento?**
                1. Você grava ou sobe um áudio relatando como se sente.
                2. Nossa IA processa o conteúdo buscando sinais de alerta.
                3. O médico recebe um resumo priorizado no dashboard dele.
                """)
                st.image("https://cdn-icons-png.flaticon.com/512/3843/3843105.png", width=250)

    # --- ABA DO MÉDICO ---
    with aba_medico:
        st.markdown("### 👨‍⚕️ Dashboard de Decisão Clínica")
        col_lista, col_detalhe = st.columns([1, 2])

        with col_lista:
            st.markdown("#### 📋 Fila de Triagem")
            historico = carregar_historico()

            if not historico:
                st.write("Nenhum atendimento na fila.")
            else:
                for idx, item in enumerate(reversed(historico)):
                    p_nome = item.get('paciente', 'Paciente')
                    p_id = item.get('id_hospital', 'S/ID')
                    p_data = item.get('data', '--/--')
                    icone = "🔴" if "Alerta" in item.get('ia_output', '') else "🟢"

                    if st.button(f"{icone} {p_nome} ({p_id}) - {p_data}", key=f"hist_{idx}"):
                        st.session_state['atendimento_atual'] = item

        with col_detalhe:
            if 'atendimento_atual' in st.session_state:
                at = st.session_state['atendimento_atual']
                st.markdown(f"""
                <div class="patient-card">
                    <h4>Prontuário: {at.get('paciente')}</h4>
                    <p><b>ID Hospitalar:</b> {at.get('id_hospital')} | <b>Data:</b> {at.get('data')}</p>
                    <hr>
                    <strong>Análise Gerada pela IA:</strong><br>
                    {at.get('ia_output')}
                </div>
                """, unsafe_allow_html=True)

                parecer_medico = st.text_area("✍️ Digite sua prescrição ou parecer final:")
                if st.button("Confirmar e Finalizar Atendimento"):
                    st.success("Parecer médico integrado ao prontuário com sucesso!")
            else:
                st.info("Selecione um paciente na lista ao lado para ver os detalhes da triagem.")

        st.divider()
        st.subheader("🎥 Análise de Vídeo Cirúrgico")
        video_input = st.file_uploader("Subir vídeo do procedimento (.mp4)", type=["mp4"])

        if video_input:
            st.video(video_input)
            if st.button("🔍 Analisar com Visão Computacional"):
                with st.spinner("O motor híbrido (YOLOv8 + Gemini) está processando o vídeo..."):
                    temp_vid_path = os.path.join(os.getcwd(), "temp_video_clinico.mp4")
                    with open(temp_vid_path, "wb") as f:
                        f.write(video_input.getvalue())

                    try:
                        video_tool = VideoAnalyzer()
                        resultado = video_tool.analyze_video(temp_vid_path)

                        if resultado:
                            st.markdown("### 📊 Resultado da Análise")

                            # Tenta pegar a origem de qualquer jeito
                            origem = resultado.get('origem') or resultado.get('source') or "IA Híbrida"
                            st.markdown(f"**Origem:** `{origem}`")

                            st.markdown('<div class="patient-card">', unsafe_allow_html=True)

                            # --- AJUSTE AQUI: Tenta todas as combinações possíveis de nomes ---
                            texto_analise = (
                                    resultado.get('analise') or
                                    resultado.get('analysis') or
                                    resultado.get('ia_output')
                            )

                            if texto_analise:
                                st.info(texto_analise)

                            deteccoes = (
                                    resultado.get('detalhes') or
                                    resultado.get('detections') or
                                    resultado.get('predictions')
                            )

                            if deteccoes:
                                st.warning(f"Foram detectados {len(deteccoes)} pontos de interesse clínico.")
                                st.json(deteccoes)

                            # --- LINHA DE SEGURANÇA: Se nada acima funcionou, mostra o que veio ---
                            if not texto_analise and not deteccoes:
                                st.write("Dados brutos da IA:", resultado)

                            if "erro" in resultado or "error" in resultado:
                                st.error(resultado.get("erro") or resultado.get("error"))

                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.error("A análise retornou vazia. Verifique a conexão com as APIs.")

                    except Exception as e:
                        st.error(f"Erro ao conectar com o motor de IA: {e}")


if __name__ == "__main__":
    main()