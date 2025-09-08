#!/usr/bin/env python3
"""
Git post-push hook that reads commit messages in industrial screams using ChatterBox TTS
"""

import subprocess
import sys
import os
# Try to import chatterbox, fallback to alternative TTS if not available
try:
    from chatterbox import TTS
    CHATTERBOX_AVAILABLE = True
except ImportError:
    CHATTERBOX_AVAILABLE = False
    print("ChatterBox TTS not available, using alternative method")
import sounddevice as sd
import numpy as np
import tempfile
import time

def get_commit_messages_since_last_push():
    """Get commit messages that were just pushed"""
    try:
        # Get the current branch
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()
        
        # Get the remote tracking branch
        remote_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD@{upstream}']).decode().strip()
        
        # Get commits that were just pushed
        commits = subprocess.check_output(['git', 'log', f'{remote_branch}..HEAD', '--pretty=format:%s']).decode().strip()
        
        if commits:
            return commits.split('\n')
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit messages: {e}")
        return []

def create_industrial_scream(text):
    """Generate industrial-style scream using available TTS"""
    try:
        if CHATTERBOX_AVAILABLE:
            # Use ChatterBox TTS
            tts = TTS()
            
            # Add aggressive emotion and distortion to simulate industrial screams
            audio = tts.tts(
                text,
                speed=1.5,  # Faster for more aggressive delivery
                pitch=-0.8,  # Lower pitch for darker tone
                energy=1.2,  # Higher energy for intensity
                emotion="angry"  # Angry emotion for scream effect
            )
        else:
            # Fallback: create synthetic scream using basic waveforms
            audio = create_synthetic_scream(text)
        
        # Apply distortion effects to make it more scream-like
        audio = np.array(audio)
        
        # Add some distortion by clipping and amplifying
        audio = np.clip(audio * 1.5, -0.8, 0.8)
        
        # Add some reverb/echo effect for that industrial sound
        delayed = np.roll(audio, int(0.1 * 44100))  # 100ms delay
        delayed[:int(0.1 * 44100)] = 0
        audio = audio * 0.7 + delayed * 0.3
        
        return audio
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None

def create_synthetic_scream(text):
    """Create a synthetic scream using basic waveforms when ChatterBox is not available"""
    duration = len(text) * 0.1  # Roughly 0.1 seconds per character
    sample_rate = 44100
    samples = int(duration * sample_rate)
    
    # Create time array
    t = np.linspace(0, duration, samples)
    
    # Create a harsh, distorted sound
    # Mix of square waves and noise for industrial sound
    fundamental = 110  # Low A note
    audio = np.zeros(samples)
    
    # Add harmonics for harsh sound
    for harmonic in [1, 3, 5, 7, 9]:
        frequency = fundamental * harmonic
        amplitude = 1.0 / harmonic
        audio += amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    
    # Add noise for grit
    noise = np.random.normal(0, 0.1, samples)
    audio += noise
    
    # Normalize and apply distortion
    audio = audio / np.max(np.abs(audio))
    audio = np.tanh(audio * 3)  # Heavy distortion
    
    # Create amplitude envelope for scream effect
    envelope = np.exp(-t * 2)  # Decay envelope
    audio = audio * envelope
    
    return audio

def play_audio(audio):
    """Play audio using sounddevice"""
    try:
        sd.play(audio, samplerate=44100)
        sd.wait()  # Wait until audio finishes playing
    except Exception as e:
        print(f"Error playing audio: {e}")

def main():
    """Main function to execute the hook"""
    print("🎸 Nine Inches of Git Hooks Activated! 🎸")
    
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
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'sounddevice', 'numpy'])
    
    # Generate and play screams for each commit message
    for i, message in enumerate(commit_messages, 1):
        print(f"{i}. {message}")
        
        # Convert commit message to scream text
        scream_text = f"COMMIT! {message.upper()}! PUSHED TO REPOSITORY! AAAAAHHHH!"
        
        # Generate audio
        audio = create_industrial_scream(scream_text)
        
        if audio is not None:
            print("🔊 Playing industrial scream...")
            play_audio(audio)
            time.sleep(0.5)  # Brief pause between screams
    
    print("🎤 All commits screamed! Nine Inches of Git Hooks complete.")

if __name__ == "__main__":
    main()