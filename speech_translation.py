import os
import azure.cognitiveservices.speech as speechsdk

weatherfilename = "male.wav"


def recognize_from_microphone():
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
    speech_translation_config.speech_recognition_language="hi-IN"

    target_language="en"
    speech_translation_config.add_target_language(target_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("Speak into your microphone.")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Recognized: {}".format(translation_recognition_result.text))
        print("""Translated into '{}': {}""".format(
            target_language, 
            translation_recognition_result.translations[target_language]))
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")

recognize_from_microphone()


def translation_once_from_file():
    """performs one-shot speech translation from input from an audio file"""
    weatherfilename = "whatstheweatherlike.wav"

    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'),
        speech_recognition_language='en-US',
        target_languages=('pa', 'hi'))
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)

    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("""Recognized: {}
        Punjabi translation: {}
        Hindi translation: {}""".format(
            result.text, result.translations['pa'], result.translations['hi']))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Translation canceled: {}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(result.cancellation_details.error_details))
            
            
#translation_once_from_file()


def translation_once_with_lid_from_file():
    """performs a one-shot speech translation from an audio file, with at-start language identification"""
    
    endpoint_string = "wss://{}.stt.speech.microsoft.com/speech/universal/v2".format(os.environ.get('SPEECH_REGION'))
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=os.environ.get('SPEECH_KEY'), 
        endpoint=endpoint_string,
        target_languages=('pa', 'hi'))
    audio_config = speechsdk.audio.AudioConfig(filename=weatherfilename)

    auto_detect_source_language_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
        languages=["en-US"])

    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config,
        audio_config=audio_config,
        auto_detect_source_language_config=auto_detect_source_language_config)

    # Starts translation, with single-utterance (one-shot) recognition and language identification
    result = recognizer.recognize_once()
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        src_lang = result.properties[speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult]
        print("""Recognized:
        Detected language: {}
        Recognition result: {}
        Punjabi translation: {}
        Hindi translation: {}""".format(
            src_lang,
            result.text,
            result.translations['pa'],
            result.translations['hi']))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized:\n {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Translation canceled: {}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(result.cancellation_details.error_details))
            
            
#translation_once_with_lid_from_file()