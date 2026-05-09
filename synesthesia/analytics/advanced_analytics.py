"""
Advanced Analytics
Trend detection, risk identification, and predictive analytics
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


class TrendAnalyzer:
    """Analyzes trends in mental health data"""
    
    @staticmethod
    def detect_trend(values: List[float], threshold: float = 0.1) -> str:
        """
        Detect if a metric is trending up, down, or stable
        
        Args:
            values: List of metric values over time
            threshold: Minimum change to consider a trend
            
        Returns:
            'increasing', 'decreasing', or 'stable'
        """
        if len(values) < 2:
            return 'stable'
        
        # Calculate linear regression slope
        n = len(values)
        x = list(range(n))
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(values)
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 'stable'
        
        slope = numerator / denominator
        
        if slope > threshold:
            return 'increasing'
        elif slope < -threshold:
            return 'decreasing'
        else:
            return 'stable'
    
    @staticmethod
    def calculate_rate_of_change(values: List[float]) -> float:
        """Calculate the rate of change (slope) of a metric"""
        if len(values) < 2:
            return 0.0
        
        n = len(values)
        x = list(range(n))
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(values)
        
        numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        return numerator / denominator if denominator != 0 else 0.0
    
    @staticmethod
    def detect_volatility(values: List[float]) -> float:
        """
        Detect volatility/instability in a metric
        
        Returns:
            Standard deviation (higher = more volatile)
        """
        if len(values) < 2:
            return 0.0
        
        return statistics.stdev(values)


class RiskIdentifier:
    """Identifies agents at risk of mental health crisis"""
    
    @staticmethod
    def calculate_risk_score(agent_data: Dict[str, Any]) -> float:
        """
        Calculate risk score for an agent (0.0 = low risk, 1.0 = high risk)
        
        Args:
            agent_data: Agent information including mental health state
            
        Returns:
            Risk score from 0.0 to 1.0
        """
        mental_health = agent_data.get('mental_health', {})
        
        # Base risk from current state
        anxiety = mental_health.get('anxiety', 0.5)
        depression = mental_health.get('depression', 0.5)
        stress = mental_health.get('stress', 0.5)
        wellbeing = mental_health.get('wellbeing', 0.5)
        
        # Weighted risk calculation
        base_risk = (
            anxiety * 0.3 +
            depression * 0.4 +
            stress * 0.2 +
            (1 - wellbeing) * 0.1
        )
        
        # Adjust for trends
        history = agent_data.get('mental_health_history', [])
        if len(history) >= 5:
            recent_anxiety = [h['anxiety'] for h in history[-5:]]
            recent_depression = [h['depression'] for h in history[-5:]]
            
            anxiety_trend = TrendAnalyzer.detect_trend(recent_anxiety)
            depression_trend = TrendAnalyzer.detect_trend(recent_depression)
            
            if anxiety_trend == 'increasing':
                base_risk += 0.1
            if depression_trend == 'increasing':
                base_risk += 0.15
        
        # Adjust for social support
        social_support = agent_data.get('social_support', 0.5)
        base_risk *= (1.5 - social_support * 0.5)  # Less support = higher risk
        
        # Adjust for recent negative events
        recent_events = agent_data.get('recent_events', [])
        negative_events = [e for e in recent_events if e.get('severity', 0) > 0.5]
        if len(negative_events) > 2:
            base_risk += 0.1
        
        return min(1.0, max(0.0, base_risk))
    
    @staticmethod
    def identify_at_risk_agents(
        agents: List[Dict[str, Any]],
        risk_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Identify agents at high risk
        
        Args:
            agents: List of agent data
            risk_threshold: Minimum risk score to be considered at-risk
            
        Returns:
            List of at-risk agents with risk scores
        """
        at_risk = []
        
        for agent in agents:
            risk_score = RiskIdentifier.calculate_risk_score(agent)
            
            if risk_score >= risk_threshold:
                at_risk.append({
                    'agent_id': agent.get('agent_id'),
                    'name': agent.get('name'),
                    'role': agent.get('role'),
                    'risk_score': risk_score,
                    'mental_health': agent.get('mental_health', {}),
                    'reason': RiskIdentifier._get_risk_reason(agent, risk_score)
                })
        
        # Sort by risk score (highest first)
        at_risk.sort(key=lambda x: x['risk_score'], reverse=True)
        
        return at_risk
    
    @staticmethod
    def _get_risk_reason(agent_data: Dict[str, Any], risk_score: float) -> str:
        """Generate a human-readable reason for the risk"""
        mental_health = agent_data.get('mental_health', {})
        reasons = []
        
        if mental_health.get('depression', 0) > 0.7:
            reasons.append("severe depression")
        if mental_health.get('anxiety', 0) > 0.7:
            reasons.append("high anxiety")
        if mental_health.get('stress', 0) > 0.7:
            reasons.append("extreme stress")
        if mental_health.get('wellbeing', 1) < 0.3:
            reasons.append("very low wellbeing")
        
        social_support = agent_data.get('social_support', 0.5)
        if social_support < 0.3:
            reasons.append("lack of social support")
        
        recent_events = agent_data.get('recent_events', [])
        negative_events = [e for e in recent_events if e.get('severity', 0) > 0.5]
        if len(negative_events) > 0:
            reasons.append(f"{len(negative_events)} recent negative event(s)")
        
        if not reasons:
            return "Multiple risk factors"
        
        return ", ".join(reasons)


class PopulationAnalytics:
    """Population-level analytics and insights"""
    
    @staticmethod
    def calculate_population_stats(agents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate aggregate statistics for the population"""
        if not agents:
            return {}
        
        # Mental health metrics
        anxiety_values = []
        depression_values = []
        stress_values = []
        wellbeing_values = []
        
        # Category counts
        category_counts = defaultdict(int)
        
        # Role-based stats
        role_stats = defaultdict(lambda: {
            'count': 0,
            'anxiety': [],
            'depression': [],
            'stress': [],
            'wellbeing': []
        })
        
        for agent in agents:
            mental_health = agent.get('mental_health', {})
            
            anxiety = mental_health.get('anxiety', 0.5)
            depression = mental_health.get('depression', 0.5)
            stress = mental_health.get('stress', 0.5)
            wellbeing = mental_health.get('wellbeing', 0.5)
            category = mental_health.get('category', 'coping')
            
            anxiety_values.append(anxiety)
            depression_values.append(depression)
            stress_values.append(stress)
            wellbeing_values.append(wellbeing)
            category_counts[category] += 1
            
            # Role-based
            role = agent.get('role', 'other')
            role_stats[role]['count'] += 1
            role_stats[role]['anxiety'].append(anxiety)
            role_stats[role]['depression'].append(depression)
            role_stats[role]['stress'].append(stress)
            role_stats[role]['wellbeing'].append(wellbeing)
        
        # Calculate averages
        stats = {
            'total_population': len(agents),
            'avg_anxiety': statistics.mean(anxiety_values),
            'avg_depression': statistics.mean(depression_values),
            'avg_stress': statistics.mean(stress_values),
            'avg_wellbeing': statistics.mean(wellbeing_values),
            'category_distribution': dict(category_counts),
            'role_breakdown': {}
        }
        
        # Role breakdown
        for role, data in role_stats.items():
            if data['count'] > 0:
                stats['role_breakdown'][role] = {
                    'count': data['count'],
                    'avg_anxiety': statistics.mean(data['anxiety']),
                    'avg_depression': statistics.mean(data['depression']),
                    'avg_stress': statistics.mean(data['stress']),
                    'avg_wellbeing': statistics.mean(data['wellbeing'])
                }
        
        return stats
    
    @staticmethod
    def identify_trends(
        historical_stats: List[Dict[str, Any]]
    ) -> Dict[str, str]:
        """
        Identify trends in population mental health
        
        Args:
            historical_stats: List of population stats over time
            
        Returns:
            Dictionary of metric trends
        """
        if len(historical_stats) < 3:
            return {}
        
        # Extract time series
        anxiety_series = [s['avg_anxiety'] for s in historical_stats]
        depression_series = [s['avg_depression'] for s in historical_stats]
        stress_series = [s['avg_stress'] for s in historical_stats]
        wellbeing_series = [s['avg_wellbeing'] for s in historical_stats]
        
        return {
            'anxiety': TrendAnalyzer.detect_trend(anxiety_series),
            'depression': TrendAnalyzer.detect_trend(depression_series),
            'stress': TrendAnalyzer.detect_trend(stress_series),
            'wellbeing': TrendAnalyzer.detect_trend(wellbeing_series)
        }
    
    @staticmethod
    def generate_insights(
        agents: List[Dict[str, Any]],
        historical_stats: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Generate human-readable insights about the population
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Current state insights
        stats = PopulationAnalytics.calculate_population_stats(agents)
        
        # High-level state
        crisis_count = stats['category_distribution'].get('crisis', 0)
        struggling_count = stats['category_distribution'].get('struggling', 0)
        
        if crisis_count > len(agents) * 0.1:
            insights.append(f"⚠️ {crisis_count} agents ({crisis_count/len(agents)*100:.1f}%) are in crisis")
        
        if struggling_count > len(agents) * 0.3:
            insights.append(f"⚠️ {struggling_count} agents ({struggling_count/len(agents)*100:.1f}%) are struggling")
        
        # Metric-specific insights
        if stats['avg_stress'] > 0.7:
            insights.append(f"📊 Population stress is very high ({stats['avg_stress']:.2f})")
        
        if stats['avg_depression'] > 0.6:
            insights.append(f"📊 Depression levels are concerning ({stats['avg_depression']:.2f})")
        
        if stats['avg_wellbeing'] < 0.4:
            insights.append(f"📊 Overall wellbeing is low ({stats['avg_wellbeing']:.2f})")
        
        # Role-specific insights
        if stats['role_breakdown']:
            most_stressed_role = max(
                stats['role_breakdown'].items(),
                key=lambda x: x[1]['avg_stress']
            )
            insights.append(f"💼 {most_stressed_role[0]} are the most stressed role ({most_stressed_role[1]['avg_stress']:.2f})")
        
        # Trend insights
        if historical_stats and len(historical_stats) >= 3:
            trends = PopulationAnalytics.identify_trends(historical_stats)
            
            if trends.get('depression') == 'increasing':
                insights.append("📈 Depression is trending upward")
            
            if trends.get('anxiety') == 'increasing':
                insights.append("📈 Anxiety is trending upward")
            
            if trends.get('wellbeing') == 'decreasing':
                insights.append("📉 Wellbeing is declining")
        
        return insights
