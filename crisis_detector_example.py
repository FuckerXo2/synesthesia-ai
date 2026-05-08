"""
Crisis Detection System for MentalHealthSim

This module monitors agent states and simulation outputs for crisis indicators.
It provides real-time alerts and resource recommendations.

CRITICAL: This is a safety-critical component. All changes must be reviewed
by clinical professionals before deployment.
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class RiskLevel(Enum):
    """Risk severity levels"""
    NONE = 0
    LOW = 1
    MODERATE = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class CrisisAlert:
    """Crisis alert information"""
    risk_level: RiskLevel
    indicators: List[str]
    recommended_actions: List[str]
    crisis_resources: Dict[str, str]
    agent_id: str
    round_number: int
    timestamp: str
    notes: str


class CrisisDetector:
    """
    Detects crisis indicators in agent states and simulation outputs.
    
    This system uses multiple detection methods:
    1. Keyword/phrase matching (high-risk language)
    2. Behavioral pattern analysis (withdrawal, deterioration)
    3. Metric threshold monitoring (severe scores)
    4. Contextual analysis (combination of factors)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize crisis detector.
        
        Args:
            config: Configuration dictionary with thresholds and settings
        """
        self.config = config or {}
        self.alert_threshold = self.config.get('alert_threshold', 0.8)
        self.enabled = self.config.get('enabled', True)
        
        # Load clinical indicators
        self._load_risk_indicators()
        
        # Alert history for pattern detection
        self.alert_history: List[CrisisAlert] = []
        
        logger.info("CrisisDetector initialized with threshold: %.2f", self.alert_threshold)
    
    def _load_risk_indicators(self):
        """
        Load risk indicators from clinical guidelines.
        
        NOTE: These should be validated by clinical professionals and
        updated based on current research and best practices.
        """
        
        # CRITICAL RISK: Immediate danger indicators
        self.critical_indicators = {
            'suicidal_ideation': [
                r'\b(want to die|wish I was dead|kill myself|end my life|suicide)\b',
                r'\b(not worth living|better off dead|no reason to live)\b',
            ],
            'self_harm': [
                r'\b(cut myself|hurt myself|self-harm|self harm)\b',
                r'\b(burning myself|hitting myself)\b',
            ],
            'harm_to_others': [
                r'\b(hurt (someone|others)|harm (someone|others))\b',
                r'\b(violent thoughts|want to hurt)\b',
            ],
            'severe_deterioration': [
                r'\b(can\'t go on|giving up|no hope|hopeless)\b',
                r'\b(unbearable|can\'t take it|too much)\b',
            ]
        }
        
        # HIGH RISK: Serious concern indicators
        self.high_risk_indicators = {
            'isolation': [
                r'\b(completely alone|no one cares|nobody understands)\b',
                r'\b(pushing everyone away|isolating)\b',
            ],
            'substance_abuse': [
                r'\b(drinking heavily|using drugs|getting high)\b',
                r'\b(can\'t stop drinking|need substances)\b',
            ],
            'severe_symptoms': [
                r'\b(can\'t function|can\'t get out of bed|can\'t work)\b',
                r'\b(constant panic|always anxious|severe depression)\b',
            ]
        }
        
        # MODERATE RISK: Concerning patterns
        self.moderate_risk_indicators = {
            'declining_functioning': [
                r'\b(missing work|skipping classes|not eating)\b',
                r'\b(can\'t sleep|sleeping all day|avoiding people)\b',
            ],
            'negative_coping': [
                r'\b(drinking to cope|using to forget|avoiding everything)\b',
            ]
        }
        
        # Protective factors (reduce risk)
        self.protective_factors = {
            'support': [
                r'\b(talked to friend|family helped|therapist said)\b',
                r'\b(support group|feeling supported|people care)\b',
            ],
            'coping': [
                r'\b(used coping skills|practiced mindfulness|went for walk)\b',
                r'\b(reached out|asked for help|called therapist)\b',
            ],
            'hope': [
                r'\b(feeling better|little hope|things improving)\b',
                r'\b(looking forward|making plans|future)\b',
            ]
        }
    
    def analyze_agent_state(
        self,
        agent_id: str,
        agent_state: Dict[str, Any],
        round_number: int
    ) -> Optional[CrisisAlert]:
        """
        Analyze agent state for crisis indicators.
        
        Args:
            agent_id: Unique agent identifier
            agent_state: Current agent state including:
                - mental_health_metrics: Dict of current scores
                - recent_actions: List of recent behaviors
                - recent_thoughts: List of recent internal states
                - social_connections: Current social network state
            round_number: Current simulation round
        
        Returns:
            CrisisAlert if crisis detected, None otherwise
        """
        if not self.enabled:
            return None
        
        indicators = []
        risk_scores = []
        
        # 1. Analyze mental health metrics
        metrics = agent_state.get('mental_health_metrics', {})
        metric_risk, metric_indicators = self._analyze_metrics(metrics)
        if metric_risk > 0:
            risk_scores.append(metric_risk)
            indicators.extend(metric_indicators)
        
        # 2. Analyze recent thoughts/statements
        thoughts = agent_state.get('recent_thoughts', [])
        thought_risk, thought_indicators = self._analyze_text(thoughts)
        if thought_risk > 0:
            risk_scores.append(thought_risk)
            indicators.extend(thought_indicators)
        
        # 3. Analyze behavioral patterns
        actions = agent_state.get('recent_actions', [])
        behavior_risk, behavior_indicators = self._analyze_behaviors(actions)
        if behavior_risk > 0:
            risk_scores.append(behavior_risk)
            indicators.extend(behavior_indicators)
        
        # 4. Analyze social connections
        social = agent_state.get('social_connections', {})
        social_risk, social_indicators = self._analyze_social(social)
        if social_risk > 0:
            risk_scores.append(social_risk)
            indicators.extend(social_indicators)
        
        # 5. Check for protective factors
        protective_score = self._assess_protective_factors(agent_state)
        
        # Calculate overall risk
        if not risk_scores:
            return None
        
        # Weighted average with protective factor adjustment
        avg_risk = sum(risk_scores) / len(risk_scores)
        adjusted_risk = max(0, avg_risk - (protective_score * 0.2))
        
        # Determine risk level
        risk_level = self._calculate_risk_level(adjusted_risk)
        
        # Generate alert if threshold exceeded
        if adjusted_risk >= self.alert_threshold or risk_level == RiskLevel.CRITICAL:
            alert = self._generate_alert(
                agent_id=agent_id,
                risk_level=risk_level,
                indicators=indicators,
                round_number=round_number,
                protective_score=protective_score
            )
            
            self.alert_history.append(alert)
            logger.warning(
                "CRISIS ALERT: Agent %s, Risk Level: %s, Round: %d",
                agent_id, risk_level.name, round_number
            )
            
            return alert
        
        return None
    
    def _analyze_metrics(self, metrics: Dict[str, float]) -> tuple[float, List[str]]:
        """Analyze mental health metric scores for crisis indicators."""
        risk_score = 0.0
        indicators = []
        
        # PHQ-9 style depression score (0-27)
        depression = metrics.get('depression_score', 0)
        if depression >= 20:  # Severe
            risk_score = max(risk_score, 0.9)
            indicators.append(f"Severe depression score: {depression}")
        elif depression >= 15:  # Moderately severe
            risk_score = max(risk_score, 0.7)
            indicators.append(f"Moderately severe depression: {depression}")
        
        # GAD-7 style anxiety score (0-21)
        anxiety = metrics.get('anxiety_score', 0)
        if anxiety >= 15:  # Severe
            risk_score = max(risk_score, 0.8)
            indicators.append(f"Severe anxiety score: {anxiety}")
        
        # Functioning score (0-100, lower is worse)
        functioning = metrics.get('functioning_score', 100)
        if functioning <= 30:  # Severe impairment
            risk_score = max(risk_score, 0.85)
            indicators.append(f"Severe functional impairment: {functioning}")
        elif functioning <= 50:  # Moderate impairment
            risk_score = max(risk_score, 0.6)
            indicators.append(f"Moderate functional impairment: {functioning}")
        
        return risk_score, indicators
    
    def _analyze_text(self, texts: List[str]) -> tuple[float, List[str]]:
        """Analyze text content for crisis language."""
        risk_score = 0.0
        indicators = []
        
        combined_text = ' '.join(texts).lower()
        
        # Check critical indicators
        for category, patterns in self.critical_indicators.items():
            for pattern in patterns:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    risk_score = 1.0  # Maximum risk
                    indicators.append(f"CRITICAL: {category} language detected")
                    logger.critical("Critical indicator detected: %s", category)
                    break
            if risk_score == 1.0:
                break
        
        # Check high risk indicators
        if risk_score < 1.0:
            for category, patterns in self.high_risk_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, combined_text, re.IGNORECASE):
                        risk_score = max(risk_score, 0.8)
                        indicators.append(f"High risk: {category} detected")
        
        # Check moderate risk indicators
        if risk_score < 0.8:
            for category, patterns in self.moderate_risk_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, combined_text, re.IGNORECASE):
                        risk_score = max(risk_score, 0.6)
                        indicators.append(f"Moderate risk: {category} detected")
        
        return risk_score, indicators
    
    def _analyze_behaviors(self, actions: List[Dict[str, Any]]) -> tuple[float, List[str]]:
        """Analyze behavioral patterns for concerning changes."""
        risk_score = 0.0
        indicators = []
        
        if not actions:
            return risk_score, indicators
        
        # Check for isolation behaviors
        social_actions = [a for a in actions if a.get('type') == 'social_interaction']
        if len(social_actions) == 0 and len(actions) >= 5:
            risk_score = max(risk_score, 0.6)
            indicators.append("Complete social withdrawal observed")
        
        # Check for avoidance behaviors
        avoidance_count = sum(1 for a in actions if a.get('coping_type') == 'avoidant')
        if avoidance_count >= len(actions) * 0.7:
            risk_score = max(risk_score, 0.5)
            indicators.append("Predominantly avoidant coping")
        
        # Check for self-harm behaviors
        harmful_actions = [a for a in actions if a.get('type') == 'self_harm']
        if harmful_actions:
            risk_score = 1.0
            indicators.append("CRITICAL: Self-harm behavior detected")
        
        return risk_score, indicators
    
    def _analyze_social(self, social_state: Dict[str, Any]) -> tuple[float, List[str]]:
        """Analyze social connection quality."""
        risk_score = 0.0
        indicators = []
        
        connection_quality = social_state.get('connection_quality', 1.0)
        num_connections = social_state.get('num_active_connections', 0)
        
        if num_connections == 0:
            risk_score = 0.7
            indicators.append("Complete social isolation")
        elif connection_quality < 0.3:
            risk_score = 0.6
            indicators.append("Very poor social connection quality")
        
        return risk_score, indicators
    
    def _assess_protective_factors(self, agent_state: Dict[str, Any]) -> float:
        """Assess protective factors that reduce risk."""
        protective_score = 0.0
        
        thoughts = agent_state.get('recent_thoughts', [])
        combined_text = ' '.join(thoughts).lower()
        
        for category, patterns in self.protective_factors.items():
            for pattern in patterns:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    protective_score += 0.2
                    break
        
        # Cap at 1.0
        return min(protective_score, 1.0)
    
    def _calculate_risk_level(self, risk_score: float) -> RiskLevel:
        """Convert risk score to risk level enum."""
        if risk_score >= 0.9:
            return RiskLevel.CRITICAL
        elif risk_score >= 0.7:
            return RiskLevel.HIGH
        elif risk_score >= 0.5:
            return RiskLevel.MODERATE
        elif risk_score >= 0.3:
            return RiskLevel.LOW
        else:
            return RiskLevel.NONE
    
    def _generate_alert(
        self,
        agent_id: str,
        risk_level: RiskLevel,
        indicators: List[str],
        round_number: int,
        protective_score: float
    ) -> CrisisAlert:
        """Generate crisis alert with recommendations."""
        
        # Get appropriate recommendations
        recommended_actions = self._get_recommendations(risk_level)
        
        # Get crisis resources
        crisis_resources = self._get_crisis_resources()
        
        # Generate notes
        notes = f"Risk detected at round {round_number}. "
        notes += f"Protective factors score: {protective_score:.2f}. "
        notes += "Immediate clinical review recommended."
        
        return CrisisAlert(
            risk_level=risk_level,
            indicators=indicators,
            recommended_actions=recommended_actions,
            crisis_resources=crisis_resources,
            agent_id=agent_id,
            round_number=round_number,
            timestamp=self._get_timestamp(),
            notes=notes
        )
    
    def _get_recommendations(self, risk_level: RiskLevel) -> List[str]:
        """Get recommended actions based on risk level."""
        
        if risk_level == RiskLevel.CRITICAL:
            return [
                "IMMEDIATE ACTION REQUIRED",
                "Stop simulation and review with clinical supervisor",
                "Assess for immediate safety concerns",
                "Consider emergency intervention protocols",
                "Document all indicators thoroughly",
                "Do not proceed without clinical consultation"
            ]
        
        elif risk_level == RiskLevel.HIGH:
            return [
                "Urgent clinical review needed",
                "Increase monitoring frequency",
                "Consider crisis intervention",
                "Assess support system adequacy",
                "Review and adjust treatment plan",
                "Document and track closely"
            ]
        
        elif risk_level == RiskLevel.MODERATE:
            return [
                "Clinical review recommended",
                "Monitor for escalation",
                "Assess need for intervention adjustment",
                "Strengthen support system",
                "Review coping strategies"
            ]
        
        else:  # LOW
            return [
                "Continue monitoring",
                "Note indicators for pattern tracking",
                "Maintain current interventions"
            ]
    
    def _get_crisis_resources(self) -> Dict[str, str]:
        """Get crisis resource information."""
        return {
            'suicide_prevention_lifeline': '988 (call or text)',
            'crisis_text_line': 'Text HOME to 741741',
            'emergency_services': '911',
            'samhsa_helpline': '1-800-662-4357',
            'trevor_project': '1-866-488-7386 (LGBTQ+ youth)',
            'veterans_crisis_line': '988 then press 1',
            'online_chat': 'https://988lifeline.org/chat/'
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_alert_history(
        self,
        agent_id: Optional[str] = None,
        min_risk_level: Optional[RiskLevel] = None
    ) -> List[CrisisAlert]:
        """
        Get alert history with optional filtering.
        
        Args:
            agent_id: Filter by specific agent
            min_risk_level: Filter by minimum risk level
        
        Returns:
            List of matching alerts
        """
        alerts = self.alert_history
        
        if agent_id:
            alerts = [a for a in alerts if a.agent_id == agent_id]
        
        if min_risk_level:
            alerts = [a for a in alerts if a.risk_level.value >= min_risk_level.value]
        
        return alerts
    
    def generate_safety_report(self) -> Dict[str, Any]:
        """Generate summary report of all safety alerts."""
        
        total_alerts = len(self.alert_history)
        
        alerts_by_level = {
            level: len([a for a in self.alert_history if a.risk_level == level])
            for level in RiskLevel
        }
        
        agents_with_alerts = len(set(a.agent_id for a in self.alert_history))
        
        return {
            'total_alerts': total_alerts,
            'alerts_by_level': {level.name: count for level, count in alerts_by_level.items()},
            'agents_with_alerts': agents_with_alerts,
            'critical_alerts': alerts_by_level[RiskLevel.CRITICAL],
            'high_risk_alerts': alerts_by_level[RiskLevel.HIGH],
            'most_recent_alert': self.alert_history[-1] if self.alert_history else None
        }


# Example usage
if __name__ == "__main__":
    # Initialize detector
    detector = CrisisDetector(config={'alert_threshold': 0.7})
    
    # Example agent state with concerning indicators
    agent_state = {
        'mental_health_metrics': {
            'depression_score': 22,  # Severe
            'anxiety_score': 16,     # Severe
            'functioning_score': 35   # Severe impairment
        },
        'recent_thoughts': [
            "I feel completely hopeless",
            "Nothing matters anymore",
            "I can't go on like this"
        ],
        'recent_actions': [
            {'type': 'avoidance', 'coping_type': 'avoidant'},
            {'type': 'avoidance', 'coping_type': 'avoidant'},
            {'type': 'isolation', 'coping_type': 'avoidant'}
        ],
        'social_connections': {
            'connection_quality': 0.2,
            'num_active_connections': 1
        }
    }
    
    # Analyze for crisis
    alert = detector.analyze_agent_state(
        agent_id="agent_001",
        agent_state=agent_state,
        round_number=15
    )
    
    if alert:
        print(f"\n🚨 CRISIS ALERT DETECTED 🚨")
        print(f"Risk Level: {alert.risk_level.name}")
        print(f"\nIndicators:")
        for indicator in alert.indicators:
            print(f"  - {indicator}")
        print(f"\nRecommended Actions:")
        for action in alert.recommended_actions:
            print(f"  - {action}")
        print(f"\nCrisis Resources:")
        for resource, contact in alert.crisis_resources.items():
            print(f"  - {resource}: {contact}")
    else:
        print("No crisis detected")
