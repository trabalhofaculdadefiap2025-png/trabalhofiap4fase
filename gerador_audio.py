from gtts import gTTS
import os

# O texto que simula a paciente com risco de depressão pós-parto e dor física
texto = "Olá doutor, sinto muita tristeza e exaustão extrema desde o parto. Não tenho ânimo para nada e sinto uma dor aguda no abdômen que me preocupa muito."

print("Gerando áudio de simulação...")
tts = gTTS(text=texto, lang='pt')
tts.save("teste_paciente.mp3")
print("✅ Arquivo 'teste_paciente.mp3' gerado com sucesso!")