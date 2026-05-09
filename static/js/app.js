// Synesthesia Web App - Frontend

let socket;
let currentSimId = null;
let canvas, ctx;
let camera = { x: 0, y: 0, zoom: 1 };
let isDragging = false;
let lastMousePos = { x: 0, y: 0 };
let selectedAgent = null;
let simulationState = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    canvas = document.getElementById('simulation-canvas');
    ctx = canvas.getContext('2d');
    
    setupCanvas();
    setupSocketIO();
    
    // Setup Oracle input Enter key
    const oracleInput = document.getElementById('oracle-input');
    if (oracleInput) {
        oracleInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                askCustomQuery();
            }
        });
    }
});

function setupCanvas() {
    // Handle mouse events
    canvas.addEventListener('mousedown', handleMouseDown);
    canvas.addEventListener('mousemove', handleMouseMove);
    canvas.addEventListener('mouseup', handleMouseUp);
    canvas.addEventListener('wheel', handleWheel);
    
    // Resize canvas
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
}

function resizeCanvas() {
    const container = canvas.parentElement;
    canvas.width = container.clientWidth;
    canvas.height = container.clientHeight;
    
    if (simulationState) {
        render();
    }
}

function setupSocketIO() {
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
    });
    
    socket.on('generation_progress', (data) => {
        updateLoadingMessage(data.message);
    });
    
    socket.on('simulation_update', (data) => {
        if (data.sim_id === currentSimId) {
            simulationState = data.state;
            updateUI();
            
            // Start rendering loop if not already started
            if (!window.renderingStarted) {
                window.renderingStarted = true;
                render();
            }
        }
    });
}

function setPreset(text) {
    document.getElementById('society-input').value = text;
}

async function generateSimulation() {
    const society = document.getElementById('society-input').value || 'Modern city';
    const population = parseInt(document.getElementById('population-input').value) || 100;
    
    // Show loading screen
    showScreen('loading-screen');
    updateLoadingMessage('Generating society structure...');
    
    try {
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ society, population })
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentSimId = data.sim_id;
            simulationState = data.initial_state;
            
            // Show simulation screen
            showScreen('simulation-screen');
            
            // Start simulation
            await startSimulation();
        } else {
            alert('Error: ' + data.error);
            showScreen('setup-screen');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate simulation');
        showScreen('setup-screen');
    }
}

async function startSimulation() {
    const response = await fetch(`/api/start/${currentSimId}`, {
        method: 'POST'
    });
    
    const data = await response.json();
    if (!data.success) {
        alert('Failed to start simulation');
    }
}

async function togglePause() {
    const response = await fetch(`/api/pause/${currentSimId}`, {
        method: 'POST'
    });
    
    const data = await response.json();
    if (data.success) {
        const btn = document.getElementById('pause-btn');
        btn.textContent = data.paused ? 'RESUME' : 'PAUSE';
    }
}

async function stopSimulation() {
    if (confirm('Stop simulation and return to setup?')) {
        await fetch(`/api/stop/${currentSimId}`, {
            method: 'POST'
        });
        
        currentSimId = null;
        simulationState = null;
        showScreen('setup-screen');
    }
}

async function injectEvent() {
    const input = document.getElementById('event-input');
    const event = input.value.trim();
    
    if (!event) {
        alert('Please enter an event description');
        return;
    }
    
    if (!currentSimId) {
        alert('No simulation running');
        return;
    }
    
    try {
        const response = await fetch(`/api/inject_event/${currentSimId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ event })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Show feedback
            const feedback = document.getElementById('event-feedback');
            const result = data.result;
            
            feedback.innerHTML = `
                INJECTED | ${result.affected_count} AGENTS | 
                STRESS ${result.stress_change > 0 ? '+' : ''}${(result.stress_change * 100).toFixed(0)}% | 
                ANXIETY ${result.anxiety_change > 0 ? '+' : ''}${(result.anxiety_change * 100).toFixed(0)}%
            `;
            
            // Clear input
            input.value = '';
            
            // Clear feedback after 5 seconds
            setTimeout(() => {
                feedback.innerHTML = '';
            }, 5000);
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error injecting event:', error);
        alert('Failed to inject event');
    }
}

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
}

function updateLoadingMessage(message) {
    document.getElementById('loading-message').textContent = message;
}

function updateUI() {
    if (!simulationState) return;
    
    // Update time
    document.getElementById('sim-time').textContent = simulationState.time;
    
    // Update stats
    const stats = simulationState.stats;
    document.getElementById('stat-thriving').textContent = stats.thriving || 0;
    document.getElementById('stat-coping').textContent = stats.coping || 0;
    document.getElementById('stat-struggling').textContent = stats.struggling || 0;
    document.getElementById('stat-crisis').textContent = stats.crisis || 0;
}

function render() {
    if (!simulationState) {
        requestAnimationFrame(render);
        return;
    }
    
    // Clear canvas with gradient background
    const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height);
    gradient.addColorStop(0, '#0a0a15');
    gradient.addColorStop(1, '#0f0f1a');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Grid pattern for depth
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.02)';
    ctx.lineWidth = 1;
    const gridSize = 100;
    for (let x = 0; x < canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    for (let y = 0; y < canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    ctx.save();
    
    // Apply camera transform
    ctx.translate(-camera.x, -camera.y);
    ctx.scale(camera.zoom, camera.zoom);
    
    // Draw locations
    if (simulationState.locations) {
        simulationState.locations.forEach(loc => {
            drawLocation(loc);
        });
    }
    
    // Draw agents
    if (simulationState.agents) {
        simulationState.agents.forEach(agent => {
            drawAgent(agent);
        });
    }
    
    // Draw conversations
    if (simulationState.conversations) {
        simulationState.conversations.forEach(conv => {
            drawConversation(conv);
        });
    }
    
    ctx.restore();
    
    // Draw mini-map
    drawMiniMap();
    
    // Request next frame
    requestAnimationFrame(render);
}

function drawMiniMap() {
    if (!simulationState) return;
    
    const miniMapSize = 150;
    const miniMapX = canvas.width - miniMapSize - 20;
    const miniMapY = 20;
    
    // Mini-map background
    ctx.fillStyle = 'rgba(20, 20, 30, 0.8)';
    ctx.fillRect(miniMapX, miniMapY, miniMapSize, miniMapSize);
    
    // Mini-map border
    ctx.strokeStyle = '#667eea';
    ctx.lineWidth = 2;
    ctx.strokeRect(miniMapX, miniMapY, miniMapSize, miniMapSize);
    
    // Calculate scale
    const worldWidth = 1200;
    const worldHeight = 900;
    const scale = miniMapSize / Math.max(worldWidth, worldHeight);
    
    // Draw locations on mini-map
    if (simulationState.locations) {
        simulationState.locations.forEach(loc => {
            ctx.fillStyle = getLocationColor(loc.type);
            ctx.fillRect(
                miniMapX + loc.x * scale,
                miniMapY + loc.y * scale,
                loc.width * scale,
                loc.height * scale
            );
        });
    }
    
    // Draw agents on mini-map
    if (simulationState.agents) {
        simulationState.agents.forEach(agent => {
            ctx.fillStyle = getMentalHealthColor(agent.mental_health.category);
            ctx.fillRect(
                miniMapX + agent.x * scale - 1,
                miniMapY + agent.y * scale - 1,
                2, 2
            );
        });
    }
    
    // Draw camera viewport
    const viewWidth = canvas.width / camera.zoom;
    const viewHeight = canvas.height / camera.zoom;
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
    ctx.lineWidth = 1;
    ctx.strokeRect(
        miniMapX + camera.x * scale,
        miniMapY + camera.y * scale,
        viewWidth * scale,
        viewHeight * scale
    );
}

function drawLocation(loc) {
    // Location shadow for depth
    ctx.shadowBlur = 15;
    ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
    ctx.shadowOffsetX = 3;
    ctx.shadowOffsetY = 3;
    
    // Location background
    ctx.fillStyle = getLocationColor(loc.type);
    ctx.fillRect(loc.x, loc.y, loc.width, loc.height);
    
    // Reset shadow
    ctx.shadowBlur = 0;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
    
    // Location border with gradient
    ctx.strokeStyle = '#5a5a6a';
    ctx.lineWidth = 3;
    ctx.strokeRect(loc.x, loc.y, loc.width, loc.height);
    
    // Inner highlight
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
    ctx.lineWidth = 1;
    ctx.strokeRect(loc.x + 2, loc.y + 2, loc.width - 4, loc.height - 4);
    
    // Location name
    if (camera.zoom > 0.3) {
        ctx.fillStyle = '#ffffff';
        ctx.font = 'bold 16px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        
        // Text shadow
        ctx.shadowBlur = 5;
        ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
        
        ctx.fillText(loc.name, loc.x + loc.width / 2, loc.y + loc.height / 2);
        
        // Reset shadow
        ctx.shadowBlur = 0;
    }
    
    // Location icon/emoji
    if (camera.zoom > 0.5) {
        const icon = getLocationIcon(loc.type);
        ctx.font = '24px sans-serif';
        ctx.textAlign = 'center';
        ctx.fillText(icon, loc.x + loc.width / 2, loc.y + 20);
    }
}

function getLocationIcon(type) {
    const icons = {
        'home': '🏠',
        'workplace': '🏢',
        'school': '🏫',
        'park': '🌳',
        'restaurant': '🍽️',
        'hospital': '🏥',
        'gym': '💪',
        'store': '🛒',
        'other': '📍'
    };
    return icons[type] || icons.other;
}

function drawAgent(agent) {
    const radius = 8;  // Bigger agents (was 5)
    
    // Agent glow (for better visibility)
    ctx.shadowBlur = 10;
    ctx.shadowColor = getMentalHealthColor(agent.mental_health.category);
    
    // Agent circle
    ctx.fillStyle = getMentalHealthColor(agent.mental_health.category);
    ctx.beginPath();
    ctx.arc(agent.x, agent.y, radius, 0, Math.PI * 2);
    ctx.fill();
    
    // Reset shadow
    ctx.shadowBlur = 0;
    
    // Selection indicator
    if (selectedAgent && selectedAgent.id === agent.id) {
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(agent.x, agent.y, radius + 5, 0, Math.PI * 2);
        ctx.stroke();
    }
    
    // Agent name
    if (camera.zoom > 1.0) {
        ctx.fillStyle = '#e0e0e0';
        ctx.font = 'bold 12px sans-serif';
        ctx.textAlign = 'center';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.strokeText(agent.name, agent.x, agent.y - radius - 8);
        ctx.fillText(agent.name, agent.x, agent.y - radius - 8);
    }
}

function drawConversation(conv) {
    // Calculate midpoint between agents
    const midX = (conv.agent1.x + conv.agent2.x) / 2;
    const midY = (conv.agent1.y + conv.agent2.y) / 2;
    
    // Draw line connecting agents
    ctx.strokeStyle = '#60a5fa';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.beginPath();
    ctx.moveTo(conv.agent1.x, conv.agent1.y);
    ctx.lineTo(conv.agent2.x, conv.agent2.y);
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Draw speech bubble
    const bubbleWidth = 200;
    const bubbleHeight = 50;
    const bubbleX = midX - bubbleWidth / 2;
    const bubbleY = midY - bubbleHeight - 20;
    
    // Bubble background
    ctx.fillStyle = 'rgba(30, 30, 40, 0.95)';
    ctx.strokeStyle = '#60a5fa';
    ctx.lineWidth = 2;
    
    // Rounded rectangle
    const radius = 10;
    ctx.beginPath();
    ctx.moveTo(bubbleX + radius, bubbleY);
    ctx.lineTo(bubbleX + bubbleWidth - radius, bubbleY);
    ctx.quadraticCurveTo(bubbleX + bubbleWidth, bubbleY, bubbleX + bubbleWidth, bubbleY + radius);
    ctx.lineTo(bubbleX + bubbleWidth, bubbleY + bubbleHeight - radius);
    ctx.quadraticCurveTo(bubbleX + bubbleWidth, bubbleY + bubbleHeight, bubbleX + bubbleWidth - radius, bubbleY + bubbleHeight);
    ctx.lineTo(bubbleX + radius, bubbleY + bubbleHeight);
    ctx.quadraticCurveTo(bubbleX, bubbleY + bubbleHeight, bubbleX, bubbleY + bubbleHeight - radius);
    ctx.lineTo(bubbleX, bubbleY + radius);
    ctx.quadraticCurveTo(bubbleX, bubbleY, bubbleX + radius, bubbleY);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Bubble text
    ctx.fillStyle = '#e0e0e0';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'center';
    
    // Word wrap
    const words = conv.text.split(' ');
    let line = '';
    let y = bubbleY + 20;
    const maxWidth = bubbleWidth - 20;
    
    for (let word of words) {
        const testLine = line + word + ' ';
        const metrics = ctx.measureText(testLine);
        
        if (metrics.width > maxWidth && line !== '') {
            ctx.fillText(line, midX, y);
            line = word + ' ';
            y += 16;
        } else {
            line = testLine;
        }
    }
    ctx.fillText(line, midX, y);
    
    // 💬 icon
    ctx.font = '16px sans-serif';
    ctx.fillText('💬', midX, bubbleY - 10);
}

function getLocationColor(type) {
    const colors = {
        'home': '#8b5a3c',      // Warm brown
        'workplace': '#4a5a8a',  // Professional blue
        'school': '#9a7a4a',     // Academic tan
        'park': '#4a8a5a',       // Natural green
        'restaurant': '#aa6a4a', // Food orange-brown
        'hospital': '#c85a5a',   // Medical red
        'gym': '#5a9a6a',        // Active green
        'store': '#8a8a5a',      // Retail yellow-brown
        'other': '#6a6a6a'       // Neutral gray
    };
    return colors[type] || colors.other;
}

function getMentalHealthColor(category) {
    const colors = {
        'thriving': '#10b981',   // Vibrant green
        'coping': '#3b82f6',     // Bright blue
        'struggling': '#f59e0b', // Warning orange
        'crisis': '#ef4444'      // Alert red
    };
    return colors[category] || '#3b82f6';  // Default to blue
}

// Mouse handling
function handleMouseDown(e) {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    // Check if clicked on agent
    const worldX = (mouseX / camera.zoom) + camera.x;
    const worldY = (mouseY / camera.zoom) + camera.y;
    
    let clickedAgent = null;
    if (simulationState) {
        for (const agent of simulationState.agents) {
            const dx = agent.x - worldX;
            const dy = agent.y - worldY;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            // Bigger hit radius (20px instead of 10px) - easier to click
            if (distance < 20) {
                clickedAgent = agent;
                break;
            }
        }
    }
    
    if (clickedAgent) {
        selectAgent(clickedAgent);
    } else {
        isDragging = true;
        lastMousePos = { x: mouseX, y: mouseY };
    }
}

function handleMouseMove(e) {
    if (!isDragging) return;
    
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;
    
    const dx = mouseX - lastMousePos.x;
    const dy = mouseY - lastMousePos.y;
    
    camera.x -= dx / camera.zoom;
    camera.y -= dy / camera.zoom;
    
    lastMousePos = { x: mouseX, y: mouseY };
    
    render();
}

function handleMouseUp(e) {
    isDragging = false;
}

function handleWheel(e) {
    e.preventDefault();
    
    const zoomFactor = e.deltaY > 0 ? 0.9 : 1.1;
    camera.zoom *= zoomFactor;
    camera.zoom = Math.max(0.1, Math.min(5, camera.zoom));
    
    render();
}

function selectAgent(agent) {
    selectedAgent = agent;
    
    // Show agent panel
    const panel = document.getElementById('agent-panel');
    const infoDiv = document.getElementById('agent-info');
    
    panel.style.display = 'block';
    
    const mh = agent.mental_health;
    infoDiv.innerHTML = `
        <p><strong>${agent.name}</strong>, ${agent.age}</p>
        <p>ROLE: ${agent.role}</p>
        <p style="margin-top: 15px;"><strong>MENTAL HEALTH</strong></p>
        <p>STATE: ${mh.category.toUpperCase()}</p>
        <p>ANXIETY: ${mh.anxiety.toFixed(2)}</p>
        <p>DEPRESSION: ${mh.depression.toFixed(2)}</p>
        <p>STRESS: ${mh.stress.toFixed(2)}</p>
        <p>WELLBEING: ${mh.wellbeing.toFixed(2)}</p>
    `;
    
    render();
}

function closeAgentPanel() {
    document.getElementById('agent-panel').style.display = 'none';
    selectedAgent = null;
    render();
}

function toggleOracle() {
    const sidebar = document.getElementById('oracle-sidebar');
    sidebar.classList.toggle('active');
}

// Oracle AI Functions
async function askOracle(question) {
    if (!currentSimId) {
        alert('No simulation running');
        return;
    }
    
    // Show loading
    const responseDiv = document.getElementById('oracle-response');
    const loadingDiv = document.getElementById('oracle-loading');
    const answerDiv = document.getElementById('oracle-answer');
    
    responseDiv.style.display = 'block';
    loadingDiv.style.display = 'block';
    answerDiv.innerHTML = '';
    
    try {
        const response = await fetch(`/api/query/${currentSimId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        loadingDiv.style.display = 'none';
        
        if (data.success) {
            displayOracleResponse(data.result);
        } else {
            answerDiv.innerHTML = `<p class="error">Error: ${data.error}</p>`;
        }
    } catch (error) {
        loadingDiv.style.display = 'none';
        answerDiv.innerHTML = `<p class="error">Failed to query Oracle AI</p>`;
        console.error('Oracle error:', error);
    }
}

function askCustomQuery() {
    const input = document.getElementById('oracle-input');
    const question = input.value.trim();
    
    if (!question) {
        alert('Please enter a question');
        return;
    }
    
    askOracle(question);
    input.value = '';
}

function displayOracleResponse(result) {
    const answerDiv = document.getElementById('oracle-answer');
    
    let html = `
        <div class="oracle-answer-section">
            <h4>Answer</h4>
            <p>${result.answer}</p>
        </div>
    `;
    
    // Statistics
    if (result.statistics && Object.keys(result.statistics).length > 0) {
        html += `
            <div class="oracle-answer-section">
                <h4>Statistics</h4>
                <ul>
        `;
        for (const [key, value] of Object.entries(result.statistics)) {
            html += `<li><strong>${key}:</strong> ${value}</li>`;
        }
        html += `</ul></div>`;
    }
    
    // Insights
    if (result.insights && result.insights.length > 0) {
        html += `
            <div class="oracle-answer-section">
                <h4>Key Insights</h4>
                <ul>
        `;
        result.insights.forEach(insight => {
            html += `<li>${insight}</li>`;
        });
        html += `</ul></div>`;
    }
    
    // Recommendations
    if (result.recommendations && result.recommendations.length > 0) {
        html += `
            <div class="oracle-answer-section">
                <h4>Recommendations</h4>
                <ul>
        `;
        result.recommendations.forEach(rec => {
            html += `<li>${rec}</li>`;
        });
        html += `</ul></div>`;
    }
    
    // Agents of Interest
    if (result.agents_of_interest && result.agents_of_interest.length > 0) {
        html += `
            <div class="oracle-answer-section">
                <h4>Agents of Interest</h4>
                <ul>
        `;
        result.agents_of_interest.forEach(agent => {
            html += `<li><strong>${agent.name}:</strong> ${agent.reason}</li>`;
        });
        html += `</ul></div>`;
    }
    
    answerDiv.innerHTML = html;
}
