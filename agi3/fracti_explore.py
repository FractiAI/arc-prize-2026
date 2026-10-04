"""FractiAI heuristic explorer for ARC-AGI-3 (no LLM required).

Honesty: systematic exploration + frame-delta bandit — not a fluid-intelligence claim.
Copy into vendor/ARC-AGI-3-Agents/agents/templates/ and import from agents/__init__.py.
"""

from __future__ import annotations

import hashlib
import random
from collections import defaultdict
from typing import Any, Optional

from arcengine import FrameData, GameAction, GameState

from ..agent import Agent


def _frame_digest(frame: FrameData) -> str:
    try:
        raw = repr(frame.frame).encode()
    except Exception:
        raw = b""
    return hashlib.md5(raw).hexdigest()[:12]


def _nonzero_cells(frame: FrameData) -> list[tuple[int, int]]:
    cells: list[tuple[int, int]] = []
    layers = frame.frame or []
    for layer in layers:
        for y, row in enumerate(layer):
            for x, v in enumerate(row):
                if v:
                    cells.append((x, y))
    return cells


class FractiExplore(Agent):
    """Explore available actions; prefer ones that change the frame or raise levels."""

    MAX_ACTIONS = 400

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._rng = random.Random(hash(self.game_id) & 0xFFFFFFFF)
        self._action_scores: dict[int, float] = defaultdict(float)
        self._action_tries: dict[int, int] = defaultdict(int)
        self._click_queue: list[tuple[int, int]] = []
        self._click_i = 0
        self._last_digest: Optional[str] = None
        self._last_levels = 0
        self._simple_cycle = [
            GameAction.ACTION1,
            GameAction.ACTION2,
            GameAction.ACTION3,
            GameAction.ACTION4,
            GameAction.ACTION5,
            GameAction.ACTION7,
        ]
        self._cycle_i = 0
        self._stall = 0

    @property
    def name(self) -> str:
        return f"{super().name}.explore{self.MAX_ACTIONS}"

    def is_done(self, frames: list[FrameData], latest_frame: FrameData) -> bool:
        return latest_frame.state is GameState.WIN

    def _available(self, latest_frame: FrameData) -> list[GameAction]:
        ids = latest_frame.available_actions or []
        if not ids:
            return [a for a in GameAction if a is not GameAction.RESET]
        out: list[GameAction] = []
        for a in GameAction:
            if a is GameAction.RESET:
                continue
            if a.value in ids:
                out.append(a)
        return out or [a for a in GameAction if a is not GameAction.RESET]

    def _refill_clicks(self, latest_frame: FrameData) -> None:
        cells = _nonzero_cells(latest_frame)
        if not cells:
            # sparse scan of 64×64
            cells = [(x, y) for y in range(0, 64, 8) for x in range(0, 64, 8)]
        else:
            # densify around nonzero cells
            denser: list[tuple[int, int]] = []
            for x, y in cells:
                denser.append((x, y))
                for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 64 and 0 <= ny < 64:
                        denser.append((nx, ny))
            cells = denser
        self._rng.shuffle(cells)
        self._click_queue = cells[:120]
        self._click_i = 0

    def _pick_simple(self, available: list[GameAction]) -> GameAction:
        simple = [a for a in available if a.is_simple()]
        if not simple:
            return available[0]
        # UCB-ish: prefer high score / low tries, with cycle exploration
        def key(a: GameAction) -> float:
            n = self._action_tries[a.value] + 1
            return self._action_scores[a.value] / n + 0.35 / n

        ranked = sorted(simple, key=key, reverse=True)
        # mix in cycle member if stalling
        if self._stall >= 3:
            for _ in range(len(self._simple_cycle)):
                cand = self._simple_cycle[self._cycle_i % len(self._simple_cycle)]
                self._cycle_i += 1
                if cand in simple:
                    return cand
        return ranked[0]

    def choose_action(
        self, frames: list[FrameData], latest_frame: FrameData
    ) -> GameAction:
        if latest_frame.state in [GameState.NOT_PLAYED, GameState.GAME_OVER]:
            self._last_digest = None
            self._stall = 0
            return GameAction.RESET

        # credit previous action
        dig = _frame_digest(latest_frame)
        levels = latest_frame.levels_completed or 0
        if frames and len(frames) >= 2:
            prev_input = frames[-1].action_input
            prev_id = getattr(prev_input, "id", None)
            # id may be GameAction enum or int
            if prev_id is not None:
                pid = int(getattr(prev_id, "value", prev_id))
            else:
                pid = None
            if pid is not None and pid != 0:
                reward = 0.0
                if levels > self._last_levels:
                    reward += 5.0
                if self._last_digest and dig != self._last_digest:
                    reward += 1.0
                    self._stall = 0
                else:
                    reward -= 0.15
                    self._stall += 1
                self._action_scores[pid] += reward
                self._action_tries[pid] += 1
        self._last_digest = dig
        self._last_levels = levels

        available = self._available(latest_frame)
        complex_acts = [a for a in available if a.is_complex()]

        # Prefer click exploration strongly when ACTION6 is available
        use_click = bool(complex_acts) and (
            self._stall >= 1 or self._rng.random() < 0.65
        )
        if use_click:
            action = complex_acts[0]
            if not self._click_queue or self._click_i >= len(self._click_queue):
                self._refill_clicks(latest_frame)
            x, y = self._click_queue[self._click_i % len(self._click_queue)]
            self._click_i += 1
            action.set_data({"x": int(x), "y": int(y)})
            action.reasoning = {
                "desired_action": str(action.value),
                "my_reason": "fracti_explore_click",
                "xy": [x, y],
            }
            return action

        action = self._pick_simple(available)
        action.reasoning = f"fracti_explore simple {action.value} stall={self._stall}"
        return action
