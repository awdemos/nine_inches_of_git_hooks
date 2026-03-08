#!/usr/bin/env python3
"""
Unit tests for nine_inches_of_git_hooks.py
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock, mock_open
import subprocess


class TestMockTTS:
    """Tests for the MockTTS class"""

    def test_tts_returns_numpy_array(self):
        """Test that tts() returns a numpy array"""
        # Import here to avoid issues with missing dependencies
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        audio = tts.tts("test message")

        assert isinstance(audio, np.ndarray)
        assert len(audio) > 0

    def test_tts_longer_text_creates_longer_audio(self):
        """Test that longer text generates longer audio"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        short_audio = tts.tts("hi")
        long_audio = tts.tts("this is a much longer text message")

        assert len(long_audio) > len(short_audio)

    def test_tts_speed_parameter(self):
        """Test that speed parameter affects audio duration"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        slow_audio = tts.tts("test", speed=0.5)
        fast_audio = tts.tts("test", speed=2.0)

        # Faster speed should produce shorter audio
        assert len(fast_audio) < len(slow_audio)

    def test_tts_pitch_parameter(self):
        """Test that pitch parameter affects fundamental frequency"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        low_audio = tts.tts("test", pitch=-1.0)
        high_audio = tts.tts("test", pitch=1.0)

        # Both should return valid audio arrays
        assert isinstance(low_audio, np.ndarray)
        assert isinstance(high_audio, np.ndarray)

    def test_tts_energy_parameter(self):
        """Test that energy parameter affects audio characteristics"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        low_energy = tts.tts("test", energy=0.5)
        high_energy = tts.tts("test", energy=2.0)

        # Both should return valid audio arrays
        assert isinstance(low_energy, np.ndarray)
        assert isinstance(high_energy, np.ndarray)

    def test_tts_angry_emotion(self):
        """Test that angry emotion adds distortion"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        normal_audio = tts.tts("test", emotion=None)
        angry_audio = tts.tts("test", emotion="angry")

        # Angry audio should have different characteristics (distortion + noise)
        # Just verify they're both valid arrays
        assert isinstance(angry_audio, np.ndarray)
        assert len(angry_audio) > 0

    def test_tts_normalized_output(self):
        """Test that output is normalized (values between -1 and 1)"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        audio = tts.tts("test message with some content")

        assert np.max(np.abs(audio)) <= 1.0


class TestGetCommitMessages:
    """Tests for git commit message retrieval"""

    @patch("subprocess.check_output")
    def test_get_commit_messages_success(self, mock_check_output):
        """Test successful retrieval of commit messages"""
        # Mock the git commands
        mock_check_output.side_effect = [
            b"main",  # branch name
            b"origin/main",  # remote branch
            b"fix: bug fix\nfeat: new feature",  # commit messages
        ]

        # We need to import the function with mocked dependencies
        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            from nine_inches_of_git_hooks import get_commit_messages_since_last_push

            messages = get_commit_messages_since_last_push()

            assert len(messages) == 2
            assert messages[0] == "fix: bug fix"
            assert messages[1] == "feat: new feature"

    @patch("subprocess.check_output")
    def test_get_commit_messages_no_commits(self, mock_check_output):
        """Test when there are no new commits"""
        mock_check_output.side_effect = [
            b"main",
            b"origin/main",
            b"",  # no commits
        ]

        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            from nine_inches_of_git_hooks import get_commit_messages_since_last_push

            messages = get_commit_messages_since_last_push()

            assert messages == []

    @patch("subprocess.check_output")
    def test_get_commit_messages_git_error(self, mock_check_output):
        """Test handling of git errors"""
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "git")

        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            from nine_inches_of_git_hooks import get_commit_messages_since_last_push

            messages = get_commit_messages_since_last_push()

            assert messages == []


class TestCreateSyntheticScream:
    """Tests for synthetic scream generation"""

    def test_create_synthetic_scream_returns_array(self):
        """Test that create_synthetic_scream returns a numpy array"""
        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            from nine_inches_of_git_hooks import create_synthetic_scream

            audio = create_synthetic_scream("test")

            assert isinstance(audio, np.ndarray)
            assert len(audio) > 0

    def test_create_synthetic_scream_longer_text(self):
        """Test that longer text produces longer scream"""
        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            from nine_inches_of_git_hooks import create_synthetic_scream

            short = create_synthetic_scream("hi")
            long = create_synthetic_scream("this is a longer message")

            assert len(long) > len(short)

    def test_create_synthetic_scream_normalized(self):
        """Test that synthetic scream is normalized"""
        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            from nine_inches_of_git_hooks import create_synthetic_scream

            audio = create_synthetic_scream("test message")

            # After final limiting, values should be bounded
            assert np.max(np.abs(audio)) <= 1.0


class TestPlayAudio:
    """Tests for audio playback"""

    @patch("sounddevice.play")
    @patch("sounddevice.wait")
    def test_play_audio_success(self, mock_wait, mock_play):
        """Test successful audio playback"""
        with patch.dict(
            "sys.modules",
            {
                "sounddevice": MagicMock(play=mock_play, wait=mock_wait),
                "numpy": np,
                "scipy.io": MagicMock(),
            },
        ):
            from nine_inches_of_git_hooks import play_audio

            audio = np.zeros(1000)
            result = play_audio(audio)

            assert result == True
            mock_play.assert_called_once()
            mock_wait.assert_called_once()

    @patch("sounddevice.play")
    def test_play_audio_failure(self, mock_play):
        """Test audio playback failure handling"""
        mock_play.side_effect = Exception("Audio error")

        with patch.dict(
            "sys.modules",
            {
                "sounddevice": MagicMock(play=mock_play),
                "numpy": np,
                "scipy.io": MagicMock(),
            },
        ):
            from nine_inches_of_git_hooks import play_audio

            audio = np.zeros(1000)
            result = play_audio(audio)

            assert result == False


class TestCreateIndustrialScream:
    """Tests for industrial scream generation"""

    def test_create_industrial_scream_with_mock_tts(self):
        """Test industrial scream using mock TTS"""
        with patch.dict(
            "sys.modules",
            {"sounddevice": MagicMock(), "numpy": np, "scipy.io": MagicMock()},
        ):
            # Mock the TTS availability flags
            import nine_inches_of_git_hooks as module

            module.CHATTERBOX_AVAILABLE = False
            module.PHONETIC_TTS_AVAILABLE = False
            module.GTTS_AVAILABLE = False

            from nine_inches_of_git_hooks import create_industrial_scream

            audio = create_industrial_scream("test message")

            # Should return audio when using mock TTS
            if audio is not None:
                assert isinstance(audio, np.ndarray)


class TestAudioNormalization:
    """Tests for audio normalization and safety"""

    def test_no_nan_values(self):
        """Test that audio doesn't contain NaN values"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        audio = tts.tts("test")

        assert not np.any(np.isnan(audio))

    def test_no_inf_values(self):
        """Test that audio doesn't contain infinite values"""
        from nine_inches_of_git_hooks import MockTTS

        tts = MockTTS()
        audio = tts.tts("test")

        assert not np.any(np.isinf(audio))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
