# Getting Started with MentalHealthSim

## 🎯 Quick Start Guide

This guide will help you begin adapting MiroFish for mental health simulation.

## ⚠️ Before You Begin

### Critical Prerequisites

1. **Clinical Expertise**: Partner with licensed mental health professionals
2. **Ethical Review**: Consult with ethics board or IRB if affiliated with institution
3. **Safety Planning**: Establish crisis protocols and monitoring systems
4. **Legal Review**: Understand liability and regulatory requirements

### Technical Prerequisites

- Python 3.11+
- Node.js 18+
- `uv` package manager
- LLM API access (GPT-4 or Claude recommended for nuanced understanding)
- Zep Cloud account (or alternative memory system)

## 📁 Project Structure

```
mental-health-sim/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── profile_builder.py          # Clinical profile generation
│   │   │   ├── agent_profile_generator.py  # Agent persona creation
│   │   │   ├── scenario_config_generator.py # Simulation setup
│   │   │   ├── simulation_manager.py       # Orchestration
│   │   │   ├── simulation_runner.py        # Execution
│   │   │   ├── clinical_report_agent.py    # Report generation
│   │   │   ├── crisis_detector.py          # Safety monitoring
│   │   │   ├── bias_monitor.py             # Fairness auditing
│   │   │   └── clinical_validator.py       # Research validation
│   │   ├── models/
│   │   │   ├── clinical_profile.py
│   │   │   ├── intervention.py
│   │   │   ├── mental_health_metric.py
│   │   │   └── scenario.py
│   │   └── api/
│   │       ├── profile.py
│   │       ├── simulation.py
│   │       └── report.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SafetyDisclaimer.vue
│   │   │   ├── CrisisResources.vue
│   │   │   ├── Step1ScenarioInput.vue
│   │   │   ├── Step2ProfileSetup.vue
│   │   │   ├── Step3Simulation.vue
│   │   │   ├── Step4ClinicalReport.vue
│   │   │   └── Step5Analysis.vue
│   │   └── views/
│   └── package.json
├── docs/
│   ├── ethical_guidelines.md
│   ├── clinical_validation.md
│   ├── user_guide.md
│   └── research_citations.md
├── tests/
│   ├── safety_tests.py
│   ├── bias_tests.py
│   └── validation_tests.py
└── .env.example
```

## 🚀 Step-by-Step Setup

### Step 1: Copy and Adapt MiroFish

```bash
# Navigate to your workspace
cd /path/to/your/workspace

# Copy the MiroFish directory
cp -r MicroFish-En-main mental-health-sim
cd mental-health-sim

# Rename for clarity
mv README.md README_ORIGINAL.md
```

### Step 2: Update Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

Add these new variables:

```env
# Existing MiroFish variables
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4-turbo  # Better for nuanced mental health content

ZEP_API_KEY=your_zep_key

# New mental health-specific variables
CLINICAL_MODE=true
CRISIS_DETECTION_ENABLED=true
BIAS_MONITORING_ENABLED=true
PROFESSIONAL_VERIFICATION_REQUIRED=true

# Simulation defaults
DEFAULT_SIMULATION_DURATION=24  # weeks
SIMULATION_TIME_SCALE=1_round_1_week
MENTAL_HEALTH_METRICS=mood,anxiety,functioning,social_connection

# Safety thresholds
CRISIS_ALERT_THRESHOLD=0.8
BIAS_AUDIT_THRESHOLD=0.9

# Research validation
PUBMED_API_KEY=your_pubmed_key  # optional
CLINICAL_VALIDATION_ENABLED=true
```

### Step 3: Install Dependencies

```bash
# Install root and frontend dependencies
npm run setup

# Install backend dependencies
cd backend
uv sync
cd ..
```

### Step 4: Create Safety Components First

Create the crisis detector (highest priority):

```bash
touch backend/app/services/crisis_detector.py
```

I'll create this file for you with a basic implementation:

### Step 5: Modify Core Files

Start with the most critical adaptations:

1. **Profile Builder** (replaces graph_builder.py)
2. **Agent Profile Generator** (adapts oasis_profile_generator.py)
3. **Simulation Manager** (adapts simulation_manager.py)
4. **Clinical Report Agent** (adapts report_agent.py)

### Step 6: Update Frontend

1. Add safety disclaimer to all pages
2. Modify step components for clinical context
3. Update visualizations for mental health metrics
4. Add crisis resource links

### Step 7: Testing & Validation

```bash
# Run safety tests
python -m pytest tests/safety_tests.py

# Run bias audits
python -m pytest tests/bias_tests.py

# Validate against research
python -m pytest tests/validation_tests.py
```

## 📝 First Scenario to Build

### Recommended MVP Scenario: Depression + CBT

**Why this scenario?**
- Well-researched intervention
- Clear outcome measures (PHQ-9)
- Established protocols
- Good for training purposes

**Scenario Components:**

1. **Primary Agent**: Individual with moderate depression
   - PHQ-9 score: 15 (moderate)
   - History: Recent life stressor (job loss)
   - Coping: Some healthy, some avoidant
   - Support: Partner + 2 friends

2. **Intervention**: 12 weeks of CBT
   - Weekly sessions
   - Homework assignments
   - Thought records
   - Behavioral activation

3. **Support Agents**:
   - Therapist (CBT-trained)
   - Supportive partner
   - 2 friends (varying support quality)

4. **Life Events**:
   - Week 4: Job interview (stressor)
   - Week 8: Small success (protective)
   - Week 10: Family conflict (stressor)

5. **Metrics Tracked**:
   - PHQ-9 score (weekly)
   - Functioning level
   - Social engagement
   - Coping strategy use
   - Therapy homework completion

6. **Expected Outcome** (based on research):
   - 50-60% show significant improvement
   - PHQ-9 reduction of 5-8 points
   - Improved functioning
   - Better coping skills

## 🛡️ Safety Checklist

Before running any simulation:

- [ ] Safety disclaimer displayed prominently
- [ ] Crisis resources easily accessible
- [ ] Crisis detection system active
- [ ] Bias monitoring enabled
- [ ] Professional user verified
- [ ] Scenario reviewed by clinician
- [ ] Validation against research completed
- [ ] Limitations clearly stated
- [ ] Audit logging enabled

## 📚 Essential Reading

### Clinical Resources
- CBT protocols (Beck Institute)
- PHQ-9 and GAD-7 measures
- Evidence-based treatment guidelines
- Cultural considerations in mental health

### Technical Resources
- OASIS framework documentation
- LangChain for agent orchestration
- Bias detection in AI systems
- Clinical NLP best practices

### Ethical Resources
- APA Ethics Code
- NASW Code of Ethics
- AI ethics guidelines
- Research ethics (Belmont Report)

## 🤝 Building Your Team

### Minimum Viable Team

1. **Clinical Advisor** (psychiatrist or psychologist)
   - Validates scenarios
   - Reviews outputs
   - Ensures safety

2. **Developer** (you!)
   - Adapts codebase
   - Implements features
   - Maintains system

3. **Peer Reviewer** (another clinician)
   - Second opinion
   - Bias detection
   - Quality assurance

### Ideal Team (as you scale)

- Clinical psychologist
- Psychiatrist
- Social worker
- Peer support specialist
- ML engineer
- UX designer
- Ethics consultant

## 🎯 Milestones

### Week 1: Foundation
- [ ] Safety systems implemented
- [ ] Ethical guidelines documented
- [ ] Clinical advisor onboarded

### Week 2: Core Adaptation
- [ ] Profile builder working
- [ ] Agent generator adapted
- [ ] Basic simulation runs

### Week 3: First Scenario
- [ ] Depression + CBT scenario created
- [ ] Simulation completes successfully
- [ ] Report generated

### Week 4: Validation
- [ ] Clinical advisor reviews
- [ ] Compare to research outcomes
- [ ] Document limitations
- [ ] Plan next steps

## ⚠️ Common Pitfalls to Avoid

1. **Oversimplification**: Mental health is complex; avoid reductionist models
2. **Bias**: Ensure diverse representation and fair outcomes
3. **Overpromising**: Be clear about limitations and uncertainties
4. **Scope creep**: Start small, validate, then expand
5. **Ignoring safety**: Safety features are not optional
6. **Working alone**: Always involve clinical experts
7. **Treating as diagnostic**: This is research/training only

## 🆘 When Things Go Wrong

### If simulation produces concerning content:
1. Stop immediately
2. Document what happened
3. Review with clinical advisor
4. Improve crisis detection
5. Add safeguards
6. Test thoroughly before resuming

### If bias detected:
1. Analyze root cause
2. Review training data/prompts
3. Adjust agent generation
4. Re-test with diverse scenarios
5. Document and monitor

### If validation fails:
1. Compare to specific research
2. Identify discrepancies
3. Adjust model parameters
4. Consult clinical experts
5. Document limitations

## 📞 Resources & Support

### Crisis Resources (to include in app)
- **988 Suicide & Crisis Lifeline**: Call or text 988
- **Crisis Text Line**: Text HOME to 741741
- **SAMHSA National Helpline**: 1-800-662-4357
- **Emergency**: 911

### Professional Organizations
- American Psychological Association (APA)
- National Alliance on Mental Illness (NAMI)
- Mental Health America (MHA)
- Substance Abuse and Mental Health Services Administration (SAMHSA)

### Research Databases
- PubMed / PubMed Central
- PsycINFO
- Cochrane Library
- ClinicalTrials.gov

## 🚀 Ready to Start?

1. Review the design document
2. Consult with clinical advisor
3. Set up development environment
4. Start with safety features
5. Build first scenario
6. Validate thoroughly
7. Iterate based on feedback

---

**Remember**: This is a tool to support mental health professionals, not replace them. Every decision should prioritize safety, ethics, and clinical validity.

**Questions?** Document them and discuss with your clinical advisory team.

**Next Step**: Create the crisis detector service (see implementation roadmap).
