# 🏥 Sistema de Monitoramento e Apoio à Saúde Feminina
### Tech Challenge - Fase 4 | Pós-Tech IA para Negócios

Este repositório contém a solução desenvolvida para o Tech Challenge da Fase 4. O sistema é uma plataforma multimodal (SaMD - Software as a Medical Device) voltada para a saúde da mulher, integrando Visão Computacional e Inteligência Artificial Generativa para apoiar decisões clínicas e triagens de risco.

---

## 🚀 Funcionalidades Principais

1. **Triagem de Áudio Especializada (Saúde Mental e Psicossocial):**
   * Processamento e transcrição de relatos de voz de pacientes.
   * Análise automatizada de tom e contexto para identificação de depressão pós-parto, ansiedade gestacional ou sinais de vulnerabilidade.
   * **Fluxo Ético:** O laudo é encaminhado diretamente ao painel do médico para evitar autodiagnósticos ou ansiedade na paciente.

2. **Análise Híbrida de Vídeo Cirúrgico (Motor Duplo):**
   * **Modelo Especialista (YOLOv8):** Customizado e treinado com mais de 3.200 imagens de laparoscopia ginecológica para detectar sangramento anômalo em tempo real.
   * **Fallback Contextual (Gemini 1.5 Pro):** Caso o modelo de visão computacional detecte baixa confiança (devido a fumaça cirúrgica ou iluminação), a IA Multimodal em nuvem assume a análise para gerar um parecer descritivo dos tecidos e manipulação de instrumentos.

3. **Dashboard Clínico Unificado:**
   * Interface construída em Streamlit isolando a Área da Paciente e o Painel do Médico.
   * Vinculação de prontuários por ID de Acesso Hospitalar com persistência de dados em JSON.

---

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma:

```text
desafio_tecnico_fase4/
├── data/
│   └── yolov8n.pt               # Pesos base do modelo YOLO
├── models/                      # Artefatos locais dos modelos 
├── scripts/
│   ├── audio_analyzer.py        # Motor de análise de áudio (Vertex AI)
│   └── video_analyzer.py        # Motor híbrido de vídeo (Roboflow API + Vertex AI)
├── gerador_audio.py             # Script utilitário para testes de áudio
├── main.py                      # Interface principal e rotas do Streamlit
└── README.md                    # Documentação do projeto
