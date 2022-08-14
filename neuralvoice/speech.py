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

    speaker.say("what do you want to write onto your note list?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = note.lower()

            with open(filename, 'w') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()
        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you Please repeat")
            speaker.runAndWait()


def add_todo():
    global recognizer

    speaker.say("what to do do you want to add?")
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
                speaker.say(f"I added {item} in to the to do list")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you Please repeat")
            speaker.runAndWait()


def show_todo():
    global recognizer

    speaker.say("The item in your to do list are the following")
    for item in todo_lst:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello. What can i do for you?")
    speaker.runAndWait()


def curiosity():
    speaker.say("My name is VaporWave I was created by Piergiuseppe Di Pilla, part of Pier's knowledge flows freely "
                "in my source code. I'm a CyberLife project")
    speaker.runAndWait()


def byebye():
    speaker.say("Bye")
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
print("the boot is ready, just talk:")

while True:

    try:
        with speech_recognition.Microphone() as mic:
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
        speaker.say("I did not understand you Please repeat")
        speaker.runAndWait()
