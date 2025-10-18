import os
import sys
import pyttsx3
import speech_recognition as sr
from datetime import datetime
from config import GEMINI_API_KEY, QUESTION_BANK_URL, INTERVIEW_CATEGORIES

# 1. Gemini API: Get Interview Question
try:
    from google.genai import Client
except ImportError:
    print("google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

def get_interview_question(category):
    client = Client(api_key=GEMINI_API_KEY)
    prompt = f"Generate a unique product interview question in '{category}'. The question should be suitable for an interview simulation.Do not include explanations, meta-comments, or any additional text"
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text.strip()

# 2. TTS: Speak Question, Save Audio
def speak_text(text, audio_filename):
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_filename)
    engine.runAndWait()

# 3. STT: Record User Answer, Transcribe
def record_and_transcribe(audio_filename):
    r = sr.Recognizer()
    r.pause_threshold = 2.0
    # print(sr.Microphone.list_microphone_names())
    with sr.Microphone() as source:
        print("Speak your answer (Press Ctrl+C to exit):")
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        with open(audio_filename, 'wb') as f:
            f.write(audio.get_wav_data())
        try:
            text = r.recognize_google(audio)
            print(f"User (transcribed): {text}")
        except Exception as e:
            text = f"(Unintelligible/ERROR: {e})"
            print(f"User (transcribed): {text}")
        return text
    
"""
To let the user manually end answer recording by pressing Ctrl+C (instead of automatic silence detection)


import sounddevice as sd
import soundfile as sf

def record_and_transcribe(audio_filename):
    import queue

    q = queue.Queue()
    samplerate = 16000  # 16kHz works fine for STT
    channels = 1
    print("Speak your answer. Press Ctrl+C when done, then transcription will process...")

    def callback(indata, frames, time, status):
        q.put(indata.copy())

    try:
        with sf.SoundFile(audio_filename, mode='w', samplerate=samplerate, channels=channels) as file:
            with sd.InputStream(samplerate=samplerate, channels=channels, callback=callback):
                print("Recording... (Ctrl+C to finish)")
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print("\nRecording stopped. Transcribing audio...")
    except Exception as e:
        print(f"Recording failed: {e}")
        return ""
    
    # Now transcribe the completed audio file
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.AudioFile(audio_filename) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data)
            print(f"User (transcribed): {text}")
        except Exception as e:
            text = f"(Unintelligible/ERROR: {e})"
            print(f"User (transcribed): {text}")
    return text

"""

# 4. Subtitle Display and Save
def display_subtitle(text, who, subtitle_file):
    print(f"[{who}]: {text}")
    timestamp = datetime.now().strftime('%H:%M:%S')
    with open(subtitle_file, 'a', encoding='utf-8') as f:
        f.write(f"{timestamp} [{who}]: {text}\n")

# 5. Save Logs and Metadata
def log_conversation_round(data):
    log_file = os.path.join('conversation_logs', 'interview_log.txt')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(str(data) + '\n')

# 6. CLI Interview Loop
def run_interview():
    # Ensure artifact directories
    for folder in ['audio', 'subtitles', 'conversation_logs']:
        os.makedirs(folder, exist_ok=True)

    print("Welcome to AI Interviewer!")
    print("Select the type of interview:")
    for idx, cat in enumerate(INTERVIEW_CATEGORIES):
        print(f"{idx+1}. {cat}")
    while True:
        try:
            cat_idx = int(input("Choose a category number: ")) - 1
            if 0 <= cat_idx < len(INTERVIEW_CATEGORIES):
                break
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Please enter a valid number.")

    category = INTERVIEW_CATEGORIES[cat_idx]

    # 1. Fetch and present an interview question
    question = get_interview_question(category)
    q_audio_file = os.path.join('audio', 'question.wav')
    q_subtitle_file = os.path.join('subtitles', 'question.srt')

    display_subtitle(question, 'AI', q_subtitle_file)
    speak_text(question, q_audio_file)

    # 2. Capture user's spoken answer and transcribe
    a_audio_file = os.path.join('audio', 'user_answer.wav')
    a_subtitle_file = os.path.join('subtitles', 'answer.srt')

    answer = record_and_transcribe(a_audio_file)
    display_subtitle(answer, 'User', a_subtitle_file)

    # 3. Log the round, save metadata
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'category': category,
        'question': question,
        'answer': answer,
        'question_audio_file': q_audio_file,
        'answer_audio_file': a_audio_file,
        'question_subtitle_file': q_subtitle_file,
        'answer_subtitle_file': a_subtitle_file
    }
    log_conversation_round(metadata)

    print("\nInterview round complete!")
    print(f"Artifacts saved: \n- {q_audio_file}\n- {a_audio_file}\n- {q_subtitle_file}\n- {a_subtitle_file}")
    print("Conversation metadata logged in 'conversation_logs/interview_log.txt'")

if __name__ == "__main__":
    run_interview()
