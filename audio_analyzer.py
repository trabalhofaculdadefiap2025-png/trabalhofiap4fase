import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from dotenv import load_dotenv

load_dotenv()


class AudioAnalyzer:
    def __init__(self):
        """
        Inicializa a conexão com o Vertex AI usando o Service Account JSON.
        """

        self.creds_path = os.path.abspath('google_credentials.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.creds_path

        self.project_id = os.getenv("PROJECT_ID", "caminho do PROJECT_ID ")
        self.location = os.getenv("LOCATION", "localização")

        try:
            vertexai.init(project=self.project_id, location=self.location)

            self.model = GenerativeModel("gemini-1.5-pro")
            print(f"✅ Vertex AI inicializado com sucesso no projeto: {self.project_id}")

        except Exception as e:
            raise Exception(f"❌ Falha ao inicializar Vertex AI: {str(e)}")

    def analyze_audio_clinical(self, audio_path):
        """
        Lê o áudio local, converte para Part (Vertex AI) e solicita a análise.
        """
        try:
            if not os.path.exists(audio_path):
                return f"Erro: Arquivo {audio_path} não encontrado."

            print(f"🧠 [IA] Iniciando análise clínica do áudio: {os.path.basename(audio_path)}")

            with open(audio_path, "rb") as f:
                audio_bytes = f.read()

            mime_type = "audio/mpeg" if audio_path.lower().endswith(".mp3") else "audio/wav"

            audio_part = Part.from_data(data=audio_bytes, mime_type=mime_type)

            prompt_sistema = """
            Você é um assistente de IA especializado em Saúde da Mulher e Design Comportamental.
            Sua missão é realizar um diagnóstico preliminar a partir deste áudio de triagem.

            Analise rigorosamente:
            1. SAÚDE MENTAL: Identifique sinais de exaustão extrema, depressão pós-parto ou ansiedade.
            2. ALERTA FÍSICO: Detecte menções a dores agudas, sangramentos ou complicações pós-cirúrgicas.
            3. SEGURANÇA E REDE: Identifique sinais de vulnerabilidade social ou violência doméstica.

            ESTRUTURA DO OUTPUT:
            - Resumo Executivo (Visão Advisor)
            - Tabela de Riscos (Maturidade Clínica: Reativo | Estável | Alerta)
            - Evidências observadas no relato.
            """

            resposta = self.model.generate_content([prompt_sistema, audio_part])

            return resposta.text

        except Exception as e:
            print(f"   ❌ Erro na chamada da IA: {e}")
            return f"Erro técnico na análise: {str(e)}"


# Bloco para teste rápido direto pelo terminal
if __name__ == "__main__":
    # Garanta que o pip install google-cloud-aiplatform foi executado
    try:
        test = AudioAnalyzer()
        print("Módulo de áudio pronto para uso.")
    except Exception as err:
        print(err)
