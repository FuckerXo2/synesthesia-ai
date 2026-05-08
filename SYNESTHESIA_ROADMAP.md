# Synesthesia - Implementation Roadmap

## 🎯 From MiroFish to Synesthesia: 16-Week Plan

This roadmap transforms MiroFish (social prediction engine) into Synesthesia (mental health community simulator).

---

## 📋 Phase 1: Foundation (Weeks 1-4)

### Week 1: Setup & Core Adaptations

**Goal:** Get MiroFish running and understand the architecture

**Tasks:**
- [ ] Copy MiroFish codebase to `synesthesia` directory
- [ ] Install all dependencies and verify it runs
- [ ] Study key files:
  - `backend/app/services/graph_builder.py`
  - `backend/app/services/oasis_profile_generator.py`
  - `backend/app/services/simulation_manager.py`
  - `backend/app/services/report_agent.py`
- [ ] Document current data flow
- [ ] Identify all files that need adaptation

**Deliverables:**
- Working MiroFish installation
- Architecture documentation
- Adaptation plan

---

### Week 2: Community Profile Builder

**Goal:** Replace social network graph builder with mental health community profiler

**File Changes:**
```
graph_builder.py → community_profile_builder.py
```

**New Functionality:**
```python
class CommunityProfileBuilder:
    """
    Builds mental health community profiles from input data.
    
    Input: Community description, demographics, stressors
    Output: Mental health knowledge graph
    """
    
    def build_profile(self, community_data):
        """
        Extract:
        - Population characteristics
        - Mental health baseline (prevalence rates)
        - Social network structure
        - Existing resources
        - Stressors and protective factors
        """
        
    def create_knowledge_graph(self):
        """
        G = (V, E)
        V = {individuals, supporters, stressors, resources}
        E = {supports, triggers, protects, isolates}
        """
        
    def validate_profile(self):
        """
        Compare to epidemiological data
        Ensure realistic distributions
        """
```

**Tasks:**
- [ ] Design community profile schema
- [ ] Implement profile extraction from text
- [ ] Build mental health knowledge graph
- [ ] Add validation against epidemiological data
- [ ] Create test profiles (university, workplace, city)

**Deliverables:**
- `community_profile_builder.py` working
- 3 test community profiles
- Validation tests passing

---

### Week 3: Agent Population Generator

**Goal:** Generate diverse mental health agent populations

**File Changes:**
```
oasis_profile_generator.py → mental_health_agent_generator.py
```

**New Agent Types:**
```python
class AgentType(Enum):
    PRIMARY = "primary"              # Experiencing mental health challenges
    SUPPORTER = "supporter"          # Friends, family
    PROFESSIONAL = "professional"    # Therapists, counselors
    INFLUENCER = "influencer"        # Community leaders, social media
    INSTITUTIONAL = "institutional"  # Employers, schools

class MentalHealthAgent:
    agent_id: str
    agent_type: AgentType
    
    # Mental health state
    mood: float  # -10 to +10
    anxiety: float  # 0 to 10
    functioning: float  # 0 to 100
    crisis_risk: float  # 0 to 1
    
    # Personality
    openness: float
    support_giving: float
    stigma_internalization: float
    resilience: float
    
    # Social network
    connections: List[Connection]
    network_position: NetworkMetrics
    
    # Behavioral rules
    help_seeking_threshold: float
    support_offering_threshold: float
    stigma_spreading_likelihood: float
```

**Tasks:**
- [ ] Design agent schema
- [ ] Implement realistic mental health distributions
- [ ] Generate social networks (scale-free, clustered)
- [ ] Assign behavioral rules based on personality
- [ ] Create diverse agent populations
- [ ] Validate against demographic data

**Deliverables:**
- `mental_health_agent_generator.py` working
- Realistic agent populations
- Network structure validation

---

### Week 4: Simulation Environment Adaptation

**Goal:** Adapt OASIS social media simulation to mental health contexts

**File Changes:**
```
simulation_config_generator.py → mental_health_scenario_generator.py
simulation_runner.py → mental_health_simulation_runner.py
```

**New Interaction Contexts:**
```python
class InteractionContext(Enum):
    SOCIAL_MEDIA = "social_media"      # Stigma vs support
    THERAPY_SESSION = "therapy"         # Professional help
    PEER_SUPPORT = "peer_support"       # Support groups
    WORKPLACE = "workplace"             # Stress, support
    FAMILY = "family"                   # Conflict, support
    CRISIS_MOMENT = "crisis"            # Intervention
    COMMUNITY_SPACE = "community"       # Connection

class MentalHealthAction(Enum):
    SEEK_HELP = "seek_help"
    OFFER_SUPPORT = "offer_support"
    SHARE_STRUGGLE = "share_struggle"
    HIDE_STRUGGLE = "hide_struggle"
    SPREAD_STIGMA = "spread_stigma"
    CHALLENGE_STIGMA = "challenge_stigma"
    ISOLATE = "isolate"
    REACH_OUT = "reach_out"
    INTERVENE_CRISIS = "intervene_crisis"
    USE_COPING_SKILL = "use_coping_skill"
    DO_NOTHING = "do_nothing"
```

**Tasks:**
- [ ] Define mental health interaction contexts
- [ ] Implement action types for each context
- [ ] Adapt OASIS engine for mental health dynamics
- [ ] Create state update rules
- [ ] Implement social contagion mechanics
- [ ] Add crisis detection during simulation

**Deliverables:**
- Mental health simulation engine working
- Multiple interaction contexts implemented
- State update rules validated

---

## 📋 Phase 2: Core Features (Weeks 5-8)

### Week 5: Intervention System

**Goal:** Build intervention testing framework

**New Files:**
```
backend/app/services/intervention_engine.py
backend/app/models/intervention.py
```

**Intervention Types:**
```python
class InterventionType(Enum):
    INDIVIDUAL = "individual"      # Therapy, medication
    COMMUNITY = "community"        # Peer support, campaigns
    SYSTEMIC = "systemic"          # Policy, infrastructure
    COMBINED = "combined"          # Multi-level

class Intervention:
    intervention_id: str
    name: str
    type: InterventionType
    components: List[InterventionComponent]
    target_population: str
    cost: float
    duration_weeks: int
    expected_mechanisms: List[str]
    
class InterventionComponent:
    component_type: str  # therapy, peer_support, training, etc.
    frequency: str
    intensity: str
    provider: str
```

**Tasks:**
- [ ] Design intervention schema
- [ ] Implement intervention library (CBT, peer support, etc.)
- [ ] Create intervention application logic
- [ ] Build intervention comparison framework
- [ ] Add cost tracking
- [ ] Implement mechanism tracking

**Deliverables:**
- Intervention engine working
- Library of 10+ evidence-based interventions
- Comparison framework functional

---

### Week 6: Metrics & Tracking

**Goal:** Track mental health outcomes and dynamics

**New Files:**
```
backend/app/services/metrics_tracker.py
backend/app/models/mental_health_metric.py
```

**Metrics to Track:**
```python
class MetricType(Enum):
    # Individual level
    MOOD = "mood"
    ANXIETY = "anxiety"
    FUNCTIONING = "functioning"
    CRISIS_RISK = "crisis_risk"
    HELP_SEEKING = "help_seeking"
    
    # Population level
    CRISIS_RATE = "crisis_rate"
    HELP_SEEKING_RATE = "help_seeking_rate"
    RECOVERY_RATE = "recovery_rate"
    STIGMA_LEVEL = "stigma_level"
    SOCIAL_ISOLATION = "social_isolation"
    SUPPORT_QUALITY = "support_quality"
    
    # Network level
    NETWORK_DENSITY = "network_density"
    CLUSTERING = "clustering"
    ISOLATION_RATE = "isolation_rate"

class MetricsTracker:
    def track_individual(self, agent_id, time_step):
        """Track individual agent metrics"""
        
    def track_population(self, time_step):
        """Track population-level metrics"""
        
    def track_network(self, time_step):
        """Track network dynamics"""
        
    def detect_cascades(self):
        """Identify positive/negative cascades"""
        
    def identify_leverage_points(self):
        """Find high-impact agents"""
```

**Tasks:**
- [ ] Implement metrics tracking system
- [ ] Add real-time monitoring
- [ ] Create cascade detection
- [ ] Build leverage point identification
- [ ] Add visualization data export
- [ ] Implement statistical analysis

**Deliverables:**
- Comprehensive metrics tracking
- Cascade detection working
- Leverage point identification functional

---

### Week 7: Report Generation

**Goal:** Adapt report agent for mental health insights

**File Changes:**
```
report_agent.py → mental_health_report_agent.py
```

**New Report Structure:**
```python
class MentalHealthReport:
    """
    Generates evidence-based reports on simulation outcomes
    """
    
    sections = [
        "Executive Summary",
        "Baseline Community Profile",
        "Crisis Event Impact",
        "Intervention Comparisons",
        "Outcome Distributions",
        "Network Effects Analysis",
        "Leverage Points Identified",
        "ROI Analysis",
        "Unintended Consequences",
        "Recommendations",
        "Validation Against Research",
        "Limitations and Uncertainties",
        "Next Steps"
    ]
    
    def generate_executive_summary(self):
        """Key findings and recommendations"""
        
    def compare_interventions(self):
        """Side-by-side effectiveness comparison"""
        
    def analyze_network_effects(self):
        """How interventions spread through networks"""
        
    def calculate_roi(self):
        """Value created per dollar spent"""
        
    def identify_leverage_points(self):
        """Which agents/interventions have outsized impact"""
        
    def validate_against_research(self):
        """Compare to published studies"""
```

**Tasks:**
- [ ] Adapt report agent for mental health context
- [ ] Implement new report sections
- [ ] Add intervention comparison logic
- [ ] Build ROI calculation
- [ ] Add research validation
- [ ] Create visualizations

**Deliverables:**
- Mental health report agent working
- Comprehensive report generation
- Research validation integrated

---

### Week 8: Frontend Adaptation

**Goal:** Redesign UI for mental health community simulation

**File Changes:**
```
Step1GraphBuild.vue → Step1CommunityProfile.vue
Step2EnvSetup.vue → Step2InterventionDesign.vue
Step3Simulation.vue → Step3Simulation.vue (adapted)
Step4Report.vue → Step4Results.vue
Step5Interaction.vue → Step5Analysis.vue
```

**New Components:**
```
SafetyDisclaimer.vue
CrisisResources.vue
CommunityProfileBuilder.vue
InterventionDesigner.vue
MetricsVisualization.vue
NetworkVisualization.vue
ROIComparison.vue
```

**Tasks:**
- [ ] Redesign UI for mental health context
- [ ] Add safety disclaimers on all pages
- [ ] Create community profile builder UI
- [ ] Build intervention designer interface
- [ ] Implement metrics visualizations
- [ ] Add network visualization
- [ ] Create ROI comparison charts
- [ ] Ensure accessibility (WCAG 2.1 AA)

**Deliverables:**
- Complete UI redesign
- All components functional
- Accessibility compliance

---

## 📋 Phase 3: Validation (Weeks 9-12)

### Week 9: Research Validation System

**Goal:** Compare simulation results to published research

**New Files:**
```
backend/app/services/research_validator.py
backend/app/data/research_database.json
```

**Validation Approach:**
```python
class ResearchValidator:
    """
    Validates simulation results against published research
    """
    
    def load_research_database(self):
        """
        Load studies on:
        - Peer support effectiveness
        - Therapy outcomes
        - Crisis intervention
        - Stigma reduction
        - Network effects
        """
        
    def compare_to_research(self, simulation_results):
        """
        Compare:
        - Effect sizes
        - Outcome distributions
        - Time courses
        - Moderators
        """
        
    def calculate_alignment_score(self):
        """
        How well do simulations match real-world studies?
        Target: 80%+ alignment
        """
        
    def identify_discrepancies(self):
        """
        Where do simulations diverge from research?
        Why? How to fix?
        """
```

**Tasks:**
- [ ] Build research database (50+ studies)
- [ ] Implement comparison algorithms
- [ ] Calculate alignment scores
- [ ] Identify and fix discrepancies
- [ ] Document validation results
- [ ] Create validation report

**Deliverables:**
- Research validation system working
- 80%+ alignment with published studies
- Validation documentation

---

### Week 10: Bias Auditing

**Goal:** Ensure fair outcomes across demographics

**New Files:**
```
backend/app/services/bias_auditor.py
```

**Bias Checks:**
```python
class BiasAuditor:
    """
    Audits simulations for bias and unfairness
    """
    
    def audit_outcome_fairness(self):
        """
        Check if outcomes are fair across:
        - Race/ethnicity
        - Gender
        - Socioeconomic status
        - Age
        - Disability status
        """
        
    def detect_stereotypes(self):
        """
        Check for:
        - Stigmatizing language
        - Stereotypical behaviors
        - Unfair assumptions
        """
        
    def assess_representation(self):
        """
        Are all groups represented?
        Are minorities included?
        """
        
    def calculate_fairness_metrics(self):
        """
        - Demographic parity
        - Equal opportunity
        - Predictive parity
        """
```

**Tasks:**
- [ ] Implement bias auditing system
- [ ] Run audits on all scenarios
- [ ] Fix identified biases
- [ ] Document fairness metrics
- [ ] Create ongoing monitoring

**Deliverables:**
- Bias auditing system working
- All scenarios passing fairness checks
- Ongoing monitoring in place

---

### Week 11: Expert Review

**Goal:** Get validation from mental health professionals

**Process:**
1. Recruit 5+ clinical experts:
   - Psychiatrist
   - Clinical psychologist
   - Social worker
   - Peer support specialist
   - Public health expert

2. Review protocol:
   - Scenario realism
   - Agent behavior accuracy
   - Intervention mechanisms
   - Outcome plausibility
   - Ethical considerations

3. Iterate based on feedback

**Tasks:**
- [ ] Recruit expert reviewers
- [ ] Prepare review materials
- [ ] Conduct review sessions
- [ ] Document feedback
- [ ] Implement changes
- [ ] Get final approval

**Deliverables:**
- 5+ expert reviews completed
- Feedback incorporated
- Expert endorsements

---

### Week 12: Documentation & Testing

**Goal:** Complete documentation and comprehensive testing

**Documentation:**
- [ ] User guide
- [ ] Technical documentation
- [ ] API reference
- [ ] Research validation report
- [ ] Ethical guidelines
- [ ] Case studies

**Testing:**
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] End-to-end tests
- [ ] Performance tests
- [ ] Security tests
- [ ] Accessibility tests

**Deliverables:**
- Complete documentation
- Comprehensive test suite
- All tests passing

---

## 📋 Phase 4: Pilot (Weeks 13-16)

### Week 13: Pilot Setup

**Goal:** Prepare for real-world pilot program

**Partner Selection:**
- University with mental health challenges
- Willing to test Synesthesia for planning
- Has data for validation
- Committed to feedback

**Pilot Scope:**
- One scenario (e.g., crisis response planning)
- 4-week pilot period
- Weekly check-ins
- Feedback collection

**Tasks:**
- [ ] Secure pilot partner
- [ ] Sign agreements
- [ ] Set up pilot environment
- [ ] Train pilot users
- [ ] Establish feedback channels
- [ ] Define success metrics

**Deliverables:**
- Pilot partner secured
- Pilot environment ready
- Users trained

---

### Week 14-15: Pilot Execution

**Goal:** Run pilot and collect data

**Activities:**
- Week 14:
  - [ ] Pilot users run first simulations
  - [ ] Daily support and troubleshooting
  - [ ] Collect usage data
  - [ ] Weekly feedback session

- Week 15:
  - [ ] Pilot users run additional scenarios
  - [ ] Test different interventions
  - [ ] Compare to their intuitions
  - [ ] Weekly feedback session

**Data Collection:**
- Usage metrics
- User satisfaction
- Accuracy perceptions
- Feature requests
- Bug reports
- Success stories

**Deliverables:**
- Pilot completed
- Data collected
- Feedback documented

---

### Week 16: Analysis & Iteration

**Goal:** Analyze pilot results and plan next phase

**Analysis:**
- [ ] Usage patterns
- [ ] User satisfaction scores
- [ ] Accuracy validation (if real-world data available)
- [ ] Feature gaps
- [ ] Bug frequency
- [ ] ROI for pilot partner

**Iteration:**
- [ ] Fix critical bugs
- [ ] Implement high-priority features
- [ ] Improve documentation
- [ ] Refine UX based on feedback

**Next Phase Planning:**
- [ ] Expand to more partners?
- [ ] Add new scenarios?
- [ ] Build additional features?
- [ ] Seek funding?
- [ ] Publish research?

**Deliverables:**
- Pilot analysis report
- Iteration plan
- Next phase roadmap

---

## 🔧 Technical Changes Summary

### File Renames & Adaptations

```
MiroFish → Synesthesia

backend/app/services/
├── graph_builder.py → community_profile_builder.py
├── oasis_profile_generator.py → mental_health_agent_generator.py
├── simulation_config_generator.py → mental_health_scenario_generator.py
├── simulation_manager.py → mental_health_simulation_manager.py
├── simulation_runner.py → mental_health_simulation_runner.py
├── report_agent.py → mental_health_report_agent.py
├── ontology_generator.py → community_profile_extractor.py
└── NEW FILES:
    ├── intervention_engine.py
    ├── metrics_tracker.py
    ├── research_validator.py
    ├── bias_auditor.py
    └── crisis_detector.py (from example)

backend/app/models/
├── project.py → community.py
├── task.py → scenario.py
└── NEW FILES:
    ├── agent.py
    ├── intervention.py
    ├── mental_health_metric.py
    └── simulation_result.py

frontend/src/components/
├── Step1GraphBuild.vue → Step1CommunityProfile.vue
├── Step2EnvSetup.vue → Step2InterventionDesign.vue
├── Step3Simulation.vue → Step3Simulation.vue (adapted)
├── Step4Report.vue → Step4Results.vue
├── Step5Interaction.vue → Step5Analysis.vue
└── NEW FILES:
    ├── SafetyDisclaimer.vue
    ├── CrisisResources.vue
    ├── CommunityProfileBuilder.vue
    ├── InterventionDesigner.vue
    ├── MetricsVisualization.vue
    ├── NetworkVisualization.vue
    └── ROIComparison.vue
```

### New Environment Variables

```env
# Synesthesia-specific
SIMULATION_MODE=mental_health
DEFAULT_POPULATION_SIZE=1000
DEFAULT_SIMULATION_WEEKS=24
CRISIS_DETECTION_ENABLED=true
BIAS_MONITORING_ENABLED=true

# Metrics
MENTAL_HEALTH_METRICS=mood,anxiety,functioning,crisis_risk
POPULATION_METRICS=crisis_rate,help_seeking_rate,recovery_rate
NETWORK_METRICS=isolation,support_quality,clustering

# Validation
RESEARCH_VALIDATION_ENABLED=true
RESEARCH_DATABASE_PATH=backend/app/data/research_database.json
ALIGNMENT_THRESHOLD=0.80

# Safety
CRISIS_ALERT_THRESHOLD=0.8
BIAS_AUDIT_THRESHOLD=0.9
EXPERT_REVIEW_REQUIRED=true
```

---

## 📊 Success Metrics

### Phase 1 (Foundation)
- ✅ All core files adapted
- ✅ Community profile builder working
- ✅ Agent generator creating realistic populations
- ✅ Simulation engine running mental health scenarios

### Phase 2 (Core Features)
- ✅ Intervention system functional
- ✅ Metrics tracking comprehensive
- ✅ Report generation working
- ✅ UI redesigned and accessible

### Phase 3 (Validation)
- ✅ 80%+ alignment with research
- ✅ Bias audits passing
- ✅ 5+ expert reviews positive
- ✅ Documentation complete

### Phase 4 (Pilot)
- ✅ Pilot partner secured
- ✅ Pilot completed successfully
- ✅ Positive user feedback
- ✅ Real-world validation (if possible)

---

## 💰 Resource Requirements

### Development Time
- **Full-time**: 16 weeks (4 months)
- **Part-time**: 32 weeks (8 months)

### Team
- **Minimum**: 1 developer + 1 clinical advisor
- **Recommended**: 1 developer + 2 clinical advisors + 1 UX designer
- **Ideal**: 2 developers + 3 clinical advisors + 1 UX designer + 1 researcher

### Budget
- **Development**: $0-10K (if self-developed)
- **LLM API**: $1,000-2,000 (for 16 weeks)
- **Clinical advisors**: $5,000-10,000 (stipends)
- **Pilot program**: $2,000-5,000
- **Total**: $8,000-27,000

### Infrastructure
- LLM API access (GPT-4 or Claude)
- Zep Cloud (free tier sufficient for development)
- Cloud hosting (AWS/GCP/Azure)
- Development machines

---

## 🚧 Risk Mitigation

### Technical Risks
- **LLM inconsistency**: Use GPT-4 or Claude, add validation layers
- **Performance issues**: Optimize agent interactions, use caching
- **API costs**: Start small, scale gradually

### Clinical Risks
- **Inaccurate predictions**: Validate against research, expert review
- **Harmful recommendations**: Crisis detection, bias monitoring
- **Misuse**: Clear disclaimers, professional gating

### Adoption Risks
- **Skepticism**: Demonstrate validation, show ROI
- **Complexity**: Simplify UI, provide training
- **Cost concerns**: Show cost-effectiveness vs. alternatives

---

## 🎯 Milestones

### Month 1 (Weeks 1-4)
✅ Foundation complete
- Community profile builder
- Agent generator
- Simulation engine adapted

### Month 2 (Weeks 5-8)
✅ Core features complete
- Intervention system
- Metrics tracking
- Report generation
- UI redesigned

### Month 3 (Weeks 9-12)
✅ Validation complete
- Research validation (80%+ alignment)
- Bias audits passing
- Expert reviews positive
- Documentation complete

### Month 4 (Weeks 13-16)
✅ Pilot complete
- Pilot partner secured
- Pilot executed
- Feedback incorporated
- Next phase planned

---

## 🚀 Post-Roadmap: What's Next?

### Phase 5: Scale (Months 5-8)
- Add more scenario types (workplace, city, online)
- Expand intervention library
- Build optimization features
- Create research platform

### Phase 6: Research (Months 9-12)
- Publish validation studies
- Partner with universities
- Contribute to mental health research
- Build academic community

### Phase 7: Impact (Year 2+)
- Widespread adoption by universities, cities, organizations
- Demonstrated real-world impact
- Policy influence
- Lives saved

---

**This roadmap is ambitious but achievable. Start with Phase 1, validate continuously, and iterate based on feedback.**

**The goal: Build a tool that helps communities make evidence-based mental health decisions - and saves lives.**
