let cardState = {};

// Extract IP addresses from the json data into a single string comma separated
function extractIPAddresses(data) {
    const netInterfaces = data.net_interfaces;
    const ipAddresses = [];

    netInterfaces.forEach(interface => {
        ipAddresses.push(...interface.ip_addresses);
    });

    return ipAddresses.join(', ');
}

// Create the HTML user table from the json data
function extractUsersTable(data) {
    let users = Array.isArray(data.users) ? data.users : [];
    return  users.map(user => `
        <tr class="${user.logged ? 'logged' : ''}">
            <td>${user.username}</td>
            <td>${user.login_time}</td>
        </tr>
    `).join('');
}

function fetchStatus() {
    fetch('/status_data')
        .then(response => response.json())
        .then(data => {
            let container = document.getElementById('status-container');
            container.innerHTML = '';

            for (let client_name in data) {
                let json = data[client_name];
                let card = document.createElement('div');
                card.classList.add('card');

                // If the client is timed out, add a class that overlay disabling the card
                if (json.timed_out) {
                    card.classList.add('timed_out');
                }

                // IP Addresses
                let ipAddresses = extractIPAddresses(json.details);

                // Users table
                let userRows = extractUsersTable(json.details);

                // card content
                card.innerHTML = `
                    <h2>${client_name} 
                        ${json.new_version_available != "" ? 
                        '<span class="version-upgrade">⬆️<span class="tooltip">New agent version ' + json.new_version_available + ' available!</span></span>' : ''}
                    </h2>
                    <div class="info-group">
                        <p><strong>Hostname:</strong> ${json.details.hostname}</p>
                        <p><strong>IP:</strong> ${ipAddresses}</p>
                        <p><strong>OS:</strong> ${json.details.os.os_name || 'N/A'}</p>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-label">CPU</div>
                        <div class="progress-bar cpu-bar">
                            <div class="progress-bar-bg"></div>
                            <div class="progress-bar-fill" style="width: ${json.details.hardware.cpu_usage || 0}%"></div>
                            <div class="progress-bar-text">${json.details.hardware.cpu_usage || '0'}%</div>
                        </div>
                    </div>

                    <div class="progress-bar-container">
                        <div class="progress-bar-label">Storage</div>
                        <div class="progress-bar storage-bar">
                            <div class="progress-bar-bg"></div>
                            <div class="progress-bar-fill" style="width: ${((json.details.hardware.disk_used_GB || 0) / json.details.hardware.disk_total_GB) * 100}%"></div>
                            <div class="progress-bar-text">${json.details.hardware.disk_total_GB - (json.details.hardware.disk_used_GB || 0)} GB free of ${json.details.hardware.disk_total_GB} GB</div>
                        </div>
                    </div>

                    <div class="progress-bar-container">
                        <div class="progress-bar-label">Memory</div>
                        <div class="progress-bar memory-bar">
                            <div class="progress-bar-bg"></div>
                            <div class="progress-bar-fill" style="width: ${json.details.hardware.ram_total_MB > 0 ? ((json.details.hardware.ram_used_MB || 0) / json.details.hardware.ram_total_MB) * 100 : 0}%"></div>
                            <div class="progress-bar-text">${json.details.hardware.ram_total_MB - (json.details.hardware.ram_used_MB || 0)} MB free of ${json.details.hardware.ram_total_MB} MB</div>
                        </div>
                    </div>

                    <table class="user-table">
                        <thead>
                            <tr>
                                <th style="text-align: center;">Full Name</th>
                                <th style="text-align: center;">Login Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${userRows.length > 0 ? userRows : '<tr><td colspan="2">Nessun dato disponibile</td></tr>'}
                        </tbody>
                    </table>

                    <button class="collapsible">Show extra info</button>
                    <div class="content">
                        <pre>${JSON.stringify(json, null, 2) || 'N/A'}</pre>
                    </div>
                `;

                container.appendChild(card);

                // Recover card state
                let collapsible = card.querySelector('.collapsible');
                let content = card.querySelector('.content');

                // Unique ID for the card
                let cardId = `card_${client_name}`;

                if (cardState[cardId] && cardState[cardId].expanded) {
                    collapsible.classList.add('active');
                    content.style.display = "block";
                } else {
                    content.style.display = "none";
                }

                // Event listener for collapsible
                collapsible.addEventListener('click', function() {
                    this.classList.toggle('active');
                    if (content.style.display === "block") {
                        content.style.display = "none";
                        cardState[cardId] = { expanded: false };
                    } else {
                        content.style.display = "block";
                        cardState[cardId] = { expanded: true };
                    }
                });
            }
        })
        .catch(error => {
            console.error('Error on request:', error);
        });
}

setInterval(fetchStatus, 10000);
window.onload = fetchStatus;
