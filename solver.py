"""ARC-AGI-2 RuleLab: interpretable one-step transformation synthesis.

This intentionally modest baseline searches for a single shared program made
from a dihedral geometry, optional monochrome-background crop, a demonstration-
derived uniform integer scale, and a globally consistent color permutation.
It does not use external models or network calls.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

Grid = list[list[int]]


@dataclass(frozen=True)
class Program:
    geometry: str = "identity"
    crop_color: int | None = None
    color_map: tuple[tuple[int, int], ...] = ()
    scale_factor: int = 1

    def apply(self, grid: Sequence[Sequence[int]]) -> Grid:
        g = [list(map(int, row)) for row in grid]
        if self.geometry == "rot90":
            g = [list(row) for row in zip(*g[::-1])]
        elif self.geometry == "rot180":
            g = [row[::-1] for row in g[::-1]]
        elif self.geometry == "rot270":
            g = [list(row) for row in zip(*g)][::-1]
        elif self.geometry == "flip_h":
            g = [row[::-1] for row in g]
        elif self.geometry == "flip_v":
            g = g[::-1]
        elif self.geometry == "transpose":
            g = [list(row) for row in zip(*g)]
        elif self.geometry == "anti_transpose":
            g = [list(row) for row in zip(*g[::-1])][::-1]
        elif self.geometry != "identity":
            raise ValueError(f"Unknown geometry: {self.geometry}")

        if self.crop_color is not None:
            pts = [(r, c) for r, row in enumerate(g) for c, x in enumerate(row)
                   if x != self.crop_color]
            if pts:
                r0, r1 = min(r for r, _ in pts), max(r for r, _ in pts)
                c0, c1 = min(c for _, c in pts), max(c for _, c in pts)
                g = [row[c0:c1 + 1] for row in g[r0:r1 + 1]]
        if self.scale_factor < 1:
            raise ValueError("scale_factor must be a positive integer")
        if self.scale_factor > 1:
            k = self.scale_factor
            g = [[cell for cell in row for _ in range(k)]
                 for row in g for _ in range(k)]
        cmap = dict(self.color_map)
        if cmap:
            g = [[cmap.get(x, x) for x in row] for row in g]
        return g


GEOMETRIES = ("identity", "rot90", "rot180", "rot270", "flip_h", "flip_v", "transpose", "anti_transpose")


def _crop_colors(examples: Sequence[dict]) -> list[int | None]:
    # Candidate crop colors are inferred only from demonstrations.
    colors = {0}
    for ex in examples:
        for row in ex["input"]:
            colors.update(map(int, row))
    return [None, *sorted(colors)]


def _infer_color_map(pairs: Sequence[tuple[Grid, Grid]]) -> dict[int, int] | None:
    mapping: dict[int, int] = {}
    reverse: dict[int, int] = {}
    for src, dst in pairs:
        if len(src) != len(dst) or any(len(a) != len(b) for a, b in zip(src, dst)):
            return None
        for srow, drow in zip(src, dst):
            for s, d in zip(srow, drow):
                if s in mapping and mapping[s] != d:
                    return None
                if d in reverse and reverse[d] != s:
                    return None
                mapping[s], reverse[d] = d, s
    return mapping


def _scale_factors(pairs: Sequence[tuple[Grid, Grid]]) -> list[int]:
    """Infer a shared uniform integer scale from demonstration dimensions."""
    factor: int | None = None
    for src, dst in pairs:
        h, w = len(src), len(src[0])
        oh, ow = len(dst), len(dst[0])
        if oh % h or ow % w or oh // h != ow // w:
            return [1]
        current = oh // h
        if factor is None:
            factor = current
        elif current != factor:
            return [1]
    return [1] if factor in (None, 1) else [1, factor]


def _programs_for_task(task: dict) -> list[Program]:
    examples = task.get("train", [])
    if not examples:
        return []
    accepted: list[Program] = []
    for geometry in GEOMETRIES:
        for crop_color in _crop_colors(examples):
            transformed = []
            valid = True
            for ex in examples:
                try:
                    src = Program(geometry, crop_color).apply(ex["input"])
                except (IndexError, ValueError):
                    valid = False
                    break
                transformed.append((src, [list(map(int, row)) for row in ex["output"]]))
            if not valid:
                continue
            for scale_factor in _scale_factors(transformed):
                scaled_pairs = [
                    (Program(geometry, crop_color, scale_factor=scale_factor).apply(ex["input"]),
                     [list(map(int, row)) for row in ex["output"]])
                    for ex in examples
                ]
                mapping = _infer_color_map(scaled_pairs)
                if mapping is None:
                    continue
                # A single global color rule must explain every demonstration.
                p = Program(geometry, crop_color, tuple(sorted(mapping.items())), scale_factor)
                if all(p.apply(ex["input"]) == [list(map(int, row)) for row in ex["output"]]
                       for ex in examples):
                    accepted.append(p)
    # Prefer less complex programs; stable sort makes results reproducible.
    def complexity(p: Program) -> tuple[int, int, int, int, str, int]:
        geom_cost = 0 if p.geometry == "identity" else 1
        crop_cost = 0 if p.crop_color is None else 1
        scale_cost = 0 if p.scale_factor == 1 else 1
        map_cost = sum(a != b for a, b in p.color_map)
        return (geom_cost + crop_cost + scale_cost + map_cost, geom_cost, crop_cost, scale_cost,
                p.geometry, -1 if p.crop_color is None else p.crop_color)
    return sorted(accepted, key=complexity)


def predict_task(task: dict, n_attempts: int = 2) -> list[list[Grid]]:
    """Return n_attempts candidates per test pair using demonstrations only."""
    programs = _programs_for_task(task)
    tests = task.get("test", [])
    result: list[list[Grid]] = []
    for ex in tests:
        guesses: list[Grid] = []
        for p in programs:
            candidate = p.apply(ex["input"])
            if candidate not in guesses:
                guesses.append(candidate)
            if len(guesses) == n_attempts:
                break
        # Guaranteed legal deterministic fallbacks for unsupported tasks.
        fallback_programs = [Program("identity"), Program("rot180"), Program("rot90"), Program("flip_h")]
        for p in fallback_programs:
            candidate = p.apply(ex["input"])
            if candidate not in guesses:
                guesses.append(candidate)
            if len(guesses) == n_attempts:
                break
        while len(guesses) < n_attempts:
            guesses.append([row[:] for row in guesses[0]])
        result.append(guesses)
    return result


def kaggle_payload(tasks: dict[str, dict]) -> dict[str, list[dict[str, Grid]]]:
    """Build the ARC Prize JSON submission object, exactly two guesses per test."""
    payload: dict[str, list[dict[str, Grid]]] = {}
    for task_id, task in tasks.items():
        payload[task_id] = [
            {"attempt_1": guesses[0], "attempt_2": guesses[1]}
            for guesses in predict_task(task, n_attempts=2)
        ]
    return payload


def exact_task_score(predictions: Iterable[Sequence[Grid]], truths: Sequence[Grid]) -> tuple[int, int]:
    """Count exact output matches, for local diagnostics only."""
    pred_list = list(predictions)
    correct = sum(any(p == truth for p in preds) for preds, truth in zip(pred_list, truths))
    return correct, len(truths)
