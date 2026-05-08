"""
Database schema for Synesthesia
Stores all simulation data: agents, mental health states, actions, events
"""

SCHEMA_SQL = """
-- Agents table: Core agent information
CREATE TABLE IF NOT EXISTS agents (
    agent_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    role TEXT NOT NULL,
    sub_role TEXT,
    gender TEXT,
    family_status TEXT,
    has_children BOOLEAN DEFAULT 0,
    num_children INTEGER DEFAULT 0,
    personality_traits TEXT, -- JSON array
    work_hours TEXT, -- JSON array of hours
    sleep_hours TEXT, -- JSON array of hours
    active_hours TEXT, -- JSON array of hours
    stressors TEXT, -- JSON array
    coping_mechanisms TEXT, -- JSON array
    therapy_access BOOLEAN DEFAULT 0,
    therapy_willingness REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mental health states: Time series of mental health metrics
CREATE TABLE IF NOT EXISTS mental_health_states (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    simulated_time TEXT, -- "Day 1, 14:00"
    anxiety REAL NOT NULL,
    depression REAL NOT NULL,
    stress REAL NOT NULL,
    wellbeing REAL NOT NULL,
    overall_distress REAL, -- Computed: (anxiety + depression + stress) / 3
    mental_health_state TEXT, -- thriving, coping, struggling, crisis
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_mental_health_agent_time 
ON mental_health_states(agent_id, timestamp);

-- Actions log: Every action taken by agents
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    simulated_time TEXT,
    action_type TEXT NOT NULL,
    action_details TEXT, -- JSON with action-specific data
    mental_health_impact TEXT, -- JSON: {"anxiety": -0.1, "stress": 0.05}
    success BOOLEAN DEFAULT 1,
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

CREATE INDEX IF NOT EXISTS idx_actions_agent_time 
ON actions(agent_id, timestamp);

CREATE INDEX IF NOT EXISTS idx_actions_type 
ON actions(action_type);

-- Social connections: Relationships between agents
CREATE TABLE IF NOT EXISTS connections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id_1 INTEGER NOT NULL,
    agent_id_2 INTEGER NOT NULL,
    connection_type TEXT NOT NULL, -- friend, family, colleague, therapist
    strength REAL DEFAULT 0.5, -- 0.0 to 1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_interaction TIMESTAMP,
    FOREIGN KEY (agent_id_1) REFERENCES agents(agent_id),
    FOREIGN KEY (agent_id_2) REFERENCES agents(agent_id),
    UNIQUE(agent_id_1, agent_id_2, connection_type)
);

CREATE INDEX IF NOT EXISTS idx_connections_agent1 
ON connections(agent_id_1);

CREATE INDEX IF NOT EXISTS idx_connections_agent2 
ON connections(agent_id_2);

-- Life events: Random events that happen to agents
CREATE TABLE IF NOT EXISTS life_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    simulated_time TEXT,
    event_type TEXT NOT NULL,
    event_details TEXT, -- JSON
    mental_health_impact TEXT, -- JSON
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

CREATE INDEX IF NOT EXISTS idx_life_events_agent_time 
ON life_events(agent_id, timestamp);

-- Interviews: Conversations with agents
CREATE TABLE IF NOT EXISTS interviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    simulated_time TEXT,
    question TEXT NOT NULL,
    response TEXT NOT NULL,
    interviewer TEXT DEFAULT 'user',
    FOREIGN KEY (agent_id) REFERENCES agents(agent_id)
);

-- Simulation metadata: Track simulation runs
CREATE TABLE IF NOT EXISTS simulations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id TEXT UNIQUE NOT NULL,
    society_description TEXT,
    total_population INTEGER,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    total_simulated_hours INTEGER,
    status TEXT DEFAULT 'running', -- running, paused, completed
    config TEXT -- JSON with full simulation config
);

-- Population statistics: Aggregated stats per time period
CREATE TABLE IF NOT EXISTS population_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    simulation_id TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    simulated_time TEXT,
    role TEXT, -- NULL for overall, or specific role
    total_agents INTEGER,
    avg_anxiety REAL,
    avg_depression REAL,
    avg_stress REAL,
    avg_wellbeing REAL,
    agents_in_crisis INTEGER,
    agents_thriving INTEGER,
    FOREIGN KEY (simulation_id) REFERENCES simulations(simulation_id)
);

CREATE INDEX IF NOT EXISTS idx_population_stats_time 
ON population_stats(simulation_id, timestamp);
"""

def get_schema():
    """Return the database schema SQL"""
    return SCHEMA_SQL
