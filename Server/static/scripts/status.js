let cardState = {};

function fetchStatus() {
    fetch('/status_data')
        .then(response => response.json())
        .then(data => {
            let container = document.getElementById('status-container');
            container.innerHTML = '';

            for (let customName in data) {
                let item = data[customName];
                let card = document.createElement('div');
                card.classList.add('card');

                let users = Array.isArray(item.json_data.users) ? item.json_data.users : [];
                let loggedInUsers = users.filter(user => user.logged);

                let userRows = users.map(user => `
                    <tr class="${user.logged ? 'logged' : ''}">
                        <td>${user.fullname}</td>
                        <td>${user.login_time}</td>
                    </tr>
                `).join('');

                if (loggedInUsers.length === 0) {
                    userRows = userRows.replace(/class="logged"/g, '');
                }

                // Join ip addresses
                let ipAddresses = Array.from(new Set([
                    item.client_ip, 
                    ...(item.json_data.ipAddresses || [])
                ])).join(', ');

                // Unique ID for the card
                let cardId = `card_${customName}`;

                // card content
                card.innerHTML = `
                    <h2>${customName}</h2>
                    <div class="info-group">
                        <p><strong>Hostname:</strong> ${item.json_data.hostname}</p>
                        <p><strong>IP:</strong> ${ipAddresses}</p>
                        <p><strong>Last Update:</strong> ${item.last_update}</p>
                        <p><strong>OS:</strong> ${item.json_data.os || 'N/A'}</p>
                    </div>
                    <div class="progress-bar-container">
                        <div class="progress-bar-label">CPU</div>
                        <div class="progress-bar cpu-bar">
                            <div class="progress-bar-bg"></div>
                            <div class="progress-bar-fill" style="width: ${item.json_data.cpu_usage || 0}%"></div>
                            <div class="progress-bar-text">${item.json_data.cpu_usage || '0'}%</div>
                        </div>
                    </div>

                    <div class="progress-bar-container">
                        <div class="progress-bar-label">Storage</div>
                        <div class="progress-bar storage-bar">
                            <div class="progress-bar-bg"></div>
                            <div class="progress-bar-fill" style="width: ${((item.json_data.disk_used || 0) / item.json_data.disk_size) * 100}%"></div>
                            <div class="progress-bar-text">${item.json_data.disk_size - (item.json_data.disk_used || 0)} GB free of ${item.json_data.disk_size} GB</div>
                        </div>
                    </div>

                    <div class="progress-bar-container">
                        <div class="progress-bar-label">Memory</div>
                        <div class="progress-bar memory-bar">
                            <div class="progress-bar-bg"></div>
                            <div class="progress-bar-fill" style="width: ${item.json_data.total_memory > 0 ? ((item.json_data.used_memory || 0) / item.json_data.total_memory) * 100 : 0}%"></div>
                            <div class="progress-bar-text">${item.json_data.total_memory - (item.json_data.used_memory || 0)} MB free of ${item.json_data.total_memory} MB</div>
                        </div>
                    </div>

                    <table class="user-table">
                        <thead>
                            <tr>
                                <th>Full Name</th>
                                <th>Login Time</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${userRows.length > 0 ? userRows : '<tr><td colspan="2">Nessun dato disponibile</td></tr>'}
                        </tbody>
                    </table>

                    <button class="collapsible">Show extra info</button>
                    <div class="content">
                        <pre>${JSON.stringify(item.json_data, null, 2) || 'N/A'}</pre>
                    </div>
                `;

                container.appendChild(card);

                // Ripristina lo stato del card
                let collapsible = card.querySelector('.collapsible');
                let content = card.querySelector('.content');

                if (cardState[cardId] && cardState[cardId].expanded) {
                    collapsible.classList.add('active');
                    content.style.display = "block";
                } else {
                    content.style.display = "none";
                }

                // Aggiungi event listener per aggiornare lo stato al click
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

setInterval(fetchStatus, 3000);
window.onload = fetchStatus;