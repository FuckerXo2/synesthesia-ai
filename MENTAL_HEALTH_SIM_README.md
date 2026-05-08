# MentalHealthSim 🧠

**A Multi-Agent Simulation Platform for Mental Health Research and Training**

> ⚠️ **CRITICAL DISCLAIMER**: This is a RESEARCH and TRAINING tool ONLY. It is NOT for diagnosis, treatment, or clinical decision-making without professional oversight. Always consult licensed mental health professionals.

---

## 🎯 What is MentalHealthSim?

MentalHealthSim adapts multi-agent simulation technology to model mental health scenarios, enabling:

- **Training** mental health professionals with realistic scenarios
- **Testing** intervention strategies before real-world application
- **Understanding** social dynamics affecting mental wellbeing
- **Exploring** treatment options in a safe digital environment
- **Researching** mental health system dynamics

### What It Is NOT

❌ A diagnostic tool  
❌ A replacement for therapy or counseling  
❌ A self-help application  
❌ A clinical decision-making system  
❌ A substitute for professional mental health care  

### What It IS

✅ A training platform for professionals  
✅ A research tool for intervention testing  
✅ An educational resource for understanding mental health  
✅ A simulation environment for exploring scenarios  
✅ A tool to support (not replace) clinical expertise  

---

## 🏗️ Architecture

Built on the MiroFish multi-agent framework, adapted for mental health contexts:

### Core Components

1. **Profile Builder**: Generates realistic agent profiles with mental health histories
2. **Scenario Designer**: Creates therapeutic environments and life events
3. **Simulation Engine**: Runs agent interactions over time
4. **Crisis Detector**: Monitors for safety concerns in real-time
5. **Bias Monitor**: Ensures fair and unbiased outcomes
6. **Clinical Validator**: Compares results to research literature
7. **Report Generator**: Creates evidence-based analysis reports

### Tech Stack

- **Backend**: Python 3.11+ (Flask)
- **Frontend**: Vue 3 + Vite
- **LLM**: GPT-4 or Claude (for nuanced understanding)
- **Memory**: Zep Cloud or custom solution
- **Simulation**: Adapted OASIS framework

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- `uv` package manager
- LLM API access (OpenAI or Anthropic)
- Clinical advisor (required for validation)

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd mental-health-sim

# Install dependencies
npm run setup:all

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Start development servers
npm run dev
```

### First Run

1. Review safety disclaimers
2. Load example scenario (Depression + CBT)
3. Run simulation (supervised)
4. Review generated report
5. Validate against research

---

## 📊 Example Scenarios

### Scenario 1: Depression + CBT (MVP)

**Profile**: 28-year-old with moderate depression following job loss

**Intervention**: 12 weeks of Cognitive Behavioral Therapy

**Metrics**: PHQ-9, functioning, social engagement

**Expected Outcome**: 50-60% show significant improvement (based on research)

### Scenario 2: Anxiety + Exposure Therapy

**Profile**: 35-year-old with social anxiety

**Intervention**: Graduated exposure + cognitive restructuring

**Metrics**: GAD-7, avoidance behaviors, quality of life

### Scenario 3: PTSD + Trauma-Focused Therapy

**Profile**: 42-year-old veteran with PTSD

**Intervention**: Prolonged Exposure or CPT

**Metrics**: PCL-5, functioning, sleep quality

---

## 🛡️ Safety Features

### Built-In Safeguards

1. **Crisis Detection System**
   - Real-time monitoring for concerning content
   - Automatic alerts for high-risk scenarios
   - Immediate resource recommendations

2. **Bias Monitoring**
   - Fairness audits across demographics
   - Stereotype detection
   - Outcome equity analysis

3. **Clinical Validation**
   - Comparison to peer-reviewed research
   - Expert review protocols
   - Accuracy tracking

4. **Professional Gating**
   - Credential verification required
   - Training completion mandatory
   - Supervised use for students

### Crisis Resources (Always Visible)

- **988 Suicide & Crisis Lifeline**: Call or text 988
- **Crisis Text Line**: Text HOME to 741741
- **SAMHSA Helpline**: 1-800-662-4357
- **Emergency**: 911

---

## 📚 Documentation

- [Design Document](MENTAL_HEALTH_SIM_DESIGN.md) - Full system design
- [Implementation Roadmap](IMPLEMENTATION_ROADMAP.md) - Development plan
- [Getting Started Guide](GETTING_STARTED.md) - Setup instructions
- [Ethical Guidelines](docs/ethical_guidelines.md) - Ethics framework
- [Clinical Validation](docs/clinical_validation.md) - Validation process

---

## 🎓 Use Cases

### Appropriate Uses

✅ **Clinical Training**
- Medical students learning psychiatry
- Psychology graduate students
- Social work training programs
- Continuing education for professionals

✅ **Research**
- Testing intervention hypotheses
- Understanding treatment mechanisms
- Exploring system dynamics
- Comparative effectiveness research

✅ **Treatment Planning**
- Exploring options with supervision
- Understanding potential outcomes
- Identifying risk factors
- Optimizing intervention timing

✅ **Education**
- Reducing mental health stigma
- Teaching about interventions
- Demonstrating social support importance
- Understanding recovery trajectories

### Inappropriate Uses

❌ Self-diagnosis or self-treatment  
❌ Clinical decisions without professional oversight  
❌ Simulating real individuals without consent  
❌ Marketing or commercial exploitation  
❌ Replacing actual therapy or counseling  

---

## 🤝 Team & Governance

### Required Team Members

1. **Clinical Advisor** (psychiatrist or psychologist)
   - Validates scenarios and outputs
   - Ensures safety and accuracy
   - Reviews all major changes

2. **Developer** (software engineer)
   - Maintains codebase
   - Implements features
   - Ensures system reliability

3. **Ethics Consultant**
   - Reviews ethical implications
   - Ensures responsible use
   - Guides policy decisions

### Advisory Board (Recommended)

- Clinical psychologist
- Psychiatrist
- Social worker
- Peer support specialist
- Ethicist
- Community representatives

---

## 📈 Validation & Quality

### Clinical Validity

- All scenarios validated against research literature
- Expert clinician review required
- Continuous accuracy monitoring
- Regular updates based on new evidence

### Safety Metrics

- Zero harmful recommendations (target)
- 100% crisis detection rate (target)
- Regular bias audits
- Incident tracking and response

### Educational Effectiveness

- Learning outcome assessments
- User satisfaction surveys
- Professional feedback integration
- Continuous improvement cycles

---

## 🔬 Research Foundation

### Evidence-Based Interventions

- **CBT**: Beck Institute protocols
- **DBT**: Linehan's model
- **ACT**: Hayes et al. framework
- **Trauma-Focused**: PE, CPT, EMDR
- **Medication**: Evidence-based pharmacotherapy

### Validated Measures

- **PHQ-9**: Depression screening
- **GAD-7**: Anxiety assessment
- **PCL-5**: PTSD symptoms
- **WHODAS**: Functioning
- **Quality of Life**: Various scales

### Research Integration

- PubMed/PsycINFO integration
- Automatic citation generation
- Regular literature reviews
- Expert consensus updates

---

## 🌍 Diversity & Inclusion

### Cultural Considerations

- Multiple cultural backgrounds represented
- Various family structures included
- Different healthcare access levels
- Diverse coping traditions
- Language and communication styles
- Stigma variations across cultures

### Bias Prevention

- Regular fairness audits
- Diverse clinical advisory board
- Community input and feedback
- Transparent limitations
- Continuous monitoring

---

## 📞 Support & Resources

### For Users

- User guide and tutorials
- Video demonstrations
- FAQ and troubleshooting
- Clinical advisor consultation
- Technical support

### For Researchers

- API documentation
- Data export capabilities
- Research collaboration opportunities
- Publication support
- IRB guidance

### For Developers

- Technical documentation
- Contribution guidelines
- Code review process
- Testing requirements
- Security protocols

---

## 🚦 Current Status

### Phase 1: Foundation ✅
- [x] Design document completed
- [x] Implementation roadmap created
- [x] Safety systems designed
- [ ] Clinical advisor onboarded
- [ ] Ethics review completed

### Phase 2: MVP Development 🚧
- [ ] Core architecture adapted
- [ ] First scenario implemented
- [ ] Safety systems operational
- [ ] Basic UI functional

### Phase 3: Validation 📋
- [ ] Clinical expert review
- [ ] Research comparison
- [ ] Bias audits
- [ ] Safety testing

### Phase 4: Pilot 🎯
- [ ] University partnership
- [ ] Student training
- [ ] Feedback collection
- [ ] Iteration and improvement

---

## 🤝 Contributing

We welcome contributions from:

- Mental health professionals
- Software developers
- UX/UI designers
- Researchers
- Community advocates

### Contribution Guidelines

1. Review ethical guidelines
2. Discuss proposed changes with clinical advisor
3. Follow code review process
4. Include tests and documentation
5. Ensure safety compliance

---

## 📄 License

[To be determined - likely AGPL-3.0 with additional ethical use restrictions]

### Ethical Use Requirements

Any use of this software must:

1. Prioritize user safety and wellbeing
2. Include appropriate disclaimers
3. Require professional oversight
4. Protect privacy and confidentiality
5. Avoid harm and exploitation
6. Promote equity and inclusion
7. Maintain transparency about limitations

---

## 🙏 Acknowledgments

- **MiroFish/OASIS**: Original multi-agent framework
- **Clinical Advisors**: [Names with permission]
- **Research Partners**: [Institutions]
- **Community Input**: [Organizations]

---

## 📧 Contact

- **General Inquiries**: [email]
- **Clinical Questions**: [clinical advisor email]
- **Technical Support**: [support email]
- **Research Collaboration**: [research email]

---

## ⚠️ Final Reminder

**This tool supports mental health professionals; it does not replace them.**

Every feature, every simulation, every recommendation must be:
- Clinically validated
- Ethically sound
- Safety-focused
- Professionally supervised
- Continuously improved

**If you or someone you know is in crisis:**
- Call or text 988 (Suicide & Crisis Lifeline)
- Text HOME to 741741 (Crisis Text Line)
- Call 911 for emergencies
- Visit your nearest emergency room

---

*Building technology that serves humanity, with humility and care.*
