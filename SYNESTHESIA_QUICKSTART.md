# Synesthesia - Quick Start Guide

## 🎯 Get Your First Simulation Running in 30 Minutes

This guide gets you from zero to your first mental health community simulation.

---

## 📋 Prerequisites

### Required
- **Python 3.11+** (`python --version`)
- **Node.js 18+** (`node -v`)
- **uv** package manager (`uv --version` - install from https://docs.astral.sh/uv/)
- **LLM API key** (OpenAI GPT-4 or Anthropic Claude)
- **Zep Cloud account** (free tier: https://app.getzep.com/)

### Recommended
- Mental health professional advisor (for validation)
- Basic understanding of mental health concepts
- Familiarity with command line

---

## 🚀 Installation (10 minutes)

### Step 1: Get the Code

```bash
# Navigate to your workspace
cd /path/to/your/workspace

# Copy MiroFish as starting point
cp -r MicroFish-En-main synesthesia
cd synesthesia

# Clean up
rm -rf .git
git init
```

### Step 2: Install Dependencies

```bash
# Install Node dependencies (root + frontend)
npm run setup

# Install Python dependencies (backend)
cd backend
uv sync
cd ..
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit with your favorite editor
nano .env  # or vim, code, etc.
```

Add your keys:
```env
# LLM Configuration (use GPT-4 or Claude for best results)
LLM_API_KEY=sk-your-openai-key-here
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4-turbo

# Or for Claude:
# LLM_API_KEY=sk-ant-your-anthropic-key
# LLM_BASE_URL=https://api.anthropic.com/v1
# LLM_MODEL_NAME=claude-3-opus-20240229

# Zep Cloud (for agent memory)
ZEP_API_KEY=z_your_zep_key_here

# Synesthesia-specific settings
SIMULATION_MODE=mental_health
DEFAULT_POPULATION_SIZE=1000
DEFAULT_SIMULATION_WEEKS=24
CRISIS_DETECTION_ENABLED=true
```

### Step 4: Start the System

```bash
# Start both frontend and backend
npm run dev
```

You should see:
```
[backend] Running on http://localhost:5001
[frontend] Running on http://localhost:3000
```

Open http://localhost:3000 in your browser.

---

## 🎬 Your First Simulation (20 minutes)

### Scenario: University Mental Health Crisis Response

**Context:**
- University with 20,000 students
- Recent student suicide
- Exam season in 4 weeks
- Counseling center overwhelmed (6-week wait times)
- Student government has $500K emergency budget

**Question:** What intervention prevents the most crises?

### Step 1: Create Community Profile

In the Synesthesia UI:

1. Click **"New Simulation"**
2. Select **"University Community"** template
3. Fill in details:

```
Community Name: State University
Population Size: 20,000
Agent Sample Size: 1,000 (5% representative sample)

Demographics:
- Age Range: 18-25
- 55% Female, 43% Male, 2% Non-binary
- 30% First-generation students
- 15% International students

Baseline Mental Health:
- Depression Prevalence: 18%
- Anxiety Prevalence: 22%
- Crisis Risk: 3%
- Help-Seeking Rate: 35%

Social Network:
- Average Connections: 12
- Network Density: 0.15 (typical for universities)
- Isolated Students: 8%

Current Resources:
- Counselors: 10 (1 per 2,000 students)
- Wait Time: 6 weeks
- Crisis Hotline: Yes
- Peer Support: No
- Stigma Level: Medium-High
```

4. Click **"Generate Community Graph"**

Wait 2-3 minutes while Synesthesia:
- Extracts entities and relationships
- Builds knowledge graph
- Validates structure

### Step 2: Define Crisis Event

1. Click **"Add Crisis Event"**
2. Select **"Student Suicide"**
3. Configure:

```
Event Type: Student Suicide
Timing: Week 0 (simulation start)
Directly Affected: 50 (close friends, roommates)
Indirectly Affected: 500 (same dorm, classes)
Community-Wide Impact: High (news coverage, social media)

Expected Effects:
- Increased crisis risk (copycat concern)
- Increased anxiety (safety concerns)
- Increased help-seeking (or decreased due to stigma)
- Social network disruption
```

### Step 3: Design Interventions to Test

Click **"Add Interventions"** and configure:

#### Intervention A: No Additional Action (Control)
```
Name: Baseline (No Intervention)
Components: Existing resources only
Cost: $0
```

#### Intervention B: Hire More Counselors
```
Name: Expand Counseling Capacity
Components:
  - Hire 5 additional counselors
  - Reduce wait time to 2 weeks
Cost: $400,000
Expected Mechanism: Increase access to professional help
```

#### Intervention C: Peer Support Network
```
Name: Peer Support Program
Components:
  - Train 100 peer supporters (8-week program)
  - Create support groups (10-15 students each)
  - Weekly check-ins
Cost: $50,000
Expected Mechanism: 
  - Reduce stigma through peer modeling
  - Increase help-seeking through normalization
  - Create support cascades
  - Reduce isolation
```

#### Intervention D: RA Mental Health Training
```
Name: Resident Advisor Training
Components:
  - Train all 200 RAs in mental health first aid
  - Crisis intervention protocols
  - Referral pathways
Cost: $75,000
Expected Mechanism:
  - Early detection
  - Immediate support
  - Effective referrals
```

#### Intervention E: Combined Approach
```
Name: Comprehensive Response
Components:
  - Peer support program ($50K)
  - RA training ($75K)
  - 2 additional counselors ($160K)
Cost: $285,000
Expected Mechanism: Multi-level intervention with synergies
```

### Step 4: Configure Simulation Parameters

```
Simulation Duration: 24 weeks (6 months post-crisis)
Number of Runs: 500 (for statistical significance)
Time Step: 1 day
Agent Sample: 1,000 (5% of population)

Metrics to Track:
- Crisis rate (hospitalizations, attempts)
- Help-seeking rate
- Social isolation levels
- Stigma levels
- Recovery rates
- Resource utilization
```

### Step 5: Run Simulation

1. Click **"Run Simulation"**
2. Watch the progress:
   - Population generation (2 min)
   - Baseline period (3 min)
   - Crisis event injection (1 min)
   - Intervention simulations (10 min per scenario)
   - Analysis and reporting (5 min)

**Total time: ~30-40 minutes for 500 runs**

You'll see real-time updates:
```
Run 1/500: Scenario A (Baseline)
  Week 4: Crisis rate 4.2%, Help-seeking 28%
  Week 12: Crisis rate 4.8%, Help-seeking 31%
  Week 24: Crisis rate 4.5%, Help-seeking 33%

Run 1/500: Scenario C (Peer Support)
  Week 4: Crisis rate 3.8%, Help-seeking 35%
  Week 12: Crisis rate 2.9%, Help-seeking 48%
  Week 24: Crisis rate 2.7%, Help-seeking 52%
```

### Step 6: Review Results

After simulation completes, you'll see:

```
═══════════════════════════════════════════════════════
SYNESTHESIA SIMULATION REPORT
University Mental Health Crisis Response
═══════════════════════════════════════════════════════

SCENARIO A: Baseline (No Intervention)
├─ Crisis Rate: 4.5% (±0.3%)
├─ Help-Seeking: 33% (±2%)
├─ Social Isolation: +12% (±3%)
├─ Recovery Rate: 38% (±4%)
├─ Cost: $0
└─ Lives at Risk: ~900 students

SCENARIO B: Expand Counseling
├─ Crisis Rate: 3.4% (±0.3%)  [24% reduction ↓]
├─ Help-Seeking: 45% (±3%)    [36% increase ↑]
├─ Social Isolation: +8% (±2%)
├─ Recovery Rate: 51% (±4%)   [34% increase ↑]
├─ Cost: $400,000
└─ Lives at Risk: ~680 students (220 fewer)

SCENARIO C: Peer Support Network
├─ Crisis Rate: 2.8% (±0.4%)  [38% reduction ↓↓]
├─ Help-Seeking: 52% (±4%)    [58% increase ↑↑]
├─ Social Isolation: -2% (±3%) [DECREASED ↑↑]
├─ Recovery Rate: 56% (±5%)   [47% increase ↑↑]
├─ Cost: $50,000
└─ Lives at Risk: ~560 students (340 fewer)

SCENARIO D: RA Training
├─ Crisis Rate: 3.6% (±0.3%)  [20% reduction ↓]
├─ Help-Seeking: 41% (±3%)    [24% increase ↑]
├─ Social Isolation: +9% (±2%)
├─ Recovery Rate: 47% (±4%)   [24% increase ↑]
├─ Cost: $75,000
└─ Lives at Risk: ~720 students (180 fewer)

SCENARIO E: Combined Approach
├─ Crisis Rate: 2.1% (±0.3%)  [53% reduction ↓↓↓]
├─ Help-Seeking: 61% (±4%)    [85% increase ↑↑↑]
├─ Social Isolation: -5% (±3%) [DECREASED ↑↑]
├─ Recovery Rate: 64% (±5%)   [68% increase ↑↑↑]
├─ Cost: $285,000
└─ Lives at Risk: ~420 students (480 fewer)

═══════════════════════════════════════════════════════
ROI ANALYSIS
═══════════════════════════════════════════════════════

Value of Statistical Life: $10M
Cost per Crisis: $50K (hospitalization, lost productivity)
Value per Recovery: $5K (wellbeing, productivity)

SCENARIO B: Expand Counseling
  Lives Saved: 11 (220 × 0.05 mortality rate)
  Crises Prevented: 220
  Recoveries Added: 260
  Value Created: $11M + $11M + $1.3M = $23.3M
  ROI: ($23.3M - $400K) / $400K = 57x

SCENARIO C: Peer Support Network ⭐ BEST ROI
  Lives Saved: 17 (340 × 0.05)
  Crises Prevented: 340
  Recoveries Added: 360
  Value Created: $17M + $17M + $1.8M = $35.8M
  ROI: ($35.8M - $50K) / $50K = 716x ⭐⭐⭐

SCENARIO D: RA Training
  Lives Saved: 9 (180 × 0.05)
  Crises Prevented: 180
  Recoveries Added: 180
  Value Created: $9M + $9M + $900K = $18.9M
  ROI: ($18.9M - $75K) / $75K = 251x

SCENARIO E: Combined ⭐ BEST OUTCOMES
  Lives Saved: 24 (480 × 0.05)
  Crises Prevented: 480
  Recoveries Added: 520
  Value Created: $24M + $24M + $2.6M = $50.6M
  ROI: ($50.6M - $285K) / $285K = 177x

═══════════════════════════════════════════════════════
KEY INSIGHTS
═══════════════════════════════════════════════════════

1. PEER SUPPORT CREATES CASCADES
   - One peer supporter helps 3.4 people on average
   - Network effects multiply impact
   - Reduces isolation (unique benefit)
   - 716x ROI (highest)

2. COMBINED APPROACH HAS SYNERGIES
   - Peer support + RA training = 53% crisis reduction
   - More than sum of parts (20% + 38% ≠ 53%)
   - Addresses multiple pathways
   - Still under budget ($285K < $500K)

3. PROFESSIONAL SERVICES ALONE INSUFFICIENT
   - More counselors help but don't address stigma
   - 60% still won't seek help even with no wait time
   - Network effects matter more than capacity

4. LEVERAGE POINTS IDENTIFIED
   - RAs are highly connected (avg 45 connections)
   - Training them creates 45x multiplier
   - Peer supporters bridge isolated students
   - Social media influencers spread hope or stigma

═══════════════════════════════════════════════════════
RECOMMENDATION
═══════════════════════════════════════════════════════

IMPLEMENT: Scenario E (Combined Approach)

Rationale:
✓ 53% crisis reduction (480 lives at lower risk)
✓ 24 lives saved (statistical)
✓ 85% increase in help-seeking
✓ Reduces isolation (not just treats crisis)
✓ Under budget ($285K of $500K available)
✓ Sustainable (peer support continues)
✓ Addresses multiple pathways

Use remaining $215K for:
- Sustaining peer support program ($50K/year)
- Marketing and awareness ($50K)
- Evaluation and adjustment ($50K)
- Emergency reserve ($65K)

═══════════════════════════════════════════════════════
NEXT STEPS
═══════════════════════════════════════════════════════

1. Present findings to decision-makers
2. Engage student input on implementation
3. Pilot peer support with 50 students (8 weeks)
4. Train RAs before fall semester
5. Monitor outcomes and compare to simulation
6. Adjust based on real-world data
7. Re-run simulation with updated parameters

═══════════════════════════════════════════════════════
```

### Step 7: Deep Dive Analysis

Click on **"Scenario C: Peer Support"** to explore:

**Network Visualization:**
- See how support spreads through the network
- Identify highly connected individuals (leverage points)
- Watch isolation decrease over time

**Agent Trajectories:**
- Follow individual agents through the simulation
- See decision points (seek help or not?)
- Understand what influenced their choices

**Cascade Analysis:**
- One peer supporter helps 3.4 people
- Those 3.4 help 1.8 others each
- Total cascade: 1 → 3.4 → 6.1 → 8.9 people helped

**Critical Moments:**
- Week 2: First peer support session → stigma drops 5%
- Week 4: Highly connected student seeks help → 12 friends follow
- Week 8: Support group forms → isolation drops 15% in that cluster
- Week 12: Social media post about therapy → help-seeking spikes 20%

**What-If Analysis:**
Click **"Modify and Re-run"** to test:
- What if we trained 200 peer supporters instead of 100?
- What if we targeted training at highly connected students?
- What if we combined with social media campaign?

---

## 🎓 Understanding the Results

### What the Numbers Mean

**Crisis Rate: 2.8%**
- Out of 20,000 students, ~560 experience crisis (hospitalization, attempt)
- Down from 900 in baseline (38% reduction)
- Translates to ~17 lives saved (using 5% mortality rate)

**Help-Seeking: 52%**
- Of students experiencing distress, 52% now seek help
- Up from 33% baseline (58% increase)
- Means 1,040 more students get support

**Social Isolation: -2%**
- Isolation actually decreased (rare!)
- Peer support creates connections
- 400 fewer isolated students

**Recovery Rate: 56%**
- Of those who sought help, 56% show significant improvement
- Up from 38% baseline
- Better outcomes due to peer support + professional help

### Why Peer Support Wins

**Network Effects:**
- One trained peer supporter has 12 connections on average
- Helps 3.4 people directly
- Those people help 1.8 others each
- Cascade multiplier: 8.9x

**Stigma Reduction:**
- Peers seeking help normalizes it
- "If my friend can do it, so can I"
- Reduces shame and fear

**Access:**
- Peers are always available (not 6-week wait)
- Informal, low-barrier
- Culturally matched

**Sustainability:**
- Peer supporters continue helping after program ends
- Creates culture change
- Self-reinforcing

### Why Combined Approach Is Best

**Synergies:**
- Peer support reduces stigma → more seek professional help
- RA training catches early → refers to peer support or counseling
- Professional help improves outcomes → peers learn from success
- Multiple pathways → reaches more people

**Addresses Barriers:**
- Stigma: Peer support
- Access: More counselors
- Early detection: RA training
- Isolation: Peer networks

---

## 🔍 Next Steps

### Validate the Simulation

1. **Compare to Literature**
   - Look up peer support intervention studies
   - Check if 38% crisis reduction is realistic
   - Synesthesia should match published findings

2. **Expert Review**
   - Show results to mental health professionals
   - Get feedback on assumptions
   - Adjust model if needed

3. **Community Input**
   - Share with students
   - Do they find it realistic?
   - What did we miss?

### Refine and Re-run

1. **Adjust Parameters**
   - Change stigma levels
   - Modify network structure
   - Test different demographics

2. **Test Variations**
   - What if peer training was 12 weeks instead of 8?
   - What if we targeted specific populations (first-gen, international)?
   - What if we added social media component?

3. **Sensitivity Analysis**
   - Which assumptions matter most?
   - Where is uncertainty highest?
   - What's the range of possible outcomes?

### Implement and Monitor

1. **Pilot Program**
   - Start with 50 peer supporters
   - Run for 8 weeks
   - Collect data

2. **Compare to Simulation**
   - Did help-seeking increase as predicted?
   - Did isolation decrease?
   - Were there unexpected effects?

3. **Iterate**
   - Update simulation with real data
   - Re-run with new parameters
   - Improve predictions

---

## 🛠️ Troubleshooting

### Simulation Running Slow
- Reduce agent sample size (1000 → 500)
- Reduce number of runs (500 → 100)
- Use faster LLM (GPT-4-turbo instead of GPT-4)

### Results Seem Unrealistic
- Check baseline parameters (do they match your community?)
- Validate against research literature
- Consult with mental health professionals
- Adjust model assumptions

### High API Costs
- Start with fewer runs (100 instead of 500)
- Use smaller agent sample (500 instead of 1000)
- Cache LLM responses when possible
- Consider using local LLM for development

### Errors During Simulation
- Check logs: `backend/logs/simulation.log`
- Verify API keys are correct
- Ensure Zep Cloud is accessible
- Check network connection

---

## 📚 Learn More

### Documentation
- [Full Design Document](SYNESTHESIA_DESIGN.md)
- [Implementation Roadmap](SYNESTHESIA_ROADMAP.md)
- [Use Cases](SYNESTHESIA_CASES.md)
- [API Reference](docs/api.md)

### Concepts
- **Network Effects**: How influence spreads
- **Social Contagion**: Mental health as collective phenomenon
- **Leverage Points**: High-impact intervention targets
- **ROI Analysis**: Value created per dollar spent

### Research
- Peer support intervention studies
- Social network analysis in mental health
- Stigma reduction strategies
- Crisis prevention best practices

---

## 🎯 Your First Simulation Checklist

- [ ] Prerequisites installed (Python, Node, uv)
- [ ] API keys configured (LLM, Zep)
- [ ] System running (frontend + backend)
- [ ] Community profile created
- [ ] Crisis event defined
- [ ] Interventions configured
- [ ] Simulation run (500 iterations)
- [ ] Results reviewed
- [ ] Insights extracted
- [ ] Next steps planned

---

## 💡 Pro Tips

1. **Start Simple**
   - One community type
   - One crisis event
   - 3-4 interventions
   - 100 runs for testing

2. **Validate Early**
   - Compare to research immediately
   - Get expert feedback
   - Adjust before scaling

3. **Focus on ROI**
   - Not just effectiveness
   - Cost per outcome matters
   - Sustainability matters

4. **Look for Cascades**
   - Network effects are where the magic is
   - One intervention can trigger many outcomes
   - Leverage points have outsized impact

5. **Iterate**
   - First simulation won't be perfect
   - Learn from each run
   - Improve continuously

---

**Congratulations! You've run your first Synesthesia simulation.**

**Now you can rehearse the future of mental health - and choose the timeline where your community thrives.**

---

## 🆘 Need Help?

- **Documentation**: Check other guides in this repo
- **Issues**: Open a GitHub issue
- **Community**: Join our Discord (link in README)
- **Email**: support@synesthesia.ai

---

**Next: Try a different scenario or dive into the [Full Design Document](SYNESTHESIA_DESIGN.md)**
