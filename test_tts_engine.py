#!/usr/bin/env python3
"""
Unit tests for tts_engine.py
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import tempfile
import os


class TestTTSConfig:
    """Tests for TTSConfig dataclass"""

    def test_default_values(self):
        """Test default configuration values"""
        from tts_engine import TTSConfig

        config = TTSConfig()

        assert config.speed == 1.0
        assert config.pitch == 0.0
        assert config.energy == 1.0
        assert config.emotion is None

    def test_custom_values(self):
        """Test custom configuration values"""
        from tts_engine import TTSConfig

        config = TTSConfig(speed=1.5, pitch=-0.5, energy=1.2, emotion="angry")

        assert config.speed == 1.5
        assert config.pitch == -0.5
        assert config.energy == 1.2
        assert config.emotion == "angry"


class TestMockTTS:
    """Tests for MockTTS class"""

    def test_tts_returns_numpy_array(self):
        """Test that tts() returns a numpy array"""
        from tts_engine import MockTTS

        tts = MockTTS()
        audio = tts.tts("test message")

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0

    def test_tts_with_config(self):
        """Test tts() with TTSConfig"""
        from tts_engine import MockTTS, TTSConfig

        tts = MockTTS()
        config = TTSConfig(speed=1.5, emotion="angry")
        audio = tts.tts("test", config)

        assert isinstance(audio, np.ndarray)

    def test_tts_longer_text_creates_longer_audio(self):
        """Test that longer text generates longer audio"""
        from tts_engine import MockTTS

        tts = MockTTS()
        short_audio = tts.tts("hi")
        long_audio = tts.tts("this is a much longer text message")

        assert len(long_audio) > len(short_audio)

    def test_tts_speed_affects_duration(self):
        """Test that speed parameter affects audio duration"""
        from tts_engine import MockTTS, TTSConfig

        tts = MockTTS()
        slow_audio = tts.tts("test", TTSConfig(speed=0.5))
        fast_audio = tts.tts("test", TTSConfig(speed=2.0))

        # Faster speed should produce shorter audio
        assert len(fast_audio) < len(slow_audio)

    def test_tts_normalized_output(self):
        """Test that output is normalized (values between -1 and 1)"""
        from tts_engine import MockTTS

        tts = MockTTS()
        audio = tts.tts("test message")

        assert np.max(np.abs(audio)) <= 1.0

    def test_tts_no_nan_values(self):
        """Test that audio doesn't contain NaN values"""
        from tts_engine import MockTTS

        tts = MockTTS()
        audio = tts.tts("test")

        assert not np.any(np.isnan(audio))

    def test_tts_no_inf_values(self):
        """Test that audio doesn't contain infinite values"""
        from tts_engine import MockTTS

        tts = MockTTS()
        audio = tts.tts("test")

        assert not np.any(np.isinf(audio))


class TestApplyNinEffects:
    """Tests for apply_nin_effects function"""

    def test_returns_numpy_array(self):
        """Test that apply_nin_effects returns numpy array"""
        from tts_engine import apply_nin_effects

        audio = np.random.randn(1000)
        result = apply_nin_effects(audio)

        assert isinstance(result, np.ndarray)

    def test_same_length_output(self):
        """Test that output has same length as input"""
        from tts_engine import apply_nin_effects

        audio = np.random.randn(1000)
        result = apply_nin_effects(audio)

        assert len(result) == len(audio)

    def test_normalized_output(self):
        """Test that output is normalized"""
        from tts_engine import apply_nin_effects

        audio = np.random.randn(10000) * 100  # Large values
        result = apply_nin_effects(audio)

        # After processing, values should be bounded
        assert np.max(np.abs(result)) <= 1.0

    def test_applies_distortion(self):
        """Test that distortion is applied"""
        from tts_engine import apply_nin_effects

        # Create a simple sine wave
        audio = np.sin(np.linspace(0, 10, 1000))
        result = apply_nin_effects(audio)

        # Result should be different from input
        assert not np.allclose(result, audio)


class TestCreateSyntheticScream:
    """Tests for create_synthetic_scream function"""

    def test_returns_numpy_array(self):
        """Test that create_synthetic_scream returns numpy array"""
        from tts_engine import create_synthetic_scream

        audio = create_synthetic_scream("test")

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0

    def test_longer_text_longer_audio(self):
        """Test that longer text produces longer audio"""
        from tts_engine import create_synthetic_scream

        short = create_synthetic_scream("hi")
        long = create_synthetic_scream("this is a longer message")

        assert len(long) > len(short)

    def test_normalized_output(self):
        """Test that output is normalized"""
        from tts_engine import create_synthetic_scream

        audio = create_synthetic_scream("test message")

        assert np.max(np.abs(audio)) <= 1.0

    def test_no_nan_or_inf(self):
        """Test that audio doesn't contain NaN or Inf"""
        from tts_engine import create_synthetic_scream

        audio = create_synthetic_scream("test")

        assert not np.any(np.isnan(audio))
        assert not np.any(np.isinf(audio))


class TestCreateIndustrialScream:
    """Tests for create_industrial_scream function"""

    @patch("tts_engine.CHATTERBOX_AVAILABLE", False)
    @patch("tts_engine.PHONETIC_TTS_AVAILABLE", False)
    @patch("tts_engine.GTTS_AVAILABLE", False)
    def test_falls_back_to_mock_tts(self):
        """Test fallback to MockTTS when other TTS unavailable"""
        from tts_engine import create_industrial_scream

        audio = create_industrial_scream("test")

        # Should return audio from MockTTS
        assert audio is not None
        assert isinstance(audio, np.ndarray)

    def test_returns_numpy_array_or_none(self):
        """Test that function returns numpy array or None"""
        from tts_engine import create_industrial_scream

        audio = create_industrial_scream("test")

        assert audio is None or isinstance(audio, np.ndarray)


class TestConstants:
    """Tests for constants"""

    def test_sample_rate_is_int(self):
        """Test that SAMPLE_RATE is an integer"""
        from constants import SAMPLE_RATE, EXPECTED_SAMPLE_RATE

        assert isinstance(SAMPLE_RATE, int)
        assert SAMPLE_RATE == EXPECTED_SAMPLE_RATE

    def test_min_audio_length_is_int(self):
        """Test that MIN_AUDIO_LENGTH_FOR_FILTER is an integer"""
        from constants import MIN_AUDIO_LENGTH_FOR_FILTER, EXPECTED_MIN_AUDIO_LENGTH

        assert isinstance(MIN_AUDIO_LENGTH_FOR_FILTER, int)
        assert MIN_AUDIO_LENGTH_FOR_FILTER == EXPECTED_MIN_AUDIO_LENGTH


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
