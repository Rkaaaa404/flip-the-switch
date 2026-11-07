"""Mock dual-sensor conveyor controller for the fish inspection line.

Simulates Sensor 1 + Camera 1 (dorsal view), a passive flipping guide, then
Sensor 2 + Camera 2 (ventral view). Fish that jam or misflip never reach the
ventral sensor, which is simulated by dropping the ventral capture.
Operator-assisted manual mode is handled elsewhere (HTTP endpoint with an
explicit sequence number), not here.
"""

import asyncio
import itertools
import logging
import random
from collections.abc import Awaitable, Callable
from io import BytesIO
from pathlib import Path

from PIL import Image

EmitFn = Callable[[str, bytes], Awaitable[None]]
ImageSource = Callable[[], bytes]

logger = logging.getLogger(__name__)


class DualConveyorController:
    """Runs simulated fish passes past the dorsal and ventral sensors."""

    def __init__(
        self,
        transit_range: tuple[float, float] = (0.8, 1.5),
        rng: random.Random | None = None,
    ):
        self.transit_range = transit_range
        self._rng = rng or random.Random()

    async def _safe_emit(self, emit: EmitFn, side: str, image: bytes) -> bool:
        try:
            await emit(side, image)
        except Exception as exc:  # noqa: BLE001 - a failed emit must never stop the line
            logger.warning("Emit failed for %s view: %s", side, exc)
            return False
        return True

    async def run_mock_batch(
        self,
        count: int,
        emit: EmitFn,
        image_source: ImageSource,
        drop_ventral_every: int | None = None,
    ) -> dict:
        """Process ``count`` fish sequentially and return a summary dict."""
        if count < 1:
            raise ValueError("count must be at least 1")

        summary = {
            "fish": count,
            "dorsal_emitted": 0,
            "ventral_emitted": 0,
            "ventral_dropped": 0,
            "emit_errors": 0,
        }

        for i in range(1, count + 1):
            if await self._safe_emit(emit, "dorsal", image_source()):
                summary["dorsal_emitted"] += 1
            else:
                summary["emit_errors"] += 1

            await asyncio.sleep(self._rng.uniform(*self.transit_range))

            if drop_ventral_every and i % drop_ventral_every == 0:
                summary["ventral_dropped"] += 1
                continue

            if await self._safe_emit(emit, "ventral", image_source()):
                summary["ventral_emitted"] += 1
            else:
                summary["emit_errors"] += 1

        return summary


def sample_image_source(upload_dir: str) -> ImageSource:
    """Cycle through top-level ``*.jpg`` files in ``upload_dir``.

    Falls back to a generated 320x240 JPEG when the directory has none.
    """
    paths = sorted(Path(upload_dir).glob("*.jpg"))

    if paths:
        cycle = itertools.cycle(paths)
        return lambda: next(cycle).read_bytes()

    def generated() -> bytes:
        buffer = BytesIO()
        Image.new("RGB", (320, 240), (96, 112, 136)).save(buffer, format="JPEG")
        return buffer.getvalue()

    return generated
