#!/usr/bin/env python3
"""
Simple test to verify phonetic TTS voice output
"""

from phonetic_tts import PhoneticTTS
import sounddevice as sd
import time

def test_voice_output():
    """Test voice output with clear, distinct words"""
    tts = PhoneticTTS()
    
    # Test simple words that should be recognizable
    test_words = [
        "nine",
        "git", 
        "hook",
        "commit",
        "push",
        "test",
        "audio",
        "voice"
    ]
    
    print("🎤 Testing individual words...")
    
    for word in test_words:
        print(f"🔊 Word: {word}")
        audio = tts.speak(word, industrial=False)  # No effects for clarity
        sd.play(audio, samplerate=44100)
        sd.wait()
        time.sleep(0.3)
    
    print("🎤 Testing phrases...")
    
    test_phrases = [
        "nine inches of git hooks",
        "git commit pushed",
        "testing voice output",
        "audio system working"
    ]
    
    for phrase in test_phrases:
        print(f"🔊 Phrase: {phrase}")
        audio = tts.speak(phrase, industrial=False)
        sd.play(audio, samplerate=44100)
        sd.wait()
        time.sleep(0.5)
    
    print("✅ Voice test complete!")

if __name__ == "__main__":
    test_voice_output()