
import math
import struct
import pygame


class SoundEffects:
    """Generate and play simple game sound effects."""

    def __init__(self):
        self.enabled = True
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(
                    frequency=22050,
                    size=-16,
                    channels=1,
                    buffer=512
                )

            self.sounds = {
                "click": self.create_tone([450], 0.06),
                "move": self.create_tone([660], 0.09),
                "win": self.create_tone([523, 659, 784], 0.30),
                "lose": self.create_tone([392, 330, 262], 0.30),
                "draw": self.create_tone([440, 440], 0.20)
            }

        except pygame.error:
            self.enabled = False

    def create_tone(self, frequencies, duration):
        """Create an original sound using sine waves."""

        sample_rate = 22050
        total_samples = int(sample_rate * duration)
        audio_data = bytearray()

        for i in range(total_samples):
            t = i / sample_rate

            fade_in = min(1.0, i / 300)
            fade_out = min(1.0, (total_samples - i) / 500)
            envelope = max(0, min(fade_in, fade_out))

            value = sum(
                math.sin(2 * math.pi * frequency * t)
                for frequency in frequencies
            ) / len(frequencies)

            sample = int(32767 * 0.20 * envelope * value)

            audio_data.extend(
                struct.pack("<h", sample)
            )

        return pygame.mixer.Sound(buffer=bytes(audio_data))

    def play(self, name):
        """Play a sound if sound effects are enabled."""

        if not self.enabled:
            return

        sound = self.sounds.get(name)

        if sound:
            try:
                sound.play()
            except pygame.error:
                pass

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)
