# 🔮 ORACLE AI - Natural Language Query System

## Overview

The Oracle AI is a natural language interface that lets you ask questions about your simulation and get intelligent insights powered by LLM analysis.

## What Can You Ask?

The Oracle AI can analyze the entire simulation state and answer questions like:

### Population Analysis
- "What's happening with mental health right now?"
- "How are mental health percentages changing?"
- "What percentage of the population is thriving vs struggling?"
- "What's the average stress level across all agents?"

### Risk Assessment
- "Who is most at risk right now?"
- "Which agents are in crisis?"
- "Show me the top 5 most stressed agents"
- "Who needs immediate intervention?"

### Trend Analysis
- "What are the main mental health trends?"
- "Is mental health getting better or worse?"
- "Why is stress increasing?"
- "What patterns do you see in the data?"

### Role-Based Analysis
- "Which roles are most stressed?"
- "How do teachers compare to students in mental health?"
- "What role has the highest crisis rate?"
- "Which jobs are most mentally demanding?"

### Interventions
- "What interventions would help?"
- "How can we improve mental health in this population?"
- "What support systems are needed?"
- "What should we prioritize?"

## How It Works

### 1. Data Collection
The Oracle AI receives the complete simulation state including:
- All agent data (mental health metrics, roles, locations)
- Population statistics (category distribution)
- Time and context information

### 2. LLM Analysis
The Oracle uses the Qwen 3.5 122B model to:
- Understand your natural language question
- Analyze the simulation data
- Identify patterns and trends
- Generate insights and recommendations

### 3. Structured Response
The Oracle returns:
- **Answer**: Direct response to your question
- **Statistics**: Supporting numbers and percentages
- **Insights**: Key patterns and observations
- **Recommendations**: Actionable suggestions
- **Agents of Interest**: Specific agents relevant to the query

## Using the Oracle AI

### Quick Query Buttons
Click pre-built query buttons for common questions:
- ⚠️ **Most at Risk**: Find agents in danger
- 📊 **Trends**: Analyze mental health patterns
- 💼 **Role Analysis**: Compare stress by role
- 💡 **Interventions**: Get recommendations

### Custom Queries
Type your own question in the input box and press Enter or click "Ask"

### Example Queries

```
"Who is most stressed right now?"
→ Returns top stressed agents with specific metrics

"What's the mental health breakdown?"
→ Shows percentage distribution across categories

"Why are students struggling?"
→ Analyzes student-specific stressors and patterns

"What interventions would help teachers?"
→ Provides role-specific recommendations

"Show me agents in crisis"
→ Lists all crisis-level agents with details

"How does anxiety compare to depression?"
→ Compares different mental health metrics

"What time of day has the worst mental health?"
→ Analyzes temporal patterns (if data available)
```

## Technical Details

### Backend Implementation
- **File**: `synesthesia/llm/oracle_ai.py`
- **Class**: `OracleAI`
- **Model**: `qwen/qwen3.5-122b-a10b` (Qwen 3.5 122B)
- **Temperature**: 0.3 (lower for factual responses)
- **Response Format**: JSON with structured fields

### API Endpoints

#### POST `/api/query/<sim_id>`
Query the Oracle with a custom question
```json
Request:
{
  "question": "Who is most at risk?"
}

Response:
{
  "success": true,
  "result": {
    "answer": "...",
    "statistics": {...},
    "insights": [...],
    "recommendations": [...],
    "agents_of_interest": [...]
  }
}
```

#### GET `/api/insights/<sim_id>`
Get automatic insights without a specific question
```json
Response:
{
  "success": true,
  "result": {
    "answer": "Key insights about population mental health...",
    ...
  }
}
```

### Context Preparation
The Oracle receives rich context including:
- Population size and distribution
- Mental health category percentages
- Average metrics (anxiety, depression, stress, wellbeing)
- Agents grouped by role with statistics
- Details about agents in crisis
- Top struggling agents sorted by stress

### Response Structure
```python
{
  "answer": str,              # Direct answer to question
  "statistics": dict,         # Key-value pairs of stats
  "insights": list[str],      # Pattern observations
  "recommendations": list[str], # Actionable suggestions
  "agents_of_interest": [     # Relevant agents
    {
      "name": str,
      "reason": str
    }
  ]
}
```

## Performance

- **Query Time**: 2-5 seconds (depends on LLM API)
- **Context Size**: ~1-2KB per 100 agents
- **Rate Limits**: Handled by NVIDIA Build API (unlimited for now)

## Future Enhancements

### Planned Features
- [ ] Historical trend analysis (compare current vs past states)
- [ ] Predictive analytics ("who will be at risk in 1 hour?")
- [ ] Conversation memory (follow-up questions)
- [ ] Export insights as reports
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Custom alert thresholds
- [ ] Integration with intervention system

### Advanced Queries (Future)
- "Compare mental health now vs 2 hours ago"
- "Predict who will enter crisis in the next hour"
- "What caused the spike in stress at 3pm?"
- "Show me the mental health trajectory of Emma"
- "Which relationships are most supportive?"

## Tips for Best Results

1. **Be Specific**: "Who are the top 3 most stressed teachers?" is better than "Who's stressed?"

2. **Ask for Numbers**: "What percentage..." or "How many..." gets quantitative answers

3. **Request Explanations**: "Why is..." or "What caused..." gets deeper analysis

4. **Combine Questions**: "Who is at risk and what interventions would help them?"

5. **Use Context**: "Which students in crisis need immediate support?"

## Troubleshooting

### Oracle Not Responding
- Check that simulation is running
- Verify LLM API key is set in `.env`
- Check browser console for errors

### Slow Responses
- Normal for first query (cold start)
- Subsequent queries should be faster
- Large populations (>200) may take longer

### Generic Answers
- Make questions more specific
- Include role names or categories
- Ask for specific metrics or agents

## Example Session

```
User: "What's happening with mental health?"
Oracle: "Currently 45% thriving, 30% coping, 20% struggling, 5% crisis.
         Average stress is elevated at 0.65. Teachers show highest stress."

User: "Why are teachers so stressed?"
Oracle: "Teachers have average stress of 0.78 vs population 0.65.
         Key factors: high workload, long hours, student demands.
         3 teachers currently in crisis state."

User: "Who are those 3 teachers?"
Oracle: "1. Sarah Johnson - stress 0.92, anxiety 0.88
         2. Michael Chen - stress 0.89, depression 0.71
         3. Emily Davis - stress 0.87, wellbeing 0.23"

User: "What interventions would help?"
Oracle: "Recommendations:
         1. Reduce teacher workload by 20%
         2. Add mental health support staff
         3. Implement stress management programs
         4. Create teacher peer support groups"
```

## Integration with Simulation

The Oracle AI is fully integrated with the real-time simulation:
- Queries reflect **current** simulation state
- Data updates every frame (10 FPS)
- Can query at any point during simulation
- Results are based on live agent data

## Privacy & Ethics

- Oracle analyzes **simulated** agents, not real people
- All data is synthetic and generated by the system
- No real personal information is processed
- Use insights responsibly and ethically

---

**Built for AMD Hackathon 2024**
**Powered by NVIDIA Build API (Qwen 3.5 122B)**
