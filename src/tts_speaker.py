# tts_speaker.py
import threading, queue, time
import pyttsx3
import config

class TTSSpeaker:
    """
    Threaded TTS so voice output never blocks the 10 Hz control loop.
    Includes deduplication — won't repeat the same message too quickly.
    """

    def __init__(self):
        self._q         = queue.Queue()
        self._last_msg  = None
        self._last_time = 0.0

        self._engine = pyttsx3.init()
        self._engine.setProperty('rate', config.TTS_RATE)

        voices = self._engine.getProperty('voices')
        if voices:
            idx = min(config.TTS_VOICE_INDEX, len(voices) - 1)
            self._engine.setProperty('voice', voices[idx].id)

        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            msg = self._q.get()
            if msg is None:
                break
            self._engine.say(msg)
            self._engine.runAndWait()

    def say(self, msg, dedupe_s=2.0):
        """
        Queue a voice message.
        Silently drops it if the same message was said within dedupe_s seconds.
        """
        now = time.time()
        if msg == self._last_msg and (now - self._last_time) < dedupe_s:
            return
        self._last_msg  = msg
        self._last_time = now
        self._q.put(msg)

    def stop(self):
        self._q.put(None)
