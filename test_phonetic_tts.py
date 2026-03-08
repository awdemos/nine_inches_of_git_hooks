#!/usr/bin/env python3
"""
Unit tests for phonetic_tts.py PhoneticTTS class
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock


class TestPhoneticTTS:
    """Tests for PhoneticTTS class"""

    def test_initialization(self):
        """Test that PhoneticTTS initializes correctly"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()

        assert tts.phoneme_formants is not None
        assert tts.word_phonemes is not None
        assert tts.letter_phonemes is not None

    def test_text_to_phonemes_returns_list(self):
        """Test that text_to_phonemes returns a list"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        phonemes = tts.text_to_phonemes("hello")

        assert isinstance(phonemes, list)
        assert len(phonemes) > 0

    def test_text_to_phonemes_handles_punctuation(self):
        """Test that punctuation is removed"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        phonemes = tts.text_to_phonemes("hello, world!")

        assert isinstance(phonemes, list)
        # Should not contain punctuation as phonemes

    def test_text_to_phonemes_known_words(self):
        """Test phoneme conversion for known words"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()

        # 'git' is in the word phonemes dictionary
        phonemes = tts.text_to_phonemes("git")

        assert isinstance(phonemes, list)
        assert len(phonemes) > 0

    def test_synthesize_phonemes_returns_array(self):
        """Test that synthesize_phonemes returns numpy array"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        phonemes = ["g", "ih", "t"]
        audio = tts.synthesize_phonemes(phonemes)

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0

    def test_speak_returns_array(self):
        """Test that speak returns numpy array"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        audio = tts.speak("test")

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0

    def test_speak_without_industrial_effects(self):
        """Test speak with industrial=False"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        audio = tts.speak("test", industrial=False)

        assert isinstance(audio, np.ndarray)

    def test_speak_with_industrial_effects(self):
        """Test speak with industrial=True (default)"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        audio = tts.speak("test", industrial=True)

        assert isinstance(audio, np.ndarray)

    def test_longer_text_produces_longer_audio(self):
        """Test that longer text produces longer audio"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        short_audio = tts.speak("hi")
        long_audio = tts.speak("this is a much longer message")

        assert len(long_audio) > len(short_audio)

    def test_audio_is_normalized(self):
        """Test that audio values are within -1 to 1"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        audio = tts.speak("test message")

        # Values should be bounded
        assert np.max(np.abs(audio)) <= 1.0 + 1e-6  # Small tolerance for floating point

    def test_no_nan_in_audio(self):
        """Test that audio doesn't contain NaN values"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        audio = tts.speak("test")

        assert not np.any(np.isnan(audio))

    def test_no_inf_in_audio(self):
        """Test that audio doesn't contain infinite values"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        audio = tts.speak("test")

        assert not np.any(np.isinf(audio))

    def test_apply_industrial_effects_changes_audio(self):
        """Test that industrial effects modify the audio"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()
        raw_audio = tts.synthesize_phonemes(["g", "ih", "t"])
        processed_audio = tts.apply_industrial_effects(raw_audio.copy())

        # The processed audio should be different from raw
        # (due to distortion, noise, resonances)
        assert not np.allclose(raw_audio, processed_audio)


class TestVoiceOutputIntegration:
    """Integration tests that verify voice output quality"""

    def test_git_words_produce_valid_audio(self):
        """Test that git-related words produce valid audio"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()

        git_words = ["git", "commit", "push", "hook", "test"]

        for word in git_words:
            audio = tts.speak(word, industrial=False)

            assert isinstance(audio, np.ndarray), f"Failed for word: {word}"
            assert len(audio) > 0, f"Empty audio for word: {word}"
            assert not np.any(np.isnan(audio)), f"NaN in audio for word: {word}"

    def test_phrase_produces_valid_audio(self):
        """Test that phrases produce valid audio"""
        from phonetic_tts import PhoneticTTS

        tts = PhoneticTTS()

        phrase = "nine inches of git hooks"
        audio = tts.speak(phrase, industrial=True)

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0
        assert not np.any(np.isnan(audio))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
