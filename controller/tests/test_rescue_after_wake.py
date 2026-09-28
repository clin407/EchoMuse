"""Audio queued behind a controller-scored wake is the command, not stale."""

import asyncio
from types import SimpleNamespace

import em_controller


def test_rescue_keeps_order_and_drops_sentinels():
    dev = SimpleNamespace(mic_queue=asyncio.Queue(), voice_queue=asyncio.Queue(maxsize=256))
    for item in (b"f1", "vad_end", None, b"f2"):
        dev.mic_queue.put_nowait(item)
    assert em_controller._rescue_after_wake(dev, b"tail") == 3
    got = [dev.voice_queue.get_nowait() for _ in range(dev.voice_queue.qsize())]
    assert got == [b"tail", b"f1", b"f2"]
    assert dev.mic_queue.empty()


def test_rescue_with_nothing_queued():
    dev = SimpleNamespace(mic_queue=asyncio.Queue(), voice_queue=asyncio.Queue(maxsize=256))
    assert em_controller._rescue_after_wake(dev, b"") == 0
    assert dev.voice_queue.empty()
