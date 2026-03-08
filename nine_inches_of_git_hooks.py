#!/usr/bin/env python3
"""
Git post-push hook that reads commit messages in industrial screams.
Uses TTS engine for audio synthesis.
"""

import subprocess
import sys
import time
from typing import List

import sounddevice as sd
import numpy as np

from tts_engine import (
    create_industrial_scream,
    CHATTERBOX_AVAILABLE,
    PHONETIC_TTS_AVAILABLE,
    GTTS_AVAILABLE,
)


def get_commit_messages_since_last_push() -> List[str]:
    """Get commit messages that were just pushed"""
    try:
        # Get the current branch
        branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"], timeout=30
            )
            .decode()
            .strip()
        )

        # Get the remote tracking branch
        remote_branch = (
            subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD@{upstream}"], timeout=30
            )
            .decode()
            .strip()
        )

        # Get commits that were just pushed
        commits = (
            subprocess.check_output(
                ["git", "log", f"{remote_branch}..HEAD", "--pretty=format:%s"],
                timeout=60,
            )
            .decode()
            .strip()
        )

        if commits:
            return commits.split("\n")
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit messages: {e}")
        return []


def play_audio(audio: np.ndarray) -> bool:
    """Play audio using sounddevice. Returns True on success, False on failure."""
    try:
        sd.play(audio, samplerate=44100)
        sd.wait()  # Wait until audio finishes playing
        return True
    except Exception as e:
        print(f"Error playing audio: {e}")
        return False


def main() -> None:
    """Main function to execute the hook"""
    print("🎸 Nine Inches of Git Hooks Activated! 🎸")

    # Report available TTS engines
    if CHATTERBOX_AVAILABLE:
        print("ChatterBox TTS available")
    elif PHONETIC_TTS_AVAILABLE:
        print("Using Phonetic TTS with industrial effects")
    elif GTTS_AVAILABLE:
        print("Using Google TTS with industrial effects")
    else:
        print("No TTS available, using enhanced synthetic method")

    # Get commit messages
    commit_messages = get_commit_messages_since_last_push()

    if not commit_messages:
        print("No new commits to scream about.")
        return

    print(f"Found {len(commit_messages)} commit messages to scream:")

    # Install requirements if needed
    try:
        import sounddevice
    except ImportError:
        print("Installing required packages...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "sounddevice", "numpy"],
            timeout=120,
        )

    # Generate and play screams for each commit message
    for i, message in enumerate(commit_messages, 1):
        print(f"{i}. {message}")

        # Convert commit message to scream text
        scream_text = f"COMMIT! {message.upper()}! PUSHED TO REPOSITORY! AAAAAHHHH!"

        # Generate audio
        audio = create_industrial_scream(scream_text)

        if audio is not None:
            print("🔊 Playing industrial scream...")
            if not play_audio(audio):
                print("Warning: Audio playback failed, continuing...")
            time.sleep(0.5)  # Brief pause between screams

    print("🎤 All commits screamed! Nine Inches of Git Hooks complete.")


if __name__ == "__main__":
    main()
