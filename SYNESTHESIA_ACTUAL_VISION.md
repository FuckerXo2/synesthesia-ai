# Synesthesia - The Actual Vision

## 🌍 What You're Actually Building

**A living, breathing simulated world where thousands of AI agents live their lives - and you watch their mental health dynamics unfold in real-time.**

Think:
- **The Sims** (agents living daily lives)
- **Westworld** (complex AI with real personalities)
- **SimCity** (God's-eye view of populations)
- **Black Mirror** (tracking mental health at scale)

You're not testing interventions. You're **observing a living society** and tracking mental health like it's a weather system.

---

## 🎮 The Core Experience

### You Are God

You create a world:
- 10,000 agents living their lives
- Schools, workplaces, homes, parks, social media
- Morning, afternoon, evening, night cycles
- Seasons (winter depression, summer vitality)
- Weather (rainy days affect mood)

### Agents Live Naturally

Each agent:
- Wakes up, goes to work/school
- Has relationships (friends, family, romantic)
- Experiences stress, joy, loneliness, connection
- Posts on social media
- Goes to therapy (or doesn't)
- Has mental health that fluctuates
- Lives a full simulated life

### You Watch and Track

Dashboard shows:
- **Population mental health** (depression rate: 18%, anxiety: 22%)
- **Geographic hotspots** (school district A: 25% depression, district B: 12%)
- **Demographic breakdowns** (teens: 30% anxiety, adults: 15%)
- **Temporal patterns** (Monday blues, Friday highs, winter depression)
- **Social contagion** (watch depression spread through friend networks)
- **Crisis alerts** (agent #4521 at high risk)

### You Can Interact

- **Talk to any agent**: "Hey Sarah, how are you feeling today?"
- **Ask the Oracle AI**: "What's the depression rate in the downtown area?"
- **Zoom into lives**: Watch agent #2847's day unfold
- **See relationships**: Who supports whom, who's isolated
- **Track individuals**: Follow one person's mental health journey over months

---

## 🏗️ The Architecture

### The World

```
Synesthesia World
├── Geography
│   ├── Residential areas (homes, apartments)
│   ├── Schools (elementary, high school, university)
│   ├── Workplaces (offices, retail, factories)
│   ├── Social spaces (parks, cafes, gyms)
│   └── Healthcare (therapy offices, hospitals)
│
├── Time System
│   ├── Daily cycle (morning, afternoon, evening, night)
│   ├── Weekly cycle (weekdays, weekends)
│   ├── Seasonal cycle (spring, summer, fall, winter)
│   └── Weather (sunny, rainy, cloudy, snowy)
│
└── Social Infrastructure
    ├── Social media platform
    ├── Messaging system
    ├── Community events
    └── Support systems
```

### The Agents

```python
class Agent:
    # Identity
    agent_id: str
    name: str
    age: int
    occupation: str
    location: Location
    
    # Mental Health (fluctuates daily)
    mood: float  # -10 to +10
    anxiety: float  # 0 to 10
    depression_level: float  # 0 to 10
    stress: float  # 0 to 10
    loneliness: float  # 0 to 10
    life_satisfaction: float  # 0 to 10
    
    # Personality (stable)
    personality_traits: {
        openness: float,
        conscientiousness: float,
        extraversion: float,
        agreeableness: float,
        neuroticism: float
    }
    
    # Life Context
    relationships: List[Relationship]
    daily_routine: Schedule
    stressors: List[Stressor]
    support_system: List[Agent]
    
    # Memory
    recent_experiences: List[Experience]
    long_term_memory: Memory
    
    # Behavior
    def live_day(self):
        """Agent lives through one day"""
        self.wake_up()
        self.morning_routine()
        self.go_to_work_or_school()
        self.lunch_break()
        self.afternoon_activities()
        self.evening_social()
        self.night_routine()
        self.sleep()
    
    def interact_with(self, other_agent):
        """Natural interaction with another agent"""
        # Could be supportive, neutral, or stressful
        pass
    
    def post_on_social_media(self):
        """Share thoughts/feelings online"""
        pass
    
    def seek_help_if_needed(self):
        """Decide whether to reach out for support"""
        pass
```

### Daily Life Simulation

```python
class DaySimulation:
    def __init__(self, world, agents):
        self.world = world
        self.agents = agents
        self.time = Time(hour=6, day=1, season="spring")
    
    def simulate_day(self):
        """Simulate one full day"""
        
        # Morning (6am - 12pm)
        for hour in range(6, 12):
            self.time.hour = hour
            self.simulate_hour()
        
        # Afternoon (12pm - 6pm)
        for hour in range(12, 18):
            self.time.hour = hour
            self.simulate_hour()
        
        # Evening (6pm - 10pm)
        for hour in range(18, 22):
            self.time.hour = hour
            self.simulate_hour()
        
        # Night (10pm - 6am)
        for hour in range(22, 24):
            self.time.hour = hour
            self.simulate_hour()
    
    def simulate_hour(self):
        """Simulate one hour of life"""
        
        # Update environment
        weather = self.world.get_weather()
        
        # Each agent lives their hour
        for agent in self.agents:
            # What should they be doing this hour?
            activity = agent.schedule.get_activity(self.time)
            
            # Do the activity
            if activity == "work":
                agent.work()
                agent.stress += random.uniform(0, 2)
            
            elif activity == "school":
                agent.attend_class()
                agent.stress += random.uniform(0, 1.5)
            
            elif activity == "social":
                friends = agent.get_available_friends()
                if friends:
                    agent.hang_out_with(random.choice(friends))
                    agent.loneliness -= 1
                    agent.mood += 1
                else:
                    agent.loneliness += 0.5
            
            elif activity == "sleep":
                agent.sleep()
                agent.stress *= 0.8  # Sleep reduces stress
            
            # Environmental effects
            if weather == "rainy":
                agent.mood -= 0.2
            elif weather == "sunny":
                agent.mood += 0.1
            
            # Seasonal effects
            if self.time.season == "winter":
                agent.depression_level += 0.1  # SAD
            
            # Random life events
            if random.random() < 0.01:  # 1% chance
                event = self.world.generate_life_event()
                agent.experience_event(event)
            
            # Social media
            if random.random() < 0.3:  # 30% chance per hour
                agent.check_social_media()
            
            # Update mental health
            agent.update_mental_health()
```

### The Oracle AI

```python
class OracleAI:
    """
    The super AI that knows everything about the world
    You can ask it anything
    """
    
    def __init__(self, world, agents):
        self.world = world
        self.agents = agents
    
    def query(self, question: str) -> str:
        """
        Answer any question about the world
        
        Examples:
        - "What's the depression rate in school district A?"
        - "Who is the loneliest person right now?"
        - "Show me agents at high crisis risk"
        - "What's the average mood on rainy days vs sunny days?"
        - "Which neighborhoods have the best mental health?"
        """
        
        # Parse question with LLM
        intent = self.parse_question(question)
        
        # Query the world data
        if intent.type == "population_stat":
            return self.get_population_stat(intent.metric, intent.filter)
        
        elif intent.type == "individual_query":
            return self.get_individual_info(intent.agent_id)
        
        elif intent.type == "pattern_analysis":
            return self.analyze_pattern(intent.pattern_type)
        
        elif intent.type == "comparison":
            return self.compare(intent.group_a, intent.group_b, intent.metric)
    
    def get_population_stat(self, metric, filter):
        """Get population-level statistics"""
        
        filtered_agents = self.filter_agents(filter)
        
        if metric == "depression_rate":
            depressed = sum(1 for a in filtered_agents if a.depression_level > 7)
            return f"{depressed / len(filtered_agents) * 100:.1f}%"
        
        elif metric == "average_mood":
            avg = sum(a.mood for a in filtered_agents) / len(filtered_agents)
            return f"{avg:.2f} / 10"
        
        # ... etc
```

---

## 🎮 The User Experience

### Main Dashboard

```
╔════════════════════════════════════════════════════════════╗
║  SYNESTHESIA - Day 47, Spring, 2:34 PM, Sunny            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  🌍 WORLD OVERVIEW                                         ║
║  ├─ Population: 10,000 agents                             ║
║  ├─ Time: Tuesday, 2:34 PM                                ║
║  ├─ Weather: Sunny, 72°F                                  ║
║  └─ Season: Spring (Day 47/90)                            ║
║                                                            ║
║  📊 MENTAL HEALTH SNAPSHOT                                 ║
║  ├─ Depression Rate: 18.2% (↓ 0.3% from yesterday)       ║
║  ├─ Anxiety Rate: 22.1% (↑ 0.5%)                         ║
║  ├─ Average Mood: 6.2/10 (↑ 0.4)                         ║
║  ├─ Crisis Risk: 127 agents (1.3%)                       ║
║  └─ Loneliness: 15.4% (↓ 0.2%)                           ║
║                                                            ║
║  🗺️  GEOGRAPHIC HOTSPOTS                                   ║
║  ├─ 🔴 Downtown: 28% depression (high stress)             ║
║  ├─ 🟡 Suburbs: 15% depression (moderate)                 ║
║  └─ 🟢 University: 12% depression (good support)          ║
║                                                            ║
║  ⚠️  ALERTS                                                ║
║  ├─ Agent #4521 (Sarah, 19) - Crisis risk: HIGH          ║
║  ├─ Agent #8834 (Mike, 34) - Isolation: 14 days          ║
║  └─ School District A - Depression spike: +5% this week   ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

[View Map] [Talk to Agent] [Ask Oracle] [Time Controls]
```

### Map View

Interactive map showing:
- **Agents as dots** (color = mental health)
  - 🟢 Green = healthy (mood > 7)
  - 🟡 Yellow = struggling (mood 4-7)
  - 🔴 Red = crisis (mood < 4)
- **Buildings** (homes, schools, workplaces)
- **Movement** (agents moving around)
- **Connections** (lines between friends)
- **Hotspots** (areas with high depression)

Click any agent → see their info  
Click any building → see who's inside  
Zoom in/out to see different scales

### Agent Detail View

```
╔════════════════════════════════════════════════════════════╗
║  AGENT #4521 - Sarah Chen                                 ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  👤 PROFILE                                                ║
║  ├─ Age: 19                                               ║
║  ├─ Occupation: University Student (Psychology major)     ║
║  ├─ Location: University Dorm, Room 304                   ║
║  └─ Personality: Introverted, Anxious, Empathetic         ║
║                                                            ║
║  🧠 MENTAL HEALTH (Current)                                ║
║  ├─ Mood: 3.2/10 (Very Low) 🔴                           ║
║  ├─ Depression: 8.1/10 (Severe) 🔴                       ║
║  ├─ Anxiety: 7.8/10 (High) 🔴                            ║
║  ├─ Stress: 9.2/10 (Extreme) 🔴                          ║
║  ├─ Loneliness: 8.5/10 (High) 🔴                         ║
║  └─ Crisis Risk: 85% ⚠️ HIGH ALERT                        ║
║                                                            ║
║  📈 TREND (Past 7 Days)                                    ║
║  Mood:       ▁▂▂▃▃▂▁ (declining)                         ║
║  Depression: ▃▄▅▆▇▇█ (worsening)                         ║
║                                                            ║
║  👥 SOCIAL NETWORK                                         ║
║  ├─ Close friends: 2 (both busy this week)               ║
║  ├─ Family: 0 nearby (parents 500 miles away)            ║
║  ├─ Last meaningful interaction: 3 days ago               ║
║  └─ Social media: Active but performative                 ║
║                                                            ║
║  📅 TODAY'S ACTIVITIES                                     ║
║  ├─ 8:00 AM - Missed class (stayed in bed)               ║
║  ├─ 11:00 AM - Scrolled social media (felt worse)        ║
║  ├─ 2:34 PM - Currently: Alone in dorm room              ║
║  └─ Upcoming: Assignment due tonight (not started)        ║
║                                                            ║
║  💭 RECENT THOUGHTS                                        ║
║  ├─ "I can't keep up with everyone else"                 ║
║  ├─ "Maybe I'm not cut out for this"                     ║
║  └─ "Nobody would notice if I disappeared"               ║
║                                                            ║
║  🎯 STRESSORS                                              ║
║  ├─ Academic pressure (3 exams this week)                 ║
║  ├─ Financial stress (part-time job not enough)          ║
║  ├─ Social isolation (friends made new friend group)     ║
║  └─ Imposter syndrome (feels like she doesn't belong)    ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

[💬 Talk to Sarah] [👁️ Watch Her Day] [📊 Full History]
```

### Talk to Agent

```
╔════════════════════════════════════════════════════════════╗
║  💬 Conversation with Sarah Chen                          ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  You: Hey Sarah, how are you feeling today?               ║
║                                                            ║
║  Sarah: *looks up from her laptop, surprised*             ║
║  "Oh... I'm... I'm fine, I guess. Just tired. Lots of    ║
║  work, you know?"                                         ║
║  *forces a small smile but her eyes look exhausted*       ║
║                                                            ║
║  [Her mood: 3.2/10, but she's hiding it]                 ║
║                                                            ║
║  You: _________________________________                    ║
║                                                            ║
║  [Suggested responses:]                                    ║
║  • "You don't seem fine. What's really going on?"        ║
║  • "When's the last time you talked to someone?"         ║
║  • "Have you thought about reaching out for help?"       ║
║  • [Custom response]                                      ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
```

### Oracle AI Query

```
╔════════════════════════════════════════════════════════════╗
║  🔮 ORACLE AI                                              ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  You: What's the depression rate in school district A?    ║
║                                                            ║
║  Oracle: Analyzing school district A...                   ║
║                                                            ║
║  📊 SCHOOL DISTRICT A - MENTAL HEALTH REPORT              ║
║                                                            ║
║  Population: 1,247 students (ages 14-18)                  ║
║                                                            ║
║  Depression Rate: 25.3% (316 students)                    ║
║  ├─ Mild: 12.1% (151 students)                           ║
║  ├─ Moderate: 9.8% (122 students)                        ║
║  └─ Severe: 3.4% (43 students) ⚠️                        ║
║                                                            ║
║  Comparison to city average: +7.1% (significantly higher) ║
║                                                            ║
║  Trend: ↗️ Increasing (up 3.2% from last month)          ║
║                                                            ║
║  Key Factors:                                              ║
║  ├─ High academic pressure (AP exam season)               ║
║  ├─ Recent bullying incidents (3 reported this week)      ║
║  ├─ Limited counselor availability (1 per 400 students)   ║
║  └─ Social media toxicity (Instagram drama spreading)     ║
║                                                            ║
║  At-Risk Students: 43 (3.4%)                              ║
║  ├─ Agent #7821 (Emma, 16) - Crisis risk: 92%           ║
║  ├─ Agent #3344 (Jake, 17) - Crisis risk: 87%           ║
║  └─ [View full list]                                      ║
║                                                            ║
║  Recommendation: Immediate intervention needed            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

Ask another question: _________________________________
```

---

## 🎯 What Makes This Incredible

### 1. **It's Alive**
Not a static simulation. Agents live, grow, change. You can watch for days/weeks/months.

### 2. **Emergent Behavior**
You don't program depression spreading. It emerges from:
- Social isolation
- Stress accumulation
- Lack of support
- Environmental factors
- Random life events

### 3. **God's-Eye View**
See patterns humans can't:
- "Depression clusters around this school"
- "Rainy Mondays = 15% mood drop"
- "This friend group is a protective factor"
- "Social media use correlates with anxiety"

### 4. **Individual Stories**
Zoom from macro (city-wide trends) to micro (Sarah's struggle) seamlessly.

### 5. **Interactive**
Not just watching. You can:
- Talk to agents
- Ask Oracle anything
- Follow individuals
- See relationships
- Track over time

---

## 🏗️ Technical Implementation

### Core Loop

```python
def run_synesthesia():
    # Create world
    world = World(size=10000)
    agents = generate_agents(10000)
    oracle = OracleAI(world, agents)
    
    # Main simulation loop
    while True:
        # Advance time
        world.time.advance(minutes=15)  # 15-minute increments
        
        # Each agent lives their 15 minutes
        for agent in agents:
            agent.live_time_slice(world.time)
        
        # Update world state
        world.update()
        
        # Check for user interactions
        if user.wants_to_talk():
            agent = user.select_agent()
            conversation = agent.chat_with_god(user.message)
            display(conversation)
        
        if user.asks_oracle():
            answer = oracle.query(user.question)
            display(answer)
        
        # Update dashboard
        dashboard.update(world, agents)
        
        # Sleep to real-time or fast-forward
        time.sleep(world.time_scale)
```

### Agent Decision Making

```python
class Agent:
    def live_time_slice(self, current_time):
        """Live 15 minutes of life"""
        
        # What should I be doing right now?
        activity = self.schedule.get_activity(current_time)
        
        # Generate LLM prompt
        prompt = f"""
        You are {self.name}, a {self.age}-year-old {self.occupation}.
        
        Current state:
        - Mood: {self.mood}/10
        - Stress: {self.stress}/10
        - Location: {self.location}
        - Time: {current_time}
        - Weather: {world.weather}
        
        You're supposed to be: {activity}
        
        Recent experiences:
        {self.recent_experiences}
        
        What do you do in the next 15 minutes?
        Consider your mental state and make a realistic decision.
        """
        
        # Get LLM response
        action = llm.generate(prompt)
        
        # Execute action
        self.execute_action(action)
        
        # Update mental health based on action
        self.update_mental_health(action)
```

---

## 🎮 Hackathon Demo

### The Experience

**[Start]**
"Welcome to Synesthesia. You're about to enter a living world of 10,000 AI agents."

**[World Generation - 30 seconds]**
- Watch agents spawn
- See city build itself
- Agents move to homes, schools, workplaces

**[Fast-forward through first week]**
- Watch time pass (day/night cycles)
- See agents living their lives
- Mental health dashboard updating

**[Pause on Day 7]**
"After one week, patterns are emerging..."

**[Show Dashboard]**
- Depression rate: 18%
- Anxiety hotspot: Downtown area
- Crisis alert: 3 agents at high risk

**[Zoom into Agent]**
"Let's check on Sarah..."
- Show her declining mood graph
- Show her isolation
- Show her recent thoughts

**[Talk to Sarah]**
"Hey Sarah, how are you?"
- Watch LLM-powered conversation
- See her struggle to open up
- Realistic, emotional response

**[Ask Oracle]**
"Oracle, what's causing the depression spike in downtown?"
- Oracle analyzes data
- Shows: High rent stress + long commutes + isolation
- Suggests: Community spaces needed

**[Fast-forward another week]**
- Watch Sarah's trajectory
- See if she reaches out for help
- See if friends notice

**[End]**
"This is Synesthesia. A living world where mental health emerges naturally - and you can watch, learn, and understand."

---

## 🚀 4-Week Build Plan

### Week 1: Core Simulation
- Adapt MiroFish agent system
- Add time system (day/night, seasons)
- Add locations (homes, schools, workplaces)
- Agents move around and interact

### Week 2: Mental Health System
- Add mental health states to agents
- Implement mood fluctuations
- Add stressors and life events
- Track population statistics

### Week 3: UI & Visualization
- Build dashboard
- Add map view with moving agents
- Agent detail pages
- Oracle AI query interface

### Week 4: Polish & Demo
- Add "talk to agent" feature
- Smooth animations
- Demo scenario
- Practice pitch

---

## 💡 This Is What You Wanted

Not intervention testing.  
Not clinical validation.  
Not policy planning.

**A living, breathing world where you're God watching mental health dynamics unfold naturally.**

**The Sims meets Black Mirror meets SimCity.**

**Now THAT'S a hackathon winner.** 🏆
