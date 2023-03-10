import speech_recognition as sr
import openai
import pyttsx3

# Cria um reconhecedor de fala
r = sr.Recognizer()

# Configuração da API do OpenAI
openai.api_key = "COLOQUE_AQUI_SEU_TOKEN_DA_AQUI_OPENAI"
model_engine = "text-davinci-002"

# Configuração da engine de TTS
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[23].id)

# Abre o microfone para captura de áudio
with sr.Microphone() as source:

    while True:
        entrada = input("Digite 1 e começe a falar! Ou 2 para sair:")

        if entrada == '1':
            print("Fale alguma coisa:")

            # Ajusta o nível de ruído do microfone
            r.adjust_for_ambient_noise(source)

            # Define o tempo máximo de escuta em segundos
            r.dynamic_energy_threshold = False
            r.pause_threshold = 1.0
            r.phrase_threshold = 0.5
            r.non_speaking_duration = 0.5

            # Captura o áudio a partir do microfone com tempo limite
            audio = r.listen(source, timeout=5)

            try:
                # Usa o reconhecedor de fala para converter o áudio em texto
                text = r.recognize_google(audio, language='pt-BR')
                print("Você disse: {}".format(text))

                # Monta a requisição para a API do OpenAI
                prompt = f"Conversa com o OpenAI:\n\nVocê: {text}\nAI:"
                response = openai.Completion.create(
                    engine=model_engine,
                    prompt=prompt,
                    max_tokens=3999,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                # Exibe e vocaliza a resposta do OpenAI
                if response:
                    result = response.choices[0].text.strip()
                    print("OpenAI respondeu: {}".format(result))
                    engine.say(result)
                    engine.runAndWait()
                else:
                    print("Erro ao enviar texto para o OpenAI: {}".format(response.status))
            except sr.UnknownValueError:
                print("Não entendi o que você disse")
            except sr.RequestError as e:
                print("Não foi possível se comunicar com o serviço de reconhecimento de fala; {0}".format(e))
        elif entrada == '2':
            print("Parando de escutar...")
            break
        else:
            print("Entrada inválida! Digite 1 para iniciar a escuta ou 2 para parar.")
