#!/usr/bin/env python3
"""
Phonetic text-to-speech system for Nine Inches of Git Hooks
"""

import numpy as np
import sounddevice as sd
import re
import time
from typing import List, Optional

from phonetic_data import PHONEME_FORMANTS, WORD_PHONEMES, LETTER_PHONEMES
from constants import SAMPLE_RATE


class PhoneticTTS:
    """Simple phonetic text-to-speech system"""
    def __init__(self):
        """Initialize TTS with phoneme data."""
        self.phoneme_formants = PHONEME_FORMANTS
        self.word_phonemes = WORD_PHONEMES
        self.letter_phonemes = LETTER_PHONEMES

    def text_to_phonemes(self, text: str) -> List[str]:
        """Convert text to phonemes"""
        # Clean and lowercase text
        text = re.sub(r"[^\w\s]", "", text.lower())
        words = text.split()

        phonemes = []
        for word in words:
            if word in self.word_phonemes:
                phonemes.extend(self.word_phonemes[word])
            else:
                # For unknown words, use letter-to-phoneme mapping
                for letter in word:
                    if letter in self.letter_phonemes:
                        phonemes.extend(self.letter_phonemes[letter])
                phonemes.append("sil")  # Add silence between words

        return phonemes

    def synthesize_phonemes(
        self, phonemes: List[str], sample_rate: int = SAMPLE_RATE
    ) -> np.ndarray:
        """Synthesize audio from phonemes"""
        audio = np.zeros(0)
        phoneme_duration = 0.1  # 100ms per phoneme

        for phoneme in phonemes:
            if phoneme in self.phoneme_formants:
                f1, f2, f3 = self.phoneme_formants[phoneme]

                # Create phoneme audio
                duration = phoneme_duration
                samples = int(duration * sample_rate)
                t = np.linspace(0, duration, samples)

                # Create formant synthesis
                phoneme_audio = np.zeros(samples)

                # Add fundamental frequency
                fundamental = 120 if phoneme != "sil" else 0
                if fundamental > 0:
                    phoneme_audio += 0.5 * np.sin(2 * np.pi * fundamental * t)

                # Add formants
                if f1 > 0:
                    phoneme_audio += 0.3 * np.sin(2 * np.pi * f1 * t)
                if f2 > 0:
                    phoneme_audio += 0.2 * np.sin(2 * np.pi * f2 * t)
                if f3 > 0:
                    phoneme_audio += 0.1 * np.sin(2 * np.pi * f3 * t)

                # Add some noise for naturalness
                if phoneme != "sil":
                    noise = np.random.normal(0, 0.05, samples)
                    phoneme_audio += noise

                # Apply envelope
                envelope = np.ones(samples)
                if len(phoneme_audio) > 10:
                    # Quick attack and release
                    attack_samples = min(10, len(phoneme_audio) // 4)
                    release_samples = min(15, len(phoneme_audio) // 4)

                    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                    envelope[-release_samples:] = np.linspace(1, 0, release_samples)

                phoneme_audio = phoneme_audio * envelope

                # Concatenate
                audio = np.concatenate([audio, phoneme_audio])

        return audio

    def speak(self, text: str, industrial: bool = True) -> np.ndarray:
        """Convert text to speech with optional industrial effects"""
        phonemes = self.text_to_phonemes(text)
        audio = self.synthesize_phonemes(phonemes)

        if industrial:
            audio = self.apply_industrial_effects(audio)

        return audio

    def apply_industrial_effects(self, audio: np.ndarray) -> np.ndarray:
        """Apply industrial effects to audio"""
        # Add distortion
        audio = np.tanh(audio * 2)

        # Add noise
        noise = np.random.normal(0, 0.1, len(audio))
        audio = audio + noise

        # Add some metallic resonances
        t = np.linspace(0, len(audio) / SAMPLE_RATE, len(audio))
        for freq in [200, 400, 800]:
            resonance = 0.05 * np.sin(2 * np.pi * freq * t)
            audio = audio + resonance

        # Normalize
        audio = audio / np.max(np.abs(audio) + 1e-8)

        return audio


# Test function
def test_phonetic_tts():
    """Test the phonetic TTS system"""

    tts = PhoneticTTS()

    # Test phrases
    test_phrases = [
        "Nine Inches of Git Hooks",
        "Testing audio output",
        "Git commit message",
        "Voice synthesis working",
        "Industrial sounds activated",
    ]

    print("Testing Phonetic TTS System")

    for phrase in test_phrases:
        print(f"Saying: '{phrase}'")
        audio = tts.speak(phrase, industrial=True)
        sd.play(audio, samplerate=SAMPLE_RATE)
        sd.wait()
        time.sleep(0.5)

    print("Phonetic TTS test complete!")


if __name__ == "__main__":
    test_phonetic_tts()
