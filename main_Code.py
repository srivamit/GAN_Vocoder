from googletrans import Translator
import pandas as pd
import re
import os
from gtts import gTTS
import pygame


# Load your dataset containing acronyms and sentences
dataset_path = "slang.csv"  # Update this with your dataset path
acronym_data = pd.read_csv(dataset_path)

# Function to build a dictionary mapping acronyms and slangs to sentences
def build_dictionary(data):
    acronym_dict = {}
    for index, row in data.iterrows():
        term = row['acronym'].lower()
        sentence = row['expansion']
        if term not in acronym_dict:
            acronym_dict[term] = sentence
        acronym_dict[sentence.lower()] = sentence  # Add sentence itself for slang
    return acronym_dict

# Build the dictionary
dictionary = build_dictionary(acronym_data)

# Function to resolve acronyms and slangs in a sentence
def resolve_sentence(sentence):
    # Tokenize the sentence
    tokens = re.findall(r'\b\w+\b', sentence)
    result = []
    for token in tokens:
        # Check if token is in dictionary
        if token.lower() in dictionary:
            result.append(dictionary[token.lower()])
        else:
            result.append(token)
    return ' '.join(result)

# Function to translate a sentence to a target language
def translate_sentence(sentence, target_language='en'):
    translator = Translator()
    translation = translator.translate(sentence, dest=target_language)
    return translation.text

# Function to speak the translated result
def speak_text(text,lang):
    tts = gTTS(text=text, lang=lang)
    tts.save("greeting.mp3")
    play_audio("greeting.mp3")
def play_audio(file_path):
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Adjust as needed
    pygame.mixer.music.stop()
    pygame.mixer.quit()


    # # Delete the file
    os.remove(file_path)


# Main loop for user interaction
while True:
    user_input = input("Enter a sentence (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        print("Exiting...")
        break
    else:
        resolved_sentence = resolve_sentence(user_input)
        print("Resolved Sentence:", resolved_sentence)
        print("Translation Options:")
        print("1. French (fr)")
        print("2. Spanish (es)")
        print("3. German (de)")
        print("4. Italian (it)")
        print("5. Russian (ru)")
        print("6. Chinese (zh-CN)")
        print("7. Hindi (hi)")
        print("8. English(en)")
        print("9. Japanese(ja)")
        target_language = input("Enter the number of the desired language option: ")
        if target_language.lower() == 'exit':
            print("Exiting...")
            break
        elif target_language == '1':
            translated_sentence = translate_sentence(resolved_sentence, target_language='fr')        
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='fr')
        elif target_language == '2':
            translated_sentence = translate_sentence(resolved_sentence, target_language='es')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='es')
        elif target_language == '3':
            translated_sentence = translate_sentence(resolved_sentence, target_language='de')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='de')
        elif target_language == '4':
            translated_sentence = translate_sentence(resolved_sentence, target_language='it')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='it')
        elif target_language == '5':
            translated_sentence = translate_sentence(resolved_sentence, target_language='ru')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='ru')
        elif target_language == '6':
            translated_sentence = translate_sentence(resolved_sentence, target_language='zh-CN')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='zh-CN')
        elif target_language == '7':
            translated_sentence = translate_sentence(resolved_sentence, target_language='hi')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='hi')
        elif target_language == '8':
            translated_sentence = translate_sentence(resolved_sentence, target_language='en')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='en')
        elif target_language == '9':
            translated_sentence = translate_sentence(resolved_sentence, target_language='ja')
            print("Translated Result:", translated_sentence)
            speak_text(translated_sentence,lang='ja')
        else:
            print("Invalid option. Please enter a number from 1 to 8.")
            continue
