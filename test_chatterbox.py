#!/usr/bin/env python3
"""
Test ChatterBox TTS with example from their GitHub
"""

import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS

def test_chatterbox_tts():
    """Test ChatterBox TTS with example code"""
    print("🎤 Testing ChatterBox TTS...")
    
    try:
        # Initialize model on CPU (since we don't have CUDA)
        print("Loading ChatterBox TTS model...")
        model = ChatterboxTTS.from_pretrained(device="cpu")
        print("Model loaded successfully!")
        
        # Test with git-related text
        text = "Nine Inches of Git Hooks is now working with real voice synthesis!"
        print(f"Generating audio for: '{text}'")
        
        # Generate audio
        wav = model.generate(text)
        
        # Save to file
        ta.save("test-git-hooks.wav", wav, model.sr)
        print("Audio saved to test-git-hooks.wav")
        
        # Also play the audio directly
        import sounddevice as sd
        print("Playing audio...")
        sd.play(wav.numpy(), samplerate=model.sr)
        sd.wait()
        
        # Test with different git commit messages
        commit_messages = [
            "Fixed audio output issues",
            "Added voice synthesis support",
            "Updated git hook configuration",
            "Industrial effects enhanced"
        ]
        
        for msg in commit_messages:
            print(f"Generating: '{msg}'")
            wav = model.generate(f"Git commit: {msg}")
            sd.play(wav.numpy(), samplerate=model.sr)
            sd.wait()
            
        print("✅ ChatterBox TTS test complete!")
        
except Exception as e:
    import logging
    logging.basicConfig(level=logging.ERROR)
    logging.error(f"ChatterBox TTS test failed: {e}", exc_info=True)

if __name__ == "__main__":
    test_chatterbox_tts()