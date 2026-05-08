"""
Synesthesia - Mental Health Population Simulator
A living, breathing world of AI agents with realistic mental health dynamics
"""

__version__ = "0.1.0"
__author__ = "Synesthesia Team"

from synesthesia.agent.agent import Agent
from synesthesia.simulation.engine import SimulationEngine
from synesthesia.database.models import Database

__all__ = ["Agent", "SimulationEngine", "Database"]
