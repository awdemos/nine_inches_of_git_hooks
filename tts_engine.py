#!/usr/bin/env python3
"""
TTS Engine for Nine Inches of Git Hooks
Handles text-to-speech synthesis with industrial effects.
"""

import numpy as np
import tempfile
import os
from typing import Optional
from dataclasses import dataclass

from constants import SAMPLE_RATE, MIN_AUDIO_LENGTH_FOR_FILTER

# Try to import TTS dependencies

# Try to import TTS dependencies
try:
    from chatterbox.tts import ChatterboxTTS

    CHATTERBOX_AVAILABLE = True
except Exception:
    CHATTERBOX_AVAILABLE = False

try:
    from phonetic_tts import PhoneticTTS

    PHONETIC_TTS_AVAILABLE = True
except ImportError:
    PHONETIC_TTS_AVAILABLE = False

try:
    from gtts import gTTS

    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


@dataclass
class TTSConfig:
    """Configuration for TTS synthesis"""

    speed: float = 1.0
    pitch: float = 0.0
    energy: float = 1.0
    emotion: Optional[str] = None


class MockTTS:
    """Mock TTS class that uses enhanced synthetic speech"""

    def tts(self, text: str, config: Optional[TTSConfig] = None) -> np.ndarray:
        """Generate synthetic speech with optional configuration"""
        if config is None:
            config = TTSConfig()

        speed, pitch, energy, emotion = (
            config.speed,
            config.pitch,
            config.energy,
            config.emotion,
        )

        # Generate enhanced synthetic speech with the given parameters
        duration = len(text) * 0.08 / speed
        sample_rate = 44100
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)

        # Create vocal-like synthesis with formants
        fundamental = 150 + pitch * 50
        audio = np.zeros(samples)

        # Add formants for vocal quality
        formants = [
            (800, 0.8),
            (1200, 0.6),
            (2800, 0.4),
            (3500, 0.3),
        ]

        for freq, amp in formants:
            freq_mod = freq + 50 * np.sin(2 * np.pi * 5 * t)
            audio += amp * np.sin(2 * np.pi * freq_mod * t)

        # Add harmonics based on energy
        for harmonic in range(2, int(3 + energy * 3)):
            freq = fundamental * harmonic
            amplitude = 0.3 / harmonic
            audio += amplitude * np.sin(2 * np.pi * freq * t)

        # Apply emotion effects
        if emotion == "angry":
            # Add distortion for angry emotion
            audio = np.tanh(audio * 2)
            # Add noise for aggression
            noise = np.random.normal(0, 0.1, samples)
            audio += noise

        # Normalize
        audio = audio / np.max(np.abs(audio) + 1e-8)

        return audio


def apply_nin_effects(audio: np.ndarray) -> np.ndarray:
    """Apply Nine Inch Nails-style industrial effects to audio"""
    sample_rate = 44100

    # Ensure audio is numpy array
    if not isinstance(audio, np.ndarray):
        audio = np.array(audio)

    # 1. Heavy distortion - multiple stages
    audio = audio / np.max(np.abs(audio))

    # Tube saturation simulation
    audio = np.tanh(audio * 3)

    # Bit crushing for digital distortion
    audio = np.round(audio * 8) / 8

    # 2. Add industrial noise and texture
    noise_floor = np.random.normal(0, 0.05, len(audio))
    audio = audio + noise_floor

    # 3. Create aggressive reverb/echo
    # Multiple delay taps for that industrial warehouse sound
    delays = [0.15, 0.23, 0.31, 0.47]  # Different delay times
    delays_gain = [0.3, 0.2, 0.15, 0.1]

    for delay_time, gain in zip(delays, delays_gain):
        delay_samples = int(delay_time * sample_rate)
        delayed = np.roll(audio, delay_samples)
        delayed[:delay_samples] = 0
        audio = audio + delayed * gain

    # 4. Add some metallic resonances
    # Create resonant frequencies typical in industrial music
    for freq in [200, 400, 800, 1600]:
        resonance = 0.1 * np.sin(2 * np.pi * freq * np.arange(len(audio)) / sample_rate)
        audio = audio + resonance

    # 5. Apply filtering for that telephone/underwater effect
    # Simple high-pass and low-pass filtering
    if len(audio) > MIN_AUDIO_LENGTH_FOR_FILTER:
        # High-pass filter (remove low frequencies)
        audio[1:] = audio[1:] - 0.95 * audio[:-1]

        # Low-pass filter (smooth high frequencies)
        for i in range(1, len(audio)):
            audio[i] = 0.8 * audio[i] + 0.2 * audio[i - 1]

    # 6. Dynamic processing - compression-like effect
    audio = np.tanh(audio * 2)  # Soft limiting

    # 7. Final normalization and limiting
    audio = audio / np.max(np.abs(audio))
    audio = audio * 0.8  # Reduce volume to prevent clipping

    return audio


def create_synthetic_scream(text: str) -> np.ndarray:
    """Create a synthetic scream using advanced industrial effects"""
    duration = len(text) * 0.08  # Faster delivery for more intensity
    sample_rate = 44100
    samples = int(duration * sample_rate)

    # Create time array
    t = np.linspace(0, duration, samples)

    # Create a more vocal-like industrial scream
    # Start with a fundamental frequency that varies like a human scream
    fundamental_freq = 150 + 50 * np.sin(2 * np.pi * 2 * t)  # Modulated fundamental
    audio = np.zeros(samples)

    # Add formant frequencies to make it more vocal-like (like scream formants)
    formants = [
        (800, 0.8),  # First formant
        (1200, 0.6),  # Second formant
        (2800, 0.4),  # Third formant
        (3500, 0.3),  # Fourth formant
    ]

    for freq, amp in formants:
        # Add frequency modulation for scream-like variation
        freq_mod = freq + 100 * np.sin(2 * np.pi * 15 * t)
        audio += amp * np.sin(2 * np.pi * freq_mod * t)

    # Add harsh harmonics for industrial grit
    for harmonic in [2, 3, 4, 5, 6, 7, 8]:
        freq = fundamental_freq * harmonic
        amplitude = 0.3 / harmonic
        # Add some frequency wobble for organic feel
        freq_wobble = freq + 20 * np.sin(2 * np.pi * 8 * t)
        audio += amplitude * np.sign(np.sin(2 * np.pi * freq_wobble * t))

    # Add heavy noise for industrial texture
    noise_floor = np.random.normal(0, 0.15, samples)
    # Add some filtered noise for breathiness
    breath_noise = np.random.normal(0, 0.1, samples)
    # Simple low-pass filter for breath noise
    for i in range(1, len(breath_noise)):
        breath_noise[i] = 0.7 * breath_noise[i] + 0.3 * breath_noise[i - 1]

    audio += noise_floor + breath_noise

    # Apply heavy distortion - multiple stages
    audio = audio / np.max(np.abs(audio))

    # First distortion stage - tube-like saturation
    audio = np.tanh(audio * 4)

    # Second distortion stage - hard clipping
    audio = np.clip(audio * 1.5, -0.9, 0.9)

    # Third distortion stage - bit crushing effect
    audio = np.round(audio * 16) / 16  # Reduce bit depth

    # Create dynamic envelope for scream intensity
    # Quick attack, sustain, then decay
    attack_time = 0.05
    decay_time = 0.3
    attack_samples = int(attack_time * sample_rate)
    decay_samples = int(decay_time * sample_rate)

    envelope = np.ones(samples)
    # Attack
    envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
    # Decay
    if decay_samples < samples:
        envelope[-decay_samples:] = np.linspace(1, 0.1, decay_samples)

    # Add some random volume fluctuations for organic feel
    volume_mod = 1 + 0.1 * np.sin(2 * np.pi * 10 * t)
    envelope *= volume_mod

    audio = audio * envelope

    # Add some reverb/echo for that industrial warehouse sound
    delay_time = 0.15  # 150ms delay
    delay_samples = int(delay_time * sample_rate)
    delayed = np.roll(audio, delay_samples)
    delayed[:delay_samples] = 0
    audio = audio * 0.8 + delayed * 0.2

    # Final normalization and limiting
    audio = audio / np.max(np.abs(audio))
    audio = np.tanh(audio * 0.9)  # Final limiting

    return audio


def create_gtts_industrial(text: str) -> Optional[np.ndarray]:
    """Create industrial voice using Google TTS with NIN-style effects"""
    try:
        # Create Google TTS audio
        tts = gTTS(text=text, lang="en", slow=False)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
            tts.save(tmp_file.name)
            tmp_path = tmp_file.name

        # Read the audio file
        try:
            # Use ffmpeg to convert mp3 to wav if available, otherwise use librosa
            import librosa

            audio, sr = librosa.load(tmp_path, sr=44100)
        except Exception:
            # Fallback: just create synthetic audio
            os.unlink(tmp_path)
            return create_synthetic_scream(text)

        # Clean up temp file
        os.unlink(tmp_path)

        # Apply NIN-style effects
        return apply_nin_effects(audio)

    except Exception as e:
        print(f"Error with gTTS: {e}")
        return create_synthetic_scream(text)


def create_industrial_scream(text: str) -> Optional[np.ndarray]:
    """Generate industrial-style scream using available TTS"""
    try:
        if CHATTERBOX_AVAILABLE:
            # Use ChatterBox TTS
            try:
                tts = ChatterboxTTS.from_pretrained(device="cpu")
                wav = tts.generate(text)
                # Convert to numpy array for industrial effects
                audio = wav.numpy()
                return apply_nin_effects(audio)
            except Exception as chatterbox_error:
                print(f"ChatterBox TTS failed: {chatterbox_error}")
                # Fall back to phonetic TTS
                if PHONETIC_TTS_AVAILABLE:
                    tts = PhoneticTTS()
                    audio = tts.speak(text, industrial=True)
                    return audio
                elif GTTS_AVAILABLE:
                    return create_gtts_industrial(text)
                else:
                    tts = MockTTS()
                    config = TTSConfig(
                        speed=1.5, pitch=-0.8, energy=1.2, emotion="angry"
                    )
                    audio = tts.tts(text, config)
                    return apply_nin_effects(audio)

        elif PHONETIC_TTS_AVAILABLE:
            # Use Phonetic TTS
            tts = PhoneticTTS()
            audio = tts.speak(text, industrial=True)
            return audio
        elif GTTS_AVAILABLE:
            # Use Google TTS with NIN effects
            return create_gtts_industrial(text)
        else:
            # Use enhanced mock TTS
            tts = MockTTS()
            config = TTSConfig(speed=1.5, pitch=-0.8, energy=1.2, emotion="angry")
            audio = tts.tts(text, config)
            return apply_nin_effects(audio)

    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
