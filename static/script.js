document.addEventListener('DOMContentLoaded', () => {
    const searchBtn = document.getElementById('searchBtn');
    const searchSpinner = document.getElementById('searchSpinner');
    const searchIcon = document.getElementById('searchIcon');
    const queryInput = document.getElementById('researchQuery');
    const reportContent = document.getElementById('reportContent');
    const agentLogs = document.getElementById('agentLogs');
    const dropZone = document.getElementById('dropZone');
    const pdfInput = document.getElementById('pdfInput');
    const uploadStatus = document.getElementById('uploadStatus');

    const addLog = (message, agent = "SYSTEM") => {
        const time = new Date().toLocaleTimeString();
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.innerHTML = `
            <span class="log-time">[${time}]</span>
            <span class="log-agent">${agent}:</span>
            <span class="log-msg">${message}</span>
        `;
        agentLogs.appendChild(logEntry);
        agentLogs.scrollTop = agentLogs.scrollHeight;
    };

    searchBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        if (!query) return;

        // UI Feedback
        searchBtn.disabled = true;
        searchSpinner.style.display = 'inline-block';
        searchIcon.style.display = 'none';
        reportContent.innerHTML = '<div style="text-align: center; padding-top: 100px;"><div class="spinner" style="width: 40px; height: 40px; margin: 0 auto 20px;"></div><p>Agents are synthesizing research...</p></div>';
        
        addLog(`Initiating multi-agent orchestration for: "${query}"`, "PLANNER");

        try {
            const response = await fetch('/research', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            
            if (data.logs) {
                data.logs.forEach(log => {
                    const parts = log.split(':');
                    const agentName = parts.length > 1 ? parts[0].toUpperCase() : "AGENT";
                    const msg = parts.length > 1 ? parts.slice(1).join(':') : log;
                    addLog(msg.trim(), agentName);
                });
            }

            reportContent.innerHTML = marked.parse(data.report);
            addLog("Final report synthesized successfully.", "REPORT GEN");

        } catch (error) {
            console.error(error);
            addLog("Critical failure in research pipeline.", "ERROR");
            reportContent.innerHTML = '<p style="color: #ef4444">Research failed. Check server logs.</p>';
        } finally {
            searchBtn.disabled = false;
            searchSpinner.style.display = 'none';
            searchIcon.style.display = 'inline-block';
        }
    });

    // File Handling
    dropZone.addEventListener('click', () => pdfInput.click());
    pdfInput.addEventListener('change', (e) => handleFiles(e.target.files));

    async function handleFiles(files) {
        for (const file of files) {
            addLog(`Ingesting: ${file.name}...`, "PDF AGENT");
            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/upload-pdf', { method: 'POST', body: formData });
                const result = await response.json();
                addLog(`Vector indexing complete for ${file.name} (${result.chunks} chunks).`, "CHROMA DB");
            } catch (error) {
                addLog(`Failed to index ${file.name}`, "ERROR");
            }
        }
    }
});
