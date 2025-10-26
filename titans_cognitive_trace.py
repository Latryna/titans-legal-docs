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
from typing import Dict, Iterable, List, Sequence


def print_header(title: str) -> None:
    """Print a formatted header for a module section."""
    print("\n" + "=" * 60)
    print(f"[[ {title} ]]")
    print("=" * 60)


def print_io(input_label: str, input_data: object, output_label: str, output_data: object) -> None:
    """Print formatted input/output pairs with a brief pause."""
    print(f"  -> Input ({input_label}):\n     {input_data}")
    time.sleep(0.5)
    print(f"  <- Output ({output_label}):\n     {output_data}")


@dataclass
class PerceptionModule:
    """Simulate M1 using simple feature vector construction."""

    def process(self, raw_data: Dict[str, float]) -> Sequence[float]:
        return (
            raw_data.get("feature1", 0.0),
            raw_data.get("feature2", 0.0),
            raw_data.get("urgency", 0.0),
        )


class MemoryModule:
    """Simulate M2 with a surprise-based short term memory buffer."""

    def __init__(self) -> None:
        self.short_term_memory: List[Sequence[float]] = []

    def process(self, perception_vector: Sequence[float]) -> str:
        surprise_factor = math.sqrt(sum(component ** 2 for component in perception_vector))
        if surprise_factor > 1.0:
            self.short_term_memory.append(perception_vector)
            return f"High surprise ({surprise_factor:.2f}). Stored in STM."
        return f"Low surprise ({surprise_factor:.2f}). Ignored."


@dataclass
class AbstractionModule:
    """Simulate M3 by mapping vectors to high level concepts."""

    def process(self, perception_vector: Sequence[float]) -> str:
        if perception_vector[2] > 0.8:
            return "CONCEPT_URGENT_TASK"
        if perception_vector[0] > perception_vector[1]:
            return "CONCEPT_ANALYTICAL_INPUT"
        return "CONCEPT_BACKGROUND_NOISE"


class ReasoningModule:
    """Simulate M4 reasoning over a lightweight knowledge graph."""

    def __init__(self) -> None:
        self.knowledge_graph: Dict[str, List[str]] = {
            "CONCEPT_URGENT_TASK": [
                "ACTION_ALLOCATE_RESOURCES",
                "NOTIFY_SUPERVISOR",
            ],
            "CONCEPT_ANALYTICAL_INPUT": ["ACTION_RUN_ANALYSIS"],
            "ACTION_RUN_ANALYSIS": ["SAVE_RESULTS"],
        }

    def process(self, concept: str) -> List[str]:
        return self.knowledge_graph.get(concept, ["No related concepts found."])


@dataclass
class AgencyModule:
    """Simulate M5 action selection with a simple priority scheme."""

    def process(self, potential_actions: Iterable[str]) -> str:
        for action in potential_actions:
            if "ACTION_" in action:
                return f"Decision: Execute '{action}'."
        potential_actions = list(potential_actions)
        if potential_actions:
            return f"Decision: Fallback to '{potential_actions[0]}'."
        return "Decision: No action required."


def _format_vector(perception_vector: Sequence[float]) -> str:
    return f"({perception_vector[0]:.2f}, {perception_vector[1]:.2f}, {perception_vector[2]:.2f})"


def run_cognitive_trace(input_data: Dict[str, float]) -> None:
    """Run the TITANS pipeline for the provided input data."""
    print("=" * 60)
    print(">>> STARTING TITANS COGNITIVE TRACE SIMULATION <<<")
    print(f"Initial raw data: {input_data}")
    print("=" * 60)

    m1 = PerceptionModule()
    m2 = MemoryModule()
    m3 = AbstractionModule()
    m4 = ReasoningModule()
    m5 = AgencyModule()

    print_header("M1: PERCEPTION")
    perception_vector = m1.process(input_data)
    print_io("Raw Data", input_data, "Perception Vector", _format_vector(perception_vector))

    print_header("M2: MEMORY")
    memory_status = m2.process(perception_vector)
    print_io("Perception Vector", _format_vector(perception_vector), "Memory Status", memory_status)

    print_header("M3: ABSTRACTION")
    abstract_concept = m3.process(perception_vector)
    print_io("Perception Vector", _format_vector(perception_vector), "Abstract Concept", f"'{abstract_concept}'")

    print_header("M4: REASONING")
    related_concepts = m4.process(abstract_concept)
    print_io("Abstract Concept", f"'{abstract_concept}'", "Related Concepts/Actions", related_concepts)

    print_header("M5: AGENCY")
    final_decision = m5.process(related_concepts)
    print_io("Potential Actions", related_concepts, "Final Decision", final_decision)

    print("\n" + "=" * 60)
    print(">>> SIMULATION COMPLETE <<<")
    print("=" * 60)


def main() -> None:
    print("\n\n--- SCENARIO 1: URGENT TASK ---")
    urgent_task_data = {"feature1": 0.5, "feature2": 0.3, "urgency": 0.9}
    run_cognitive_trace(urgent_task_data)

    print("\n\n--- SCENARIO 2: ROUTINE ANALYSIS ---")
    analytical_data = {"feature1": 0.9, "feature2": 0.2, "urgency": 0.1}
    run_cognitive_trace(analytical_data)


if __name__ == "__main__":
    main()
