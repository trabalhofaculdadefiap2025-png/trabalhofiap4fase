import os
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from roboflow import Roboflow
from dotenv import load_dotenv

# Carrega as chaves do arquivo .env
load_dotenv()


class VideoAnalyzer:
    def __init__(self):
        """
        Inicializa o motor duplo: YOLOv8 (Especialista) + Gemini (Contextual).
        """
        # 1. CONFIGURAÇÃO ROBOFLOW (YOLOv8)
        self.rf_api_key = os.getenv("ROBOFLOW_API_KEY")
        if not self.rf_api_key:
            print("⚠️ Erro: ROBOFLOW_API_KEY não encontrada.")

        self.rf = Roboflow(api_key=self.rf_api_key)

        try:
            # Conecta ao workspace e projeto (Versão 2 é a que acabou de treinar)
            self.project = self.rf.workspace("alessandra-dev").project("sangramento_cirurgico")
            self.yolo_model = self.project.version(2).model
            print("✅ Modelo YOLOv8 (Versão 2) carregado com sucesso.")
        except Exception as e:
            self.yolo_model = None
            print(f"⚠️ Aviso: Não foi possível carregar o YOLOv8: {e}")

        # 2. CONFIGURAÇÃO VERTEX AI (Gemini Fallback)
        # Usamos o mesmo padrão do seu projeto Natura que já deu certo
        self.creds_path = os.path.abspath('google_credentials_exemplo.json')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.creds_path

        # O ID do seu projeto no GCP
        self.project_id = ""
        self.location = ""

        try:
            vertexai.init(project=self.project_id, location=self.location)
            # Usando o modelo Pro para análise profunda de vídeo
            self.gemini_model = GenerativeModel("gemini-1.5-pro")
            print(f"✅ Gemini 1.5 Pro (Vertex AI) pronto para Fallback.")
        except Exception as e:
            print(f"❌ Erro ao inicializar Vertex AI: {e}")

    def analyze_video(self, video_path):
        """
        Tenta detectar sangramento com YOLO. Se não encontrar nada ou houver erro,
        o Gemini analisa o contexto clínico do vídeo.
        """
        resultados_yolo = None

        # Passo 1: Tentativa com YOLOv8 especializado
        if self.yolo_model:
            try:
                print(f"🔍 Analisando com YOLOv8: {video_path}")
                prediction = self.yolo_model.predict(video_path, confidence=40).json()

                # Se encontrou algo, retornamos a detecção do especialista
                if prediction.get('predictions') and len(prediction['predictions']) > 0:
                    return {
                        "origem": "YOLOv8 Especialista (Roboflow)",
                        "status": "Detecção de Objetos Ativa",
                        "detalhes": prediction['predictions'],
                        "mensagem": "⚠️ Possível sangramento detectado via Visão Computacional."
                    }
                else:
                    print("ℹ️ YOLO não encontrou padrões de sangramento. Acionando Fallback...")
            except Exception as e:
                print(f"⚠️ Erro no processamento YOLO: {e}")

        # Passo 2: Fallback para o Gemini 1.5 Pro
        return self.run_gemini_fallback(video_path)

    def run_gemini_fallback(self, video_path):
        """
        Envia o vídeo para o Gemini analisar o cenário cirúrgico completo.
        """
        try:
            print(f"🚀 [IA Multimodal] Iniciando análise contextual de vídeo...")

            with open(video_path, "rb") as f:
                video_bytes = f.read()

            # Criando a 'Part' do vídeo para o Vertex AI
            video_part = Part.from_data(data=video_bytes, mime_type="video/mp4")

            prompt = """
            Você é um Advisor Cirúrgico de alta senioridade. 
            O detector de objetos especializado não identificou hemorragias óbvias. 
            Analise este vídeo cirúrgico e descreva:
            1. O estado geral dos tecidos (há sinais de isquemia ou inflamação?).
            2. Se há presença de fluidos anômalos que não foram classificados como sangue.
            3. Algum comportamento de risco no manuseio dos instrumentos.

            Retorne um parecer consultivo para o médico responsável.
            """

            response = self.gemini_model.generate_content([prompt, video_part])

            return {
                "origem": "Gemini 1.5 Pro (Fallback Contextual)",
                "status": "Análise de IA Generativa",
                "analise": response.text,
                "mensagem": "✅ Análise de contexto concluída. Revisão humana recomendada."
            }
        except Exception as e:
            return {"status": "erro", "detalhe": f"Falha crítica na análise multimodal: {str(e)}"}