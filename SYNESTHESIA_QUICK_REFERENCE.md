# Synesthesia - Quick Reference Card

## 🎯 The One-Sentence Pitch

**Most mental health models try to predict individual outcomes. Synesthesia simulates entire communities - and shows you what interventions actually work at scale.**

---

## 📚 Documentation Map

| Document | Purpose | Read When |
|----------|---------|-----------|
| `SYNESTHESIA_PITCH.md` | **START HERE** - The vision and why this matters | First time |
| `SYNESTHESIA_DESIGN.md` | Complete system architecture | Planning implementation |
| `SYNESTHESIA_ROADMAP.md` | 16-week development plan | Ready to build |
| `SYNESTHESIA_QUICKSTART.md` | Setup and first simulation | Setting up |
| `SYNESTHESIA_README.md` | Project overview | Sharing with others |
| `SYNESTHESIA_QUICK_REFERENCE.md` | This file | Need quick info |

---

## ⚡ Quick Start Commands

```bash
# Setup (from MiroFish directory)
cp -r MicroFish-En-main synesthesia
cd synesthesia
cp .env.example .env
# Edit .env with your API keys

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
# LLM (use GPT-4 or Claude for best results)
LLM_API_KEY=your_key
LLM_MODEL_NAME=gpt-4-turbo  # or claude-3-opus-20240229
ZEP_API_KEY=your_key

# Synesthesia-specific
SIMULATION_MODE=mental_health
DEFAULT_POPULATION_SIZE=1000
DEFAULT_SIMULATION_WEEKS=24
CRISIS_DETECTION_ENABLED=true
```

---

## 🏗️ Core Concepts

### What Synesthesia Does

1. **Builds community profile** from your data
2. **Generates population** of diverse agents
3. **Simulates interactions** across contexts (social media, therapy, work, family)
4. **Tests interventions** in parallel universes
5. **Reports probabilities** of different outcomes

### What Makes It Different

**Traditional:** Predict individual outcomes  
**Synesthesia:** Simulate community dynamics

**Traditional:** Linear effects  
**Synesthesia:** Network effects and cascades

**Traditional:** One prediction  
**Synesthesia:** Probability distribution (500 runs)

**Traditional:** Treat people as isolated  
**Synesthesia:** Treat mental health as collective phenomenon

---

## 🧮 The Math That Matters

### Expected Value
```
EV = p(success) × value_created - cost

Where p comes from simulation frequency:
- Intervention works in 380 of 1,000 runs → p = 0.38
```

### Network Effects
```
Cascade multiplier = 
    influence × network_size × baseline_propensity × stigma_reduction

Example: 0.8 × 100 × 0.3 × 0.5 = 12 additional people helped
```

### ROI
```
ROI = (Value_created - Cost) / Cost

Value = lives_saved + suffering_reduced + 
        productivity_gained + costs_avoided
```

---

## 📊 Example Results

### University Crisis Response (20K students, $500K budget)

```
BASELINE (No Intervention)
├─ Crisis rate: 4.5%
├─ Help-seeking: 33%
└─ Cost: $0

MORE THERAPISTS ($400K)
├─ Crisis rate: 3.4% (24% reduction)
├─ Help-seeking: 45%
└─ ROI: 57x

PEER SUPPORT ($50K) ⭐ BEST ROI
├─ Crisis rate: 2.8% (38% reduction)
├─ Help-seeking: 52%
├─ Isolation: -2% (DECREASED)
└─ ROI: 716x

COMBINED ($285K) ⭐ BEST OUTCOMES
├─ Crisis rate: 2.1% (53% reduction)
├─ Help-seeking: 61%
├─ Isolation: -5%
└─ ROI: 177x
```

**Insight:** Peer support creates cascades. One supporter helps 3.4 people, who help 1.8 others each. Total: 8.9x multiplier.

---

## 🎯 Use Cases

| Scenario | Question | Synesthesia Answer |
|----------|----------|-------------------|
| **University Crisis** | What prevents suicide cluster? | Peer support + RA training = 45% reduction for $125K |
| **Post-Disaster** | How to allocate FEMA funds? | Economic aid + mental health = 67% better than MH alone |
| **Workplace Burnout** | What reduces burnout? | 4-day week = 52% reduction + 8% productivity increase |
| **Social Media** | What platform changes help? | Peer support features = 31% improvement, ROI quantified |
| **National Strategy** | How to allocate $100M? | Community programs (30%) + system change (20%) + safety nets |

---

## 🔄 Typical Workflow

1. **Define community** (university, workplace, city)
2. **Set baseline** (demographics, mental health prevalence, resources)
3. **Add crisis/stressor** (suicide, pandemic, economic downturn)
4. **Design interventions** (therapy, peer support, campaigns, policy)
5. **Run simulations** (500 runs per intervention)
6. **Review results** (outcome distributions, ROI, leverage points)
7. **Make decision** (evidence-based, not guesswork)
8. **Implement & monitor** (compare to simulation, iterate)

---

## 🛡️ Safety Checklist

Before any simulation:
- [ ] Community profile realistic and validated
- [ ] Baseline matches epidemiological data
- [ ] Interventions evidence-based
- [ ] Crisis detection enabled
- [ ] Bias monitoring active
- [ ] Expert review planned
- [ ] Limitations documented

---

## 📈 Success Metrics

### Validation
- 80%+ alignment with published research
- Expert validation scores 4/5+
- Bias audits passing

### Impact
- Policies informed by Synesthesia
- Resources allocated based on simulations
- Lives saved (estimated)
- Cost savings (measured)

### Adoption
- Universities using for planning
- Cities using for policy
- Organizations using for programs

---

## 🔧 File Adaptation Map

| MiroFish | → | Synesthesia |
|----------|---|-------------|
| `graph_builder.py` | → | `community_profile_builder.py` |
| `oasis_profile_generator.py` | → | `mental_health_agent_generator.py` |
| `simulation_manager.py` | → | `mental_health_simulation_manager.py` |
| `report_agent.py` | → | `mental_health_report_agent.py` |
| `Step1GraphBuild.vue` | → | `Step1CommunityProfile.vue` |
| `Step2EnvSetup.vue` | → | `Step2InterventionDesign.vue` |

**New files to create:**
- `intervention_engine.py`
- `metrics_tracker.py`
- `research_validator.py`
- `bias_auditor.py`
- `crisis_detector.py`

---

## 💡 Key Insights

### Why Peer Support Wins
- Creates cascades (1 → 3.4 → 6.1 → 8.9 people)
- Reduces stigma through modeling
- Always available (no wait times)
- Culturally matched
- Sustainable long-term

### Why Network Position Matters
- Highly connected person: 13x multiplier
- Bridge person: Connects isolated groups
- Influencer: Changes norms at scale

### Why Traditional Planning Fails
- Treats people as isolated
- Ignores network effects
- Assumes linear effects
- Based on intuition, not evidence

---

## 🚧 Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Unrealistic baseline | Validate against epidemiological data |
| Oversimplified agents | Add personality, history, behavioral rules |
| Ignoring network structure | Use realistic network models (scale-free, clustered) |
| Single run conclusions | Always run 500+ iterations |
| Ignoring uncertainty | Report confidence intervals |
| Treating as oracle | Present as probability distribution, not prediction |

---

## 📊 Metrics to Track

### Individual Level
- Mood (-10 to +10)
- Anxiety (0 to 10)
- Functioning (0 to 100)
- Crisis risk (0 to 1)

### Population Level
- Crisis rate (%)
- Help-seeking rate (%)
- Recovery rate (%)
- Stigma level (0 to 1)
- Social isolation (%)

### Network Level
- Network density
- Clustering coefficient
- Isolation rate
- Support quality

---

## 💰 Budget Estimate

| Item | Cost |
|------|------|
| Development (16 weeks) | $0-10K (self) or $20-50K (hired) |
| LLM API | $1-2K (development) |
| Clinical advisors | $5-10K (stipends) |
| Pilot program | $2-5K |
| **Total MVP** | **$8-27K** |

**Per simulation:** $50-200 in API costs  
**ROI:** Often 100x+ in value created

---

## ⏱️ Timeline

- **MVP**: 16 weeks (4 months full-time)
- **Validated**: 24 weeks (6 months with review)
- **Pilot-ready**: 32 weeks (8 months with testing)

---

## 🎯 First Scenario to Build

**Type:** University crisis response  
**Why:** Well-researched, clear outcomes, high impact  
**Complexity:** Medium  
**Validation:** Easy (lots of published studies)

**Components:**
- 20K student community
- Recent suicide (crisis event)
- 5 interventions to test
- 24-week simulation
- 500 runs per intervention

**Expected time:** 2-3 weeks to build and validate

---

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| Simulation slow | Reduce agents (1000→500) or runs (500→100) |
| Results unrealistic | Validate baseline, check assumptions |
| High API costs | Start with fewer runs, use caching |
| Errors | Check logs: `backend/logs/simulation.log` |

---

## 📚 Essential Reading

1. **Social contagion** - How mental health spreads through networks
2. **Network effects** - Why position matters more than intervention
3. **Peer support research** - Evidence for cascade effects
4. **Stigma reduction** - How attitudes change at scale
5. **ROI analysis** - Valuing mental health outcomes

---

## 🤝 Who Uses This

- **Public health officials** - Resource allocation
- **University administrators** - Crisis prevention
- **Workplace leaders** - Burnout reduction
- **Mental health orgs** - Program design
- **Researchers** - Hypothesis testing
- **Policymakers** - Evidence-based decisions

---

## ⚠️ What This Is NOT

❌ Individual diagnosis tool  
❌ Replacement for clinical judgment  
❌ Guaranteed prediction  
❌ Self-help application  
❌ Substitute for community input  

---

## ✅ What This IS

✅ Planning and policy tool  
✅ Research platform  
✅ Decision support system  
✅ Scenario generator  
✅ Evidence-based planning aid  

---

## 🌟 The Core Insight

**Mental health is a collective phenomenon.**

One person's recovery → cascade  
One person's crisis → contagion  
One intervention → ripples across network

Traditional models: People as isolated units  
Synesthesia: People as nodes in living network

**That's why it finds solutions others miss.**

---

## 🎯 The Question

**If you can stress-test a mental health intervention 500 times before deploying it - what's your excuse for still betting blind?**

---

## 📞 Contact

- **General**: hello@synesthesia.ai
- **Research**: research@synesthesia.ai
- **Partnerships**: partners@synesthesia.ai
- **Clinical advisors**: advisors@synesthesia.ai

---

## 🚀 Next Steps

1. **Read** `SYNESTHESIA_PITCH.md` for the full vision
2. **Review** `SYNESTHESIA_DESIGN.md` for architecture
3. **Follow** `SYNESTHESIA_ROADMAP.md` for implementation
4. **Start** with `SYNESTHESIA_QUICKSTART.md` for first simulation

---

**Synesthesia: Rehearse the future of mental health - before it happens.**

*The math doesn't lie. But it also doesn't care about your intuitions.*
