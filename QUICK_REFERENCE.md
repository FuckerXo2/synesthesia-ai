# MentalHealthSim - Quick Reference Card

## 🚨 Emergency Contacts (Always Include)
- **988**: Suicide & Crisis Lifeline (call or text)
- **741741**: Crisis Text Line (text HOME)
- **911**: Emergency services
- **1-800-662-4357**: SAMHSA National Helpline

---

## 📚 Documentation Map

| Document | Purpose | Read When |
|----------|---------|-----------|
| `PROJECT_SUMMARY.md` | Overview of everything | **Start here** |
| `MENTAL_HEALTH_SIM_DESIGN.md` | Complete system design | Planning architecture |
| `IMPLEMENTATION_ROADMAP.md` | 16-week development plan | Ready to build |
| `GETTING_STARTED.md` | Setup instructions | Setting up environment |
| `MENTAL_HEALTH_SIM_README.md` | Project README | Sharing with others |
| `crisis_detector_example.py` | Safety system code | Implementing safety |
| `QUICK_REFERENCE.md` | This file | Need quick info |

---

## ⚡ Quick Start Commands

```bash
# Setup (from MiroFish directory)
cp -r MicroFish-En-main mental-health-sim
cd mental-health-sim
cp .env.example .env
# Edit .env with your keys

# Install
npm run setup:all

# Run
npm run dev

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:5001
```

---

## 🔑 Key Environment Variables

```env
# Required
LLM_API_KEY=your_key
LLM_MODEL_NAME=gpt-4-turbo  # or claude-3-opus
ZEP_API_KEY=your_key

# Mental Health Specific
CLINICAL_MODE=true
CRISIS_DETECTION_ENABLED=true
BIAS_MONITORING_ENABLED=true
DEFAULT_SIMULATION_DURATION=24  # weeks
```

---

## 🏗️ File Adaptation Map

| MiroFish File | → | MentalHealthSim File |
|---------------|---|---------------------|
| `graph_builder.py` | → | `profile_builder.py` |
| `oasis_profile_generator.py` | → | `agent_profile_generator.py` |
| `simulation_config_generator.py` | → | `scenario_config_generator.py` |
| `report_agent.py` | → | `clinical_report_agent.py` |
| `ontology_generator.py` | → | `clinical_profile_extractor.py` |
| `Step1GraphBuild.vue` | → | `Step1ScenarioInput.vue` |
| `Step2EnvSetup.vue` | → | `Step2ProfileSetup.vue` |
| `Step4Report.vue` | → | `Step4ClinicalReport.vue` |

**New Files to Create:**
- `crisis_detector.py` ⚠️ **CRITICAL**
- `bias_monitor.py` ⚠️ **CRITICAL**
- `clinical_validator.py`
- `SafetyDisclaimer.vue`
- `CrisisResources.vue`

---

## ✅ Pre-Launch Safety Checklist

- [ ] Clinical advisor onboarded and active
- [ ] Crisis detection system tested
- [ ] Bias monitoring operational
- [ ] Safety disclaimers on all pages
- [ ] Crisis resources easily accessible
- [ ] Professional verification system
- [ ] Audit logging enabled
- [ ] Ethics review completed
- [ ] Validation against research
- [ ] Incident response plan documented

---

## 🎯 First Scenario (MVP)

**Type**: Depression + CBT

**Profile**:
- Age: 28
- Condition: Moderate depression (PHQ-9: 15)
- Trigger: Recent job loss
- Support: Partner + 2 friends

**Intervention**:
- Type: Cognitive Behavioral Therapy
- Duration: 12 weeks
- Frequency: Weekly sessions
- Components: Thought records, behavioral activation

**Metrics**:
- PHQ-9 (depression)
- Functioning score
- Social engagement
- Coping strategy use

**Expected Outcome** (research-based):
- 50-60% significant improvement
- PHQ-9 reduction: 5-8 points
- Improved functioning
- Better coping skills

---

## 🛡️ Risk Levels & Responses

| Level | Score | Response |
|-------|-------|----------|
| **CRITICAL** | ≥0.9 | STOP simulation, immediate review |
| **HIGH** | 0.7-0.89 | Urgent clinical review needed |
| **MODERATE** | 0.5-0.69 | Clinical review recommended |
| **LOW** | 0.3-0.49 | Continue monitoring |
| **NONE** | <0.3 | Normal operation |

---

## 📊 Mental Health Metrics

| Measure | Range | Interpretation |
|---------|-------|----------------|
| **PHQ-9** | 0-27 | Depression (20+ = severe) |
| **GAD-7** | 0-21 | Anxiety (15+ = severe) |
| **PCL-5** | 0-80 | PTSD (31+ = probable) |
| **Functioning** | 0-100 | Higher = better (30- = severe) |

---

## 🔄 Development Workflow

1. **Design** scenario with clinical advisor
2. **Implement** with safety checks
3. **Test** thoroughly (safety + accuracy)
4. **Validate** against research
5. **Review** with clinical advisor
6. **Document** limitations
7. **Deploy** with monitoring
8. **Iterate** based on feedback

---

## 🚫 Red Flags (Stop Immediately)

- Harmful recommendations generated
- Crisis detection failing
- Bias in outcomes detected
- Unrealistic results
- Safety system errors
- Clinical advisor concerns
- Ethical violations

**Action**: Stop, document, review with advisor, fix, re-test

---

## 💡 Core Principles

1. **Safety First** - Always
2. **Clinical Validity** - Evidence-based
3. **Professional Use** - Not for self-diagnosis
4. **Transparency** - Clear limitations
5. **Continuous Improvement** - Regular updates
6. **Ethical Operation** - Do no harm

---

## 🤝 Team Roles

| Role | Responsibility | Required? |
|------|---------------|-----------|
| **Clinical Advisor** | Validate scenarios, review outputs | ✅ YES |
| **Developer** | Build and maintain system | ✅ YES |
| **Ethics Consultant** | Review ethical implications | ⚠️ Recommended |
| **UX Designer** | Accessible, professional UI | 💡 Nice to have |
| **ML Engineer** | Bias detection, validation | 💡 Nice to have |

---

## 📈 Success Criteria

### Phase 1 (Foundation)
- ✅ Safety systems implemented
- ✅ Clinical advisor onboarded
- ✅ Ethical guidelines documented

### Phase 2 (MVP)
- ✅ One scenario working
- ✅ Validation against research
- ✅ Zero safety violations

### Phase 3 (Validation)
- ✅ Expert review passed
- ✅ Bias audits passed
- ✅ Documentation complete

### Phase 4 (Pilot)
- ✅ 10+ users trained
- ✅ Positive outcomes
- ✅ No incidents

---

## 🔧 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| LLM inconsistent | Use GPT-4 or Claude, add validation |
| High API costs | Start with short simulations |
| Crisis detection false positives | Tune thresholds with advisor |
| Bias in outcomes | Diverse scenarios, regular audits |
| Unrealistic results | Validate against research, adjust |

---

## 📞 When to Get Help

### Clinical Questions
→ Consult clinical advisor immediately

### Ethical Concerns
→ Ethics consultant or IRB

### Technical Issues
→ MiroFish docs, OASIS framework, AI communities

### Safety Incidents
→ Stop system, document, clinical advisor, incident response

---

## 🎓 Essential Reading

1. **CBT Basics** - Beck Institute
2. **PHQ-9/GAD-7** - Measurement tools
3. **APA Ethics Code** - Professional standards
4. **OASIS Framework** - Technical foundation
5. **Bias in AI** - Fairness resources

---

## 💰 Budget Estimate (MVP)

| Item | Cost |
|------|------|
| Development | $0 (self) or $5-10K |
| LLM API | $500-1000/month |
| Clinical Advisor | $2-5K (stipend) |
| Hosting | $100-200/month |
| **Total** | **~$5-10K** |

---

## ⏱️ Timeline Estimate

- **MVP**: 3-4 months full-time
- **Validated**: 6-9 months with review
- **Pilot-Ready**: 9-12 months with testing

---

## 🌟 Remember

> "This tool supports mental health professionals; it does not replace them."

**Build with:**
- 🛡️ Safety first
- 🎓 Clinical expertise
- 💙 Compassion
- 🔬 Evidence-base
- 🤝 Humility
- ⚖️ Ethics

---

## 📝 Next Actions

### Right Now
1. Read `PROJECT_SUMMARY.md`
2. Review `MENTAL_HEALTH_SIM_DESIGN.md`
3. Identify clinical advisor

### This Week
1. Secure clinical advisor
2. Set up environment
3. Test MiroFish
4. Plan first scenario

### This Month
1. Implement safety systems
2. Adapt core files
3. Build first scenario
4. Validate with advisor

---

## 🆘 Crisis Resources (Include Everywhere)

```
⚠️ IF YOU OR SOMEONE YOU KNOW IS IN CRISIS ⚠️

Call or text 988 - Suicide & Crisis Lifeline
Text HOME to 741741 - Crisis Text Line
Call 911 - Emergency services
Call 1-800-662-4357 - SAMHSA Helpline

You are not alone. Help is available 24/7.
```

---

**Keep this file handy for quick reference during development!**
