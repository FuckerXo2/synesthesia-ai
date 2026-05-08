"""
SYNESTHESIA WEB APP
Flask backend with real-time visualization
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import json
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
import threading
import time

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'synesthesia-secret-key-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global simulation state
simulations = {}

class SimulationRunner:
    def __init__(self, sim_id, config):
        self.sim_id = sim_id
        self.config = config
        self.running = False
        self.paused = False
        self.agents = {}
        self.locations = []
        self.spatial_world = None
        self.sim_time = datetime.now()
        self.conversations = []  # Track active conversations
        self.conversation_cooldown = {}  # Track conversation cooldowns
        
    def generate_society(self):
        """Generate society structure"""
        from synesthesia.world.society_orchestrator import SocietyOrchestrator
        
        llm_client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL")
        )
        
        orchestrator = SocietyOrchestrator(llm_client)
        society = orchestrator.generate_society_structure(
            self.config['society_description'],
            self.config['population']
        )
        
        return society
    
    def create_world(self, society):
        """Create spatial world"""
        from synesthesia.world.spatial_world import SpatialWorld, LocationType
        
        self.spatial_world = SpatialWorld(width=1200, height=900)
        
        # Create locations
        locations_config = society.get('locations', {})
        x, y = 50, 50
        
        # Smart location type mapping
        location_type_map = {
            # School/University
            'classrooms': LocationType.SCHOOL,
            'classroom': LocationType.SCHOOL,
            'lecture halls': LocationType.SCHOOL,
            'lecture_halls': LocationType.SCHOOL,
            'library': LocationType.SCHOOL,
            'libraries': LocationType.SCHOOL,
            'dorms': LocationType.HOME,
            'dormitories': LocationType.HOME,
            'student housing': LocationType.HOME,
            'cafeteria': LocationType.RESTAURANT,
            'cafeterias': LocationType.RESTAURANT,
            'dining hall': LocationType.RESTAURANT,
            'student center': LocationType.OTHER,
            'gym': LocationType.GYM,
            'labs': LocationType.SCHOOL,
            'laboratories': LocationType.SCHOOL,
            
            # Workplace
            'offices': LocationType.WORKPLACE,
            'office': LocationType.WORKPLACE,
            'meeting rooms': LocationType.WORKPLACE,
            'conference rooms': LocationType.WORKPLACE,
            'workspaces': LocationType.WORKPLACE,
            
            # Residential
            'homes': LocationType.HOME,
            'home': LocationType.HOME,
            'houses': LocationType.HOME,
            'apartments': LocationType.HOME,
            'residences': LocationType.HOME,
            
            # Healthcare
            'hospital': LocationType.HOSPITAL,
            'hospitals': LocationType.HOSPITAL,
            'clinic': LocationType.HOSPITAL,
            'clinics': LocationType.HOSPITAL,
            'medical center': LocationType.HOSPITAL,
            
            # Recreation
            'parks': LocationType.PARK,
            'park': LocationType.PARK,
            'recreation areas': LocationType.PARK,
            'gyms': LocationType.GYM,
            'fitness center': LocationType.GYM,
            
            # Retail/Food
            'restaurants': LocationType.RESTAURANT,
            'restaurant': LocationType.RESTAURANT,
            'cafes': LocationType.RESTAURANT,
            'cafe': LocationType.RESTAURANT,
            'stores': LocationType.STORE,
            'store': LocationType.STORE,
            'shops': LocationType.STORE,
            'shopping': LocationType.STORE,
        }
        
        for loc_name, details in locations_config.items():
            count = min(details.get('count', 1), 10)
            capacity = details.get('capacity', 50)
            
            # Map location name to type
            loc_name_lower = loc_name.lower().replace('_', ' ')
            location_type = location_type_map.get(loc_name_lower, LocationType.OTHER)
            
            for i in range(count):
                # Use the actual location name from society (not generic)
                display_name = f"{loc_name.replace('_', ' ').title()} {i+1}"
                
                loc = self.spatial_world.create_location(
                    name=display_name,
                    location_type=location_type,
                    x=x, y=y,
                    width=random.randint(60, 100),
                    height=random.randint(60, 100),
                    capacity=capacity
                )
                
                self.locations.append({
                    'id': loc.location_id,
                    'name': loc.name,
                    'type': loc.location_type.value,
                    'x': loc.x,
                    'y': loc.y,
                    'width': loc.width,
                    'height': loc.height
                })
                
                x += 120
                if x > 1000:
                    x = 50
                    y += 120
    
    def create_agents(self, society):
        """Create agent population"""
        from synesthesia.agent.agent import Agent
        from synesthesia.agent.state import MentalHealthState
        
        roles = society.get('roles', {})
        role_names = list(roles.keys()) if roles else ['worker']
        
        names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "Ethan", "Sophia", "Mason",
                 "Isabella", "William", "Mia", "James", "Charlotte", "Benjamin", "Amelia",
                 "Lucas", "Harper", "Henry", "Evelyn", "Alexander"]
        
        for i in range(self.config['population']):
            role = random.choice(role_names)
            role_info = roles.get(role, {})
            
            work_hours = role_info.get('work_hours', [9, 17])
            if isinstance(work_hours, list) and len(work_hours) == 2:
                work_hours = list(range(work_hours[0], work_hours[1]))
            else:
                work_hours = list(range(9, 17))
            
            agent = Agent(
                agent_id=i,
                name=f"{names[i % len(names)]} {i // len(names) + 1}" if i >= len(names) else names[i],
                age=random.randint(18, 65),
                role=role,
                personality_traits=["friendly", "hardworking"],
                mental_health=MentalHealthState(
                    anxiety=random.uniform(0.2, 0.6),
                    depression=random.uniform(0.1, 0.4),
                    stress=random.uniform(0.3, 0.7),
                    wellbeing=random.uniform(0.4, 0.8)
                ),
                work_hours=work_hours,
                sleep_hours=list(range(23, 24)) + list(range(0, 7))
            )
            
            self.agents[i] = agent
            
            # Add to spatial world
            x = random.uniform(100, 1100)
            y = random.uniform(100, 800)
            self.spatial_world.add_agent(i, x, y, speed=random.uniform(1.5, 2.5))
    
    def get_state(self):
        """Get current simulation state for frontend"""
        agents_data = []
        
        for agent_id, agent in self.agents.items():
            spatial_agent = self.spatial_world.get_agent(agent_id)
            
            agents_data.append({
                'id': agent_id,
                'name': agent.name,
                'age': agent.age,
                'role': agent.role,
                'x': spatial_agent.x if spatial_agent else 0,
                'y': spatial_agent.y if spatial_agent else 0,
                'mental_health': {
                    'anxiety': agent.mental_health.anxiety,
                    'depression': agent.mental_health.depression,
                    'stress': agent.mental_health.stress,
                    'wellbeing': agent.mental_health.wellbeing,
                    'category': agent.mental_health.category.value
                }
            })
        
        return {
            'agents': agents_data,
            'locations': self.locations,
            'conversations': self.conversations,  # Add conversations
            'time': self.sim_time.strftime('%Y-%m-%d %H:%M:%S'),
            'stats': self.get_stats()
        }
    
    def get_stats(self):
        """Get population statistics"""
        categories = {'thriving': 0, 'coping': 0, 'struggling': 0, 'crisis': 0}
        
        for agent in self.agents.values():
            categories[agent.mental_health.category.value] += 1
        
        return categories
    
    def inject_event(self, event_description: str):
        """Inject a custom event into the simulation"""
        # Parse event and apply effects
        event_lower = event_description.lower()
        
        # Determine event impact
        stress_change = 0.0
        anxiety_change = 0.0
        wellbeing_change = 0.0
        
        # Negative events
        if any(word in event_lower for word in ['election', 'crisis', 'layoff', 'fire', 'emergency', 'death', 'disaster']):
            stress_change = random.uniform(0.1, 0.3)
            anxiety_change = random.uniform(0.1, 0.25)
            wellbeing_change = random.uniform(-0.2, -0.1)
        
        # Policy changes
        elif any(word in event_lower for word in ['policy', 'law', 'regulation', 'mandate']):
            if any(word in event_lower for word in ['reduce', 'shorter', '4-day', 'benefit', 'raise', 'increase pay']):
                stress_change = random.uniform(-0.2, -0.1)
                wellbeing_change = random.uniform(0.1, 0.2)
            else:
                stress_change = random.uniform(0.05, 0.15)
                anxiety_change = random.uniform(0.05, 0.1)
        
        # Positive events
        elif any(word in event_lower for word in ['party', 'celebration', 'holiday', 'bonus', 'promotion', 'success']):
            stress_change = random.uniform(-0.15, -0.05)
            wellbeing_change = random.uniform(0.1, 0.25)
            anxiety_change = random.uniform(-0.1, -0.05)
        
        # Neutral/mixed events
        else:
            stress_change = random.uniform(-0.05, 0.1)
            anxiety_change = random.uniform(-0.05, 0.05)
        
        # Apply to all agents (with some randomness)
        affected_count = 0
        for agent in self.agents.values():
            # Not everyone is affected equally
            if random.random() < 0.8:  # 80% of population affected
                impact_multiplier = random.uniform(0.5, 1.5)
                
                agent.mental_health.stress = max(0.0, min(1.0, 
                    agent.mental_health.stress + (stress_change * impact_multiplier)))
                agent.mental_health.anxiety = max(0.0, min(1.0,
                    agent.mental_health.anxiety + (anxiety_change * impact_multiplier)))
                agent.mental_health.wellbeing = max(0.0, min(1.0,
                    agent.mental_health.wellbeing + (wellbeing_change * impact_multiplier)))
                
                # Update category
                agent.mental_health.update_category()
                
                # Add to agent's recent events
                agent.add_recent_event(event_description)
                
                affected_count += 1
        
        return {
            'affected_count': affected_count,
            'stress_change': stress_change,
            'anxiety_change': anxiety_change,
            'wellbeing_change': wellbeing_change
        }
    
    def update(self):
        """Update simulation one step"""
        from synesthesia.world.movement_system import MovementSystem
        
        if not hasattr(self, 'movement_system'):
            self.movement_system = MovementSystem(self.spatial_world)
        
        # Update movement
        self.movement_system.update(1.0)  # 1 second
        
        # Give new destinations to idle agents
        for agent_id, spatial_agent in self.spatial_world.agents.items():
            if not spatial_agent.is_moving and self.locations:
                target_loc_data = random.choice(self.locations)
                target_loc = self.spatial_world.get_location(target_loc_data['id'])
                if target_loc:
                    self.movement_system.move_agent_to_location(agent_id, target_loc.location_id)
        
        # Trigger conversations (10% chance per update)
        if random.random() < 0.1:
            self.trigger_random_conversation()
        
        # Update time
        self.sim_time += timedelta(seconds=60)  # 1 minute per update
    
    def trigger_random_conversation(self):
        """Trigger a conversation between nearby agents"""
        # Find pairs of nearby agents
        agent_ids = list(self.agents.keys())
        if len(agent_ids) < 2:
            return
        
        # Pick two random agents
        agent1_id = random.choice(agent_ids)
        agent2_id = random.choice([aid for aid in agent_ids if aid != agent1_id])
        
        agent1 = self.agents[agent1_id]
        agent2 = self.agents[agent2_id]
        
        spatial1 = self.spatial_world.get_agent(agent1_id)
        spatial2 = self.spatial_world.get_agent(agent2_id)
        
        if not spatial1 or not spatial2:
            return
        
        # Check if they're nearby (within 50 meters)
        dx = spatial1.x - spatial2.x
        dy = spatial1.y - spatial2.y
        distance = (dx*dx + dy*dy) ** 0.5
        
        if distance < 50:
            # Check cooldown
            pair_key = tuple(sorted([agent1_id, agent2_id]))
            last_time = self.conversation_cooldown.get(pair_key, 0)
            current_time = time.time()
            
            if current_time - last_time > 30:  # 30 second cooldown
                # Create conversation
                conversation = {
                    'id': f"conv_{int(time.time() * 1000)}",
                    'agent1': {
                        'id': agent1_id,
                        'name': agent1.name,
                        'x': spatial1.x,
                        'y': spatial1.y
                    },
                    'agent2': {
                        'id': agent2_id,
                        'name': agent2.name,
                        'x': spatial2.x,
                        'y': spatial2.y
                    },
                    'text': self.generate_conversation_text(agent1, agent2),
                    'start_time': current_time,
                    'duration': 5.0  # 5 seconds
                }
                
                self.conversations.append(conversation)
                self.conversation_cooldown[pair_key] = current_time
                
                # Clean up old conversations
                self.conversations = [c for c in self.conversations 
                                     if current_time - c['start_time'] < c['duration']]
    
    def generate_conversation_text(self, agent1, agent2):
        """Generate simple conversation text"""
        topics = [
            f"{agent1.name}: How are you feeling today?",
            f"{agent1.name}: This work is stressful...",
            f"{agent1.name}: Want to grab coffee?",
            f"{agent1.name}: Did you hear about the news?",
            f"{agent1.name}: I'm feeling overwhelmed.",
            f"{agent1.name}: How's your day going?",
        ]
        return random.choice(topics)
    
    def run_loop(self):
        """Main simulation loop"""
        self.running = True
        
        while self.running:
            if not self.paused:
                self.update()
                
                # Emit state to frontend
                state = self.get_state()
                socketio.emit('simulation_update', {
                    'sim_id': self.sim_id,
                    'state': state
                }, namespace='/')
            
            time.sleep(0.1)  # 10 FPS

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_simulation():
    """Generate new simulation"""
    data = request.json
    
    sim_id = f"sim_{int(time.time())}"
    
    config = {
        'society_description': data.get('society', 'Modern city'),
        'population': min(int(data.get('population', 100)), 200)  # Max 200 for web
    }
    
    # Create simulation
    sim = SimulationRunner(sim_id, config)
    
    try:
        # Generate society
        socketio.emit('generation_progress', {
            'sim_id': sim_id,
            'stage': 'society',
            'message': 'Generating society structure...'
        })
        
        society = sim.generate_society()
        
        # Create world
        socketio.emit('generation_progress', {
            'sim_id': sim_id,
            'stage': 'world',
            'message': 'Creating spatial world...'
        })
        
        sim.create_world(society)
        
        # Create agents
        socketio.emit('generation_progress', {
            'sim_id': sim_id,
            'stage': 'agents',
            'message': 'Creating population...'
        })
        
        sim.create_agents(society)
        
        # Store simulation
        simulations[sim_id] = sim
        
        return jsonify({
            'success': True,
            'sim_id': sim_id,
            'initial_state': sim.get_state()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/start/<sim_id>', methods=['POST'])
def start_simulation(sim_id):
    """Start simulation"""
    if sim_id not in simulations:
        return jsonify({'success': False, 'error': 'Simulation not found'}), 404
    
    sim = simulations[sim_id]
    
    # Start simulation loop in background thread
    thread = threading.Thread(target=sim.run_loop)
    thread.daemon = True
    thread.start()
    
    return jsonify({'success': True})

@app.route('/api/pause/<sim_id>', methods=['POST'])
def pause_simulation(sim_id):
    """Pause/resume simulation"""
    if sim_id not in simulations:
        return jsonify({'success': False, 'error': 'Simulation not found'}), 404
    
    sim = simulations[sim_id]
    sim.paused = not sim.paused
    
    return jsonify({'success': True, 'paused': sim.paused})

@app.route('/api/stop/<sim_id>', methods=['POST'])
def stop_simulation(sim_id):
    """Stop simulation"""
    if sim_id not in simulations:
        return jsonify({'success': False, 'error': 'Simulation not found'}), 404
    
    sim = simulations[sim_id]
    sim.running = False
    
    del simulations[sim_id]
    
    return jsonify({'success': True})

@app.route('/api/inject_event/<sim_id>', methods=['POST'])
def inject_event(sim_id):
    """Inject a custom event into the simulation"""
    if sim_id not in simulations:
        return jsonify({'success': False, 'error': 'Simulation not found'}), 404
    
    data = request.json
    event_description = data.get('event', '')
    
    if not event_description:
        return jsonify({'success': False, 'error': 'No event description provided'}), 400
    
    sim = simulations[sim_id]
    
    try:
        result = sim.inject_event(event_description)
        
        # Emit update to all clients
        socketio.emit('event_injected', {
            'sim_id': sim_id,
            'event': event_description,
            'result': result
        }, namespace='/')
        
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@app.route('/api/query/<sim_id>', methods=['POST'])
def query_oracle(sim_id):
    """Query Oracle AI about simulation"""
    if sim_id not in simulations:
        return jsonify({'success': False, 'error': 'Simulation not found'}), 404
    
    from synesthesia.llm.oracle_ai import OracleAI
    
    data = request.json
    question = data.get('question', '')
    
    if not question:
        return jsonify({'success': False, 'error': 'No question provided'}), 400
    
    sim = simulations[sim_id]
    state = sim.get_state()
    
    # Create LLM clients
    nvidia_client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )
    
    # Try to create AMD client if configured
    amd_client = None
    amd_key = os.getenv("AMD_API_KEY")
    amd_url = os.getenv("AMD_BASE_URL")
    
    if amd_key and amd_url and amd_key != "your_amd_api_key_here":
        try:
            amd_client = OpenAI(
                api_key=amd_key,
                base_url=amd_url
            )
            print("✅ AMD client initialized for Oracle AI")
        except Exception as e:
            print(f"⚠️ AMD client failed to initialize: {e}")
            amd_client = None
    
    # Create Oracle AI with AMD support
    oracle = OracleAI(nvidia_client, amd_client)
    
    try:
        result = oracle.query(question, state)
        return jsonify({
            'success': True,
            'result': result,
            'provider': result.get('_provider', 'UNKNOWN'),
            'model': result.get('_model', 'unknown')
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/insights/<sim_id>', methods=['GET'])
def get_insights(sim_id):
    """Get automatic insights"""
    if sim_id not in simulations:
        return jsonify({'success': False, 'error': 'Simulation not found'}), 404
    
    from synesthesia.llm.oracle_ai import OracleAI
    
    sim = simulations[sim_id]
    state = sim.get_state()
    
    llm_client = OpenAI(
        api_key=os.getenv("LLM_API_KEY"),
        base_url=os.getenv("LLM_BASE_URL")
    )
    oracle = OracleAI(llm_client)
    
    try:
        result = oracle.get_insights(state)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌍 SYNESTHESIA WEB APP")
    print("="*60)
    print("Starting server...")
    port = int(os.getenv("PORT", 5001))
    print(f"Open your browser to: http://localhost:{port}")
    print("="*60 + "\n")
    
    socketio.run(app, debug=False, host='0.0.0.0', port=port)
