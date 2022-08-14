from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys

recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 160)

todo_lst = ['Go shopping', 'clean room', 'record video']


def create_note():
    global recognizer

    speaker.say("Cosa vuoi che io aggiunga nella lista?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Scegli un filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = note.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"Operazione effettuata con successo...ho creato:{filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("Non ho capito...ripeti grazie")
            speaker.runAndWait()


def add_todo():
    global recognizer

    speaker.say("cosa vuoi che io aggiunga alla lista?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_lst.append(item)
                done = True
                speaker.say(f"go aggiunto l'oggetto {item} nella tua lista")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("Non ho capito, ripeti grazie")
            speaker.runAndWait()


def show_todo():
    global recognizer

    speaker.say("gli oggetti nella tua to do list sono i seguenti:")
    for item in todo_lst:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("CIAO. Cosa posso far per te?")
    speaker.runAndWait()


def curiosity():
    speaker.say("Il mio nome è Vapur Weive...sono stato creato da Piergiuseppe Di Pilla...parte della conoscenza di "
                "Pier scorre "
                "libera nel mio codice sorgente...e "
                "Sono un progetto CyberLife in fase di addestramento")
    speaker.runAndWait()


def byebye():
    speaker.say("Ciao alla prossima")
    speaker.runAndWait()
    sys.exit(0)


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "curiosity": curiosity,
    "exit": byebye,
    "add_todo": add_todo,
    "show_todo": show_todo

}

assistant = GenericAssistant('intentsSpeech.json', intent_methods=mappings)
assistant.train_model()
print("il bot è pronto, ora tocca a te, parla:")

while True:
    count = 0
    while count <= 3:
        try:
            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                message = recognizer.recognize_google(audio)
                message = message.lower()

            assistant.request(message)

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("Non ho capito...ripeti grazie")
            speaker.runAndWait()
            count = count + 1
            print(count)
    if count >= 4:
        speaker.say("Non capisco se ci sei ancora?... non ti sento... a breve mi iberno se non parli")
        byebye()
