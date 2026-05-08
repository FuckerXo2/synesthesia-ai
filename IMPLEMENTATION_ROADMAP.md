# MentalHealthSim - Implementation Roadmap

## 🎯 Goal
Adapt MiroFish architecture for mental health simulation while prioritizing safety, ethics, and clinical validity.

## 📋 Phase 1: Foundation (Weeks 1-4)

### Week 1: Setup & Safety Framework
- [ ] Fork/adapt MiroFish codebase
- [ ] Rename project to MentalHealthSim
- [ ] Implement comprehensive disclaimer system
- [ ] Add crisis resource links (988, Crisis Text Line, etc.)
- [ ] Create ethical guidelines document
- [ ] Set up professional credential verification system

### Week 2: Core Architecture Adaptation
- [ ] Modify `graph_builder.py` → `profile_builder.py`
  - Change from social network extraction to clinical profile generation
  - Add mental health history parsing
  - Implement personality trait extraction
  - Add coping mechanism identification

- [ ] Adapt `simulation_manager.py`
  - Change scenario types (social → therapeutic)
  - Add mental health tracking metrics
  - Implement crisis detection system
  - Add intervention tracking

- [ ] Update `oasis_profile_generator.py` → `agent_profile_generator.py`
  - Clinical profile templates
  - Evidence-based personality models
  - Diverse cultural backgrounds
  - Realistic mental health histories

### Week 3: Simulation Engine Modifications
- [ ] Adapt OASIS framework for mental health contexts
  - Replace social media actions with therapeutic interactions
  - Add therapy session simulation
  - Implement support network dynamics
  - Create life event system

- [ ] Define interaction types:
  - Therapy sessions (CBT, DBT, etc.)
  - Peer support conversations
  - Family interactions
  - Crisis interventions
  - Daily coping activities

- [ ] Create mental health metrics tracking:
  - Mood scores (PHQ-9 style)
  - Anxiety levels (GAD-7 style)
  - Functioning scores
  - Social connection quality
  - Coping effectiveness

### Week 4: Safety & Validation Systems
- [ ] Build crisis detection system
  - Pattern recognition for concerning content
  - Automatic flagging and alerts
  - Resource recommendation engine

- [ ] Implement bias monitoring
  - Stereotype detection
  - Outcome fairness analysis
  - Cultural sensitivity checks

- [ ] Create validation framework
  - Compare outputs to clinical research
  - Expert review system
  - Accuracy tracking

## 📋 Phase 2: MVP Development (Weeks 5-8)

### Week 5: Frontend Adaptation
- [ ] Redesign UI for clinical context
  - Professional, calming aesthetic
  - Accessibility-first (WCAG 2.1 AA)
  - Clear safety disclaimers

- [ ] Modify Step 1: Scenario Input
  - Clinical vignette upload
  - Scenario type selection
  - Goal definition

- [ ] Modify Step 2: Profile Setup
  - Agent role assignment
  - Mental health profile configuration
  - Support network design

### Week 6: Intervention System
- [ ] Create intervention library
  - CBT protocols
  - DBT skills
  - Medication management
  - Peer support models
  - Crisis intervention procedures

- [ ] Build intervention configuration UI
  - Select therapy type
  - Set frequency/duration
  - Assign providers
  - Define goals

- [ ] Implement life event system
  - Stressor library
  - Positive event library
  - Timing configuration
  - Severity settings

### Week 7: Simulation & Visualization
- [ ] Adapt simulation runner
  - Mental health context
  - Therapeutic interactions
  - Progress tracking
  - Critical moment detection

- [ ] Create visualization components
  - Mental health trajectory graphs
  - Intervention timeline
  - Social network diagram
  - Risk/protective factor charts

### Week 8: Report Generation
- [ ] Adapt `report_agent.py` → `clinical_report_agent.py`
  - Mental health-focused analysis
  - Evidence-based recommendations
  - Risk factor identification
  - Protective factor analysis
  - Treatment effectiveness assessment

- [ ] Add clinical validation
  - Link to research citations
  - Compare to known outcomes
  - Confidence intervals
  - Limitations section

## 📋 Phase 3: Clinical Validation (Weeks 9-12)

### Week 9: Expert Review System
- [ ] Recruit clinical advisors
  - Psychiatrists
  - Psychologists
  - Social workers
  - Peer support specialists

- [ ] Create review protocol
  - Scenario validation
  - Output assessment
  - Bias detection
  - Safety verification

### Week 10: Test Scenarios
- [ ] Develop validated test cases
  - Depression + CBT
  - Anxiety + exposure therapy
  - PTSD + trauma-focused therapy
  - Bipolar + medication management
  - Substance use + peer support

- [ ] Run simulations
- [ ] Compare to research literature
- [ ] Document accuracy and limitations

### Week 11: Refinement
- [ ] Incorporate expert feedback
- [ ] Fix identified issues
- [ ] Enhance safety features
- [ ] Improve clinical accuracy

### Week 12: Documentation
- [ ] User guide for professionals
- [ ] Clinical validation report
- [ ] Ethical guidelines
- [ ] Training materials

## 📋 Phase 4: Pilot Program (Weeks 13-16)

### Week 13: Pilot Setup
- [ ] Partner with university program
- [ ] Train pilot users
- [ ] Set up monitoring system
- [ ] Establish feedback channels

### Week 14-15: Supervised Use
- [ ] Students/trainees use system
- [ ] Faculty supervision
- [ ] Collect feedback
- [ ] Monitor for issues

### Week 16: Analysis & Iteration
- [ ] Analyze pilot results
- [ ] Assess learning outcomes
- [ ] Identify improvements
- [ ] Plan next phase

## 🔧 Key Technical Changes from MiroFish

### File Renames & Adaptations

```
MiroFish → MentalHealthSim

backend/app/services/
├── graph_builder.py → profile_builder.py
├── oasis_profile_generator.py → agent_profile_generator.py
├── simulation_config_generator.py → scenario_config_generator.py
├── report_agent.py → clinical_report_agent.py
├── ontology_generator.py → clinical_profile_extractor.py
└── NEW: crisis_detector.py
└── NEW: bias_monitor.py
└── NEW: clinical_validator.py

frontend/src/components/
├── Step1GraphBuild.vue → Step1ScenarioInput.vue
├── Step2EnvSetup.vue → Step2ProfileSetup.vue
├── Step3Simulation.vue → Step3Simulation.vue (adapted)
├── Step4Report.vue → Step4ClinicalReport.vue
└── Step5Interaction.vue → Step5Analysis.vue
└── NEW: SafetyDisclaimer.vue
└── NEW: CrisisResources.vue
```

### New Configuration Variables

```env
# Clinical LLM (needs nuanced understanding)
CLINICAL_LLM_MODEL=gpt-4-turbo  # or claude-3-opus

# Safety features
CRISIS_DETECTION_ENABLED=true
BIAS_MONITORING_ENABLED=true
PROFESSIONAL_VERIFICATION_REQUIRED=true

# Clinical validation
RESEARCH_DATABASE_API_KEY=your_pubmed_api_key
CLINICAL_VALIDATION_THRESHOLD=0.85

# Metrics tracking
MENTAL_HEALTH_METRICS=PHQ9,GAD7,PCL5,FUNCTIONING
SIMULATION_TIME_SCALE=1_round_1_week
DEFAULT_SIMULATION_DURATION=24  # 24 weeks / 6 months
```

### New Database Models

```python
# models/clinical_profile.py
class ClinicalProfile:
    agent_id: str
    mental_health_history: List[str]
    current_symptoms: Dict[str, int]
    coping_strategies: List[str]
    support_network_quality: float
    treatment_history: List[Dict]
    risk_factors: List[str]
    protective_factors: List[str]

# models/intervention.py
class Intervention:
    intervention_id: str
    type: str  # CBT, DBT, medication, etc.
    provider_agent_id: str
    frequency: str
    duration_weeks: int
    goals: List[str]
    evidence_base: str  # link to research

# models/mental_health_metric.py
class MentalHealthMetric:
    metric_id: str
    agent_id: str
    round_number: int
    metric_type: str  # mood, anxiety, functioning
    score: float
    notes: str
```

## 🛡️ Safety Implementation Details

### Crisis Detection System
```python
# services/crisis_detector.py

class CrisisDetector:
    def __init__(self):
        self.risk_keywords = [
            # Loaded from clinical guidelines
        ]
        self.severity_model = load_model()
    
    def analyze_agent_state(self, agent_state):
        """Detect crisis indicators"""
        risk_level = self.assess_risk(agent_state)
        if risk_level >= CRITICAL_THRESHOLD:
            self.trigger_alert(agent_state)
            return {
                'crisis_detected': True,
                'risk_level': risk_level,
                'recommended_actions': self.get_interventions(),
                'resources': self.get_crisis_resources()
            }
    
    def get_crisis_resources(self):
        return {
            'suicide_prevention': '988',
            'crisis_text': 'Text HOME to 741741',
            'emergency': '911',
            'warmline': '...'
        }
```

### Bias Monitoring System
```python
# services/bias_monitor.py

class BiasMonitor:
    def __init__(self):
        self.fairness_metrics = []
        self.stereotype_patterns = load_patterns()
    
    def audit_simulation(self, simulation_results):
        """Check for biased outcomes"""
        issues = []
        
        # Check outcome fairness across demographics
        fairness_score = self.assess_fairness(simulation_results)
        
        # Detect stereotypes
        stereotypes = self.detect_stereotypes(simulation_results)
        
        # Check for unrealistic outcomes
        realism_score = self.validate_realism(simulation_results)
        
        return {
            'fairness_score': fairness_score,
            'stereotypes_detected': stereotypes,
            'realism_score': realism_score,
            'issues': issues
        }
```

## 📊 Success Criteria

### Phase 1 (Foundation)
- ✅ All safety systems implemented
- ✅ Ethical guidelines documented
- ✅ Core architecture adapted

### Phase 2 (MVP)
- ✅ One complete scenario type working
- ✅ Basic simulation runs successfully
- ✅ Reports generated with citations
- ✅ No safety violations in testing

### Phase 3 (Validation)
- ✅ 3+ clinical experts validate approach
- ✅ 5+ test scenarios match research outcomes
- ✅ Zero harmful recommendations
- ✅ Bias audit passes

### Phase 4 (Pilot)
- ✅ 10+ users complete training scenarios
- ✅ Positive learning outcomes measured
- ✅ No safety incidents
- ✅ 80%+ user satisfaction

## 🤝 Collaboration Needs

### Clinical Expertise
- Psychiatrist (medication management)
- Clinical psychologist (therapy protocols)
- Social worker (systems perspective)
- Peer support specialist (lived experience)

### Technical Expertise
- ML engineer (bias detection, validation)
- UX designer (accessibility, clinical UI)
- Security engineer (data protection)

### Research Support
- Access to clinical databases
- Literature review assistance
- IRB guidance for research use

## 💰 Resource Requirements

### Development
- 3-4 months full-time development
- Clinical advisor stipends
- LLM API costs (~$500-1000/month during development)
- Cloud hosting (~$100-200/month)

### Validation
- Expert review compensation
- Pilot program support
- Research database access

### Ongoing
- Clinical advisory board
- Continuous validation
- Safety monitoring
- Updates based on new research

## 🚀 Launch Strategy

### Phase 1: Closed Beta
- University partners only
- Supervised use
- Extensive monitoring

### Phase 2: Professional Access
- Credential verification required
- Training completion mandatory
- Usage monitoring

### Phase 3: Research Platform
- Open to qualified researchers
- Data sharing agreements
- Publication support

### Phase 4: Educational Tool
- Broader access for training
- Public demo scenarios
- Stigma reduction campaigns

---

## ⚠️ Critical Reminders

1. **Safety First**: Every feature must pass safety review
2. **Clinical Validity**: All outputs must align with research
3. **Transparency**: Clear about limitations and uncertainties
4. **Professional Use**: Not for self-diagnosis or self-treatment
5. **Continuous Improvement**: Regular updates based on new research
6. **Community Input**: Ongoing engagement with stakeholders

---

**Next Step**: Review this plan with clinical advisors before starting development.
