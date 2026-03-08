#!/usr/bin/env python3
"""
Simple test to check if ChatterBox TTS can be imported
"""

try:
    from chatterbox.tts import ChatterboxTTS
    print("✅ ChatterBox TTS import successful!")
    
    # Try to create a simple model
    model = ChatterboxTTS.from_pretrained(device="cpu")
    print("✅ Model loaded successfully!")
    
    # Try to generate a short audio
    wav = model.generate("Test")
    print("✅ Audio generation successful!")
    print(f"Audio shape: {wav.shape}")
    print(f"Sample rate: {model.sr}")
    
except Exception as e:
    import logging
    logging.basicConfig(level=logging.ERROR)
    logging.error(f"ChatterBox TTS test failed: {e}", exc_info=True)