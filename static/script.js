const taskInput = document.getElementById('taskInput');
const runBtn = document.getElementById('runBtn');
const workflowsDiv = document.getElementById('workflows');
const agentsBar = document.getElementById('agentsBar');
const execution = document.getElementById('execution');
const timeline = document.getElementById('timeline');
const summaryBar = document.getElementById('summaryBar');

let selectedWorkflow = '';

// load workflows and agents
Promise.all([
    fetch('/api/workflows').then(r => r.json()),
    fetch('/api/agents').then(r => r.json())
]).then(([wfData, agData]) => {
    workflowsDiv.innerHTML = wfData.workflows.map(w => `
        <div class="wf-card" data-id="${w.id}" onclick="selectWorkflow('${w.id}', this)">
            <div class="wf-name">${w.name}</div>
            <div class="wf-desc">${w.description}</div>
            <div class="wf-agents">${w.agents.join(' → ')}</div>
        </div>
    `).join('');

    agentsBar.innerHTML = agData.agents.map(a => `
        <div class="agent-chip"><span class="agent-name">${a.name}</span><span class="agent-role">${a.role}</span></div>
    `).join('');

    // select first workflow by default
    if (wfData.workflows.length > 0) {
        selectedWorkflow = wfData.workflows[0].id;
        document.querySelector('.wf-card').classList.add('selected');
    }
});

function selectWorkflow(id, el) {
    selectedWorkflow = id;
    document.querySelectorAll('.wf-card').forEach(c => c.classList.remove('selected'));
    el.classList.add('selected');
}

runBtn.addEventListener('click', async () => {
    const task = taskInput.value.trim();
    if (!task) { alert('Enter a task description'); return; }
    if (!selectedWorkflow) { alert('Select a workflow'); return; }

    runBtn.disabled = true;
    runBtn.textContent = '⏳ Agents working...';
    execution.classList.remove('hidden');
    timeline.innerHTML = '<div style="text-align:center;padding:40px;color:#666">Agents are collaborating on your task...</div>';
    summaryBar.innerHTML = '';

    try {
        const res = await fetch('/api/run', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task, workflow_id: selectedWorkflow })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail);
        renderExecution(data);
    } catch (err) {
        timeline.innerHTML = `<div style="color:#f87171;padding:20px">Error: ${err.message}</div>`;
    }

    runBtn.disabled = false;
    runBtn.textContent = '▶ Run Agents';
});

function renderExecution(data) {
    timeline.innerHTML = data.steps.map((step, i) => `
        <div class="step" style="animation-delay: ${i * 0.15}s">
            <div class="step-header" onclick="this.nextElementSibling.classList.toggle('hidden')">
                <div>
                    <span class="step-agent">${step.agent}</span>
                    <span class="step-role">${step.role}</span>
                </div>
                <div style="display:flex;gap:8px;align-items:center">
                    <span class="step-badge ${step.status === 'success' ? 'badge-success' : 'badge-error'}">${step.status}</span>
                    <span class="step-time">${step.time_seconds}s</span>
                </div>
            </div>
            <div class="step-body">${marked.parse(step.output)}</div>
        </div>
    `).join('');

    summaryBar.innerHTML = `
        <div class="stat"><div class="stat-value">${data.agent_count}</div><div class="stat-label">Agents</div></div>
        <div class="stat"><div class="stat-value">${data.total_time}s</div><div class="stat-label">Total Time</div></div>
        <div class="stat"><div class="stat-value">${data.workflow}</div><div class="stat-label">Workflow</div></div>
    `;

    execution.scrollIntoView({ behavior: 'smooth' });
}

