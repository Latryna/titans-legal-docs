"""TITANS cognitive trace simulation.

This module provides a command line demonstration of the five TITANS modules.
Each module is implemented as a lightweight placeholder that mirrors the
behaviour described in the project documentation. When executed directly it
runs two scenarios and prints the intermediate inputs and outputs for every
module so that reviewers can follow the "thought" process step by step.
"""
from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Tuple

try:  # Optional numeric helper for nicer formatting if available
    import numpy as _np
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    _np = None  # type: ignore

try:  # Optional graph helper mirroring the original notebook demo
    import networkx as _nx
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    _nx = None  # type: ignore


Vector3 = Tuple[float, float, float]


def print_header(title: str) -> None:
    """Print a formatted header for a module section."""
    print("\n" + "=" * 60)
    print(f"[[ {title} ]]")
    print("=" * 60)


def print_io(
    input_label: str,
    input_data: object,
    output_label: str,
    output_data: object,
    *,
    delay_seconds: float,
) -> None:
    """Print formatted input/output pairs with an optional delay."""
    print(f"  -> Input ({input_label}):\n     {input_data}")
    if delay_seconds:
        time.sleep(delay_seconds)
    print(f"  <- Output ({output_label}):\n     {output_data}")


@dataclass
class CognitiveTraceResult:
    """Container holding the artefacts produced across the pipeline."""

    perception_vector: Vector3
    memory_status: str
    abstract_concept: str
    related_concepts: List[str]
    final_decision: str


@dataclass
class PerceptionModule:
    """Simulate M1 using a simple Capsule-inspired feature vector."""

    def process(self, raw_data: Dict[str, float]) -> Vector3:
        vector: Vector3 = (
            float(raw_data.get("feature1", 0.0)),
            float(raw_data.get("feature2", 0.0)),
            float(raw_data.get("urgency", 0.0)),
        )
        return vector


class MemoryModule:
    """Simulate M2 with a surprise-based short term memory buffer."""

    def __init__(self) -> None:
        self.short_term_memory: List[Vector3] = []

    def process(self, perception_vector: Vector3) -> str:
        surprise_factor = math.sqrt(sum(component ** 2 for component in perception_vector))
        if surprise_factor > 1.0:
            self.short_term_memory.append(perception_vector)
            return f"High surprise ({surprise_factor:.2f}). Stored in STM."
        return f"Low surprise ({surprise_factor:.2f}). Ignored."


@dataclass
class AbstractionModule:
    """Simulate M3 by mapping vectors to high level concepts."""

    def process(self, perception_vector: Vector3) -> str:
        if perception_vector[2] > 0.8:
            return "CONCEPT_URGENT_TASK"
        if perception_vector[0] > perception_vector[1]:
            return "CONCEPT_ANALYTICAL_INPUT"
        return "CONCEPT_BACKGROUND_NOISE"


class ReasoningModule:
    """Simulate M4 reasoning over a lightweight knowledge graph."""

    def __init__(self) -> None:
        if _nx is not None:
            graph = _nx.Graph()
            graph.add_edges_from(
                [
                    ("CONCEPT_URGENT_TASK", "ACTION_ALLOCATE_RESOURCES"),
                    ("CONCEPT_URGENT_TASK", "NOTIFY_SUPERVISOR"),
                    ("CONCEPT_ANALYTICAL_INPUT", "ACTION_RUN_ANALYSIS"),
                    ("ACTION_RUN_ANALYSIS", "SAVE_RESULTS"),
                ]
            )
            self._graph = graph
            self._adjacency: Dict[str, List[str]] | None = None
        else:
            self._graph = None
            self._adjacency = {
                "CONCEPT_URGENT_TASK": ["ACTION_ALLOCATE_RESOURCES", "NOTIFY_SUPERVISOR"],
                "CONCEPT_ANALYTICAL_INPUT": ["ACTION_RUN_ANALYSIS"],
                "ACTION_RUN_ANALYSIS": ["SAVE_RESULTS"],
            }

    def process(self, concept: str) -> List[str]:
        if self._graph is not None and _nx is not None:
            if self._graph.has_node(concept):
                return list(self._graph.neighbors(concept))
        elif self._adjacency is not None:
            if concept in self._adjacency:
                return list(self._adjacency[concept])
        return ["No related concepts found."]


@dataclass
class AgencyModule:
    """Simulate M5 action selection with a simple priority scheme."""

    def process(self, potential_actions: Iterable[str]) -> str:
        actions = list(potential_actions)
        for action in actions:
            if action.startswith("ACTION_"):
                return f"Decision: Execute '{action}'."
        if actions:
            return f"Decision: Fallback to '{actions[0]}'."
        return "Decision: No action required."


def _format_vector(perception_vector: Sequence[float]) -> str:
    if _np is not None:
        return _np.array2string(_np.array(perception_vector), precision=2, separator=", ")
    return f"({perception_vector[0]:.2f}, {perception_vector[1]:.2f}, {perception_vector[2]:.2f})"


def run_cognitive_trace(
    input_data: Dict[str, float],
    *,
    emit_console: bool = True,
    delay_seconds: float = 0.5,
) -> CognitiveTraceResult:
    """Run the TITANS pipeline for the provided input data."""
    m1 = PerceptionModule()
    m2 = MemoryModule()
    m3 = AbstractionModule()
    m4 = ReasoningModule()
    m5 = AgencyModule()

    perception_vector = m1.process(input_data)
    memory_status = m2.process(perception_vector)
    abstract_concept = m3.process(perception_vector)
    related_concepts = m4.process(abstract_concept)
    final_decision = m5.process(related_concepts)

    if emit_console:
        print("=" * 60)
        print(">>> STARTING TITANS COGNITIVE TRACE SIMULATION <<<")
        print(f"Initial raw data: {input_data}")
        print("=" * 60)

        print_header("M1: PERCEPTION")
        print_io(
            "Raw Data",
            input_data,
            "Perception Vector",
            _format_vector(perception_vector),
            delay_seconds=delay_seconds,
        )

        print_header("M2: MEMORY")
        print_io(
            "Perception Vector",
            _format_vector(perception_vector),
            "Memory Status",
            memory_status,
            delay_seconds=delay_seconds,
        )

        print_header("M3: ABSTRACTION")
        print_io(
            "Perception Vector",
            _format_vector(perception_vector),
            "Abstract Concept",
            f"'{abstract_concept}'",
            delay_seconds=delay_seconds,
        )

        print_header("M4: REASONING")
        print_io(
            "Abstract Concept",
            f"'{abstract_concept}'",
            "Related Concepts/Actions",
            related_concepts,
            delay_seconds=delay_seconds,
        )

        print_header("M5: AGENCY")
        print_io(
            "Potential Actions",
            related_concepts,
            "Final Decision",
            final_decision,
            delay_seconds=delay_seconds,
        )

        print("\n" + "=" * 60)
        print(">>> SIMULATION COMPLETE <<<")
        print("=" * 60)

    return CognitiveTraceResult(
        perception_vector=perception_vector,
        memory_status=memory_status,
        abstract_concept=abstract_concept,
        related_concepts=related_concepts,
        final_decision=final_decision,
    )


def main() -> None:
    scenarios = {
        "Scenario 1: Urgent task": {"feature1": 0.5, "feature2": 0.3, "urgency": 0.9},
        "Scenario 2: Routine analysis": {"feature1": 0.9, "feature2": 0.2, "urgency": 0.1},
    }

    for title, payload in scenarios.items():
        print(f"\n\n--- {title.upper()} ---")
        run_cognitive_trace(payload, emit_console=True)


if __name__ == "__main__":
    main()
