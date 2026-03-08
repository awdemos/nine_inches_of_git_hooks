#!/usr/bin/env python3
"""
Test script for 10-second audio playback with industrial effects
"""

import sounddevice as sd
import numpy as np
import time
import tempfile
import os
from gtts import gTTS

def create_test_audio(duration: int = 10) -> np.ndarray:
    """Create test audio with industrial effects"""
    sample_rate = 44100
    samples = int(duration * sample_rate)
    
    # Create time array
    t = np.linspace(0, duration, samples)
    
    # Create multiple frequency components for industrial sound
    audio = np.zeros(samples)
    
    # Add fundamental frequencies
    freqs = [110, 220, 440, 880]  # A notes
    for i, freq in enumerate(freqs):
        amplitude = 0.3 / (i + 1)
        # Add some frequency modulation
        freq_mod = freq + 10 * np.sin(2 * np.pi * 2 * t)
        audio += amplitude * np.sin(2 * np.pi * freq_mod * t)
    
    # Add harmonics for richness
    for harmonic in range(2, 6):
        for base_freq in freqs[:2]:  # Only use lower frequencies for harmonics
            freq = base_freq * harmonic
            amplitude = 0.1 / harmonic
            audio += amplitude * np.sin(2 * np.pi * freq * t)
    
    # Add noise for industrial texture
    noise = np.random.normal(0, 0.1, samples)
    audio += noise
    
    # Apply distortion
    audio = np.tanh(audio * 2)
    
    # Add some rhythmic elements
    beat_freq = 2  # 2 beats per second
    beat = np.sin(2 * np.pi * beat_freq * t)
    audio = audio * (0.7 + 0.3 * beat)
    
    # Normalize
    audio = audio / np.max(np.abs(audio))
    
    return audio

def create_voice_audio(text: str = "Testing Nine Inches of Git Hooks audio output!") -> np.ndarray:
    """Create voice-like audio using formant synthesis"""
    # Estimate duration based on text length (rough estimate)
    duration = len(text) * 0.1
    sample_rate = 44100
    samples = int(duration * sample_rate)
    
    # Create time array
    t = np.linspace(0, duration, samples)
    
    # Create voice-like synthesis using formants
    audio = np.zeros(samples)
    
    # Fundamental frequency (pitch) for male voice
    fundamental_freq = 120  # Hz
    
    # Add pitch variation for natural speech
    pitch_variation = 20 * np.sin(2 * np.pi * 3 * t)  # 3 Hz variation
    current_freq = fundamental_freq + pitch_variation
    
    # Add formants (vocal tract resonances)
    formants = [
        (800, 0.8),   # First formant
        (1200, 0.6),  # Second formant
        (2800, 0.4),  # Third formant
        (3500, 0.3),  # Fourth formant
    ]
    
    # Create voice-like sound
    for formant_freq, amplitude in formants:
        # Formant frequencies scale with fundamental
        scaled_freq = formant_freq * (current_freq / fundamental_freq)
        audio += amplitude * np.sin(2 * np.pi * scaled_freq * t)
    
    # Add harmonics for richness
    for harmonic in range(2, 6):
        harmonic_freq = current_freq * harmonic
        amplitude = 0.3 / harmonic
        audio += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
    
    # Add some noise for breathiness
    breath_noise = np.random.normal(0, 0.05, samples)
    # Apply simple low-pass filter to breath noise
    for i in range(1, len(breath_noise)):
        breath_noise[i] = 0.8 * breath_noise[i] + 0.2 * breath_noise[i-1]
    audio += breath_noise
    
    # Create amplitude envelope for speech-like rhythm
    # Simulate syllables with amplitude modulation
    syllable_rate = 3  # syllables per second
    envelope = 0.5 + 0.5 * np.sin(2 * np.pi * syllable_rate * t)
    audio = audio * envelope
    
    # Normalize
    audio = audio / np.max(np.abs(audio))
    
    return audio

def play_audio_test() -> None:
    """Play test audio for 10 seconds"""
    print("🎸 Starting 10-second audio test...")
    
    # Test 1: Pure industrial sound
    print("🔊 Playing industrial sound test...")
    audio1 = create_test_audio(3)
    sd.play(audio1, samplerate=44100)
    sd.wait()
    time.sleep(0.5)
    
    # Test 2: Voice synthesis
    print("🎤 Playing voice synthesis test...")
    audio2 = create_voice_audio("Nine Inches of Git Hooks is ready!")
    sd.play(audio2, samplerate=44100)
    sd.wait()
    time.sleep(0.5)
    
    # Test 3: Combined industrial + voice
    print("🎸 Playing combined industrial voice test...")
    # Create mixed audio with same duration
    industrial = create_test_audio(2)
    voice = create_voice_audio("Git commit pushed!")
    # Make arrays same length
    min_len = min(len(industrial), len(voice))
    mixed = 0.6 * industrial[:min_len] + 0.4 * voice[:min_len]
    mixed = mixed / np.max(np.abs(mixed))
    sd.play(mixed, samplerate=44100)
    sd.wait()
    
    # Test 4: Voice with different text
    print("🎤 Playing voice with different text...")
    audio4 = create_voice_audio("Testing audio output device successfully!")
    sd.play(audio4, samplerate=44100)
    sd.wait()
    
    print("✅ 10-second audio test complete!")

if __name__ == "__main__":
    play_audio_test()