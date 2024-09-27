<script lang="ts">
  import type { WorkstationStatus } from '../../types.js';
  export let workstation_data: WorkstationStatus;

  // Funzione per calcolare la percentuale di utilizzo
  const calculatePercentage = (used: number, total: number): number => {
    return (used / total) * 100;
  };
</script>

<style>
  .details-card {
    background-color: var(--card-background);
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(100, 5, 5, 0.2);
    padding: 20px;
    width: 80vw;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    position: relative;
  }

  .progress-bar {
    background-color: lightgray;
    border-radius: 4px;
    width: 100%;
    height: 20px;
    margin-bottom: 10px;
    position: relative;
  }

  .progress-fill {
    background-color: green;
    height: 100%;
    border-radius: 4px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  table, th, td {
    border: 1px solid black;
  }

  th, td {
    padding: 8px;
    text-align: left;
  }

  .section-title {
    margin-top: 20px;
    font-size: 1.2em;
    font-weight: bold;
  }
</style>

<div class="details-card">
  <h3>{workstation_data.details.client_name}</h3>
  <strong>Version:</strong> {workstation_data.details.client_sw_version}
  <br />
  <strong>Hostname:</strong> {workstation_data.details.hostname}
  <br />
  <strong>Network Name:</strong> {workstation_data.details.network_name}
  <br />
  <strong>JSON Version:</strong> {workstation_data.details.json_version}
  <br />
  <strong>Local Time:</strong> {workstation_data.details.local_time}
  <br />
  <strong>Last Update (UTC):</strong> {workstation_data.last_update_utc}
  <br />
  <strong>Timed Out:</strong> {workstation_data.timed_out ? 'Yes' : 'No'}
  <br />
  <strong>New Version Available:</strong> {workstation_data.new_version_available || 'No'}

  <div class="section-title">Hardware</div>
  <strong>Serial Number:</strong> {workstation_data.details.hardware.serial_number}
  <br />
  
  <!-- CPU Usage -->
  <strong>CPU Usage:</strong>
  <div class="progress-bar">
    <div class="progress-fill" style="width: {workstation_data.details.hardware.cpu_usage}%"></div>
  </div>
  
  <!-- RAM Usage -->
  <strong>RAM Usage:</strong>
  <div class="progress-bar">
    <div class="progress-fill" style="width: {calculatePercentage(workstation_data.details.hardware.ram_used_MB, workstation_data.details.hardware.ram_total_MB)}%"></div>
  </div>
  <small>{workstation_data.details.hardware.ram_used_MB} MB / {workstation_data.details.hardware.ram_total_MB} MB</small>
  
  <!-- Disk Usage -->
  <strong>Disk Usage:</strong>
  <div class="progress-bar">
    <div class="progress-fill" style="width: {calculatePercentage(workstation_data.details.hardware.disk_used_GB, workstation_data.details.hardware.disk_total_GB)}%"></div>
  </div>
  <small>{workstation_data.details.hardware.disk_used_GB} GB / {workstation_data.details.hardware.disk_total_GB} GB</small>

  <div class="section-title">OS Information</div>
  <strong>OS Name:</strong> {workstation_data.details.os.os_name}
  <br />
  <strong>OS Platform:</strong> {workstation_data.details.os.os_platform}
  <br />
  <strong>Uptime:</strong> {workstation_data.details.os.uptime}
  <br />

  <div class="section-title">Network Interfaces</div>
  <table>
    <thead>
      <tr>
        <th>Interface</th>
        <th>IP Addresses</th>
        <th>MAC Address</th>
      </tr>
    </thead>
    <tbody>
      {#each workstation_data.details.net_interfaces as net}
        <tr>
          <td>{net.interface}</td>
          <td>{net.ip_addresses.join(', ')}</td>
          <td>{net.mac}</td>
        </tr>
      {/each}
    </tbody>
  </table>

  <div class="section-title">Logged Users</div>
  <table>
    <thead>
      <tr>
        <th>Username</th>
        <th>Status</th>
        <th>Login Time</th>
        <th>Idle Time</th>
      </tr>
    </thead>
    <tbody>
      {#each workstation_data.details.users as user}
        <tr>
          <td>{user.username}</td>
          <td>{user.status}</td>
          <td>{user.login_time}</td>
          <td>{user.idle_time}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
