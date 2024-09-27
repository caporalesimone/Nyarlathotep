<script lang="ts">
  import type { WorkstationStatus } from "../../types.js";
  export let workstation_data: WorkstationStatus;
  import { calculatePercentage } from "$lib/utils/utils.js";

  const progressTresholds = {
    low: 40,
    high: 80,
  };

  function progressBarThresholdClass(value: number) {
    if (value < progressTresholds.low) {
      return "low";
    } else if (value >= progressTresholds.high) {
      return "high";
    } else {
      return "medium";
    }
  }

  $: cpu_percentage = workstation_data.details.hardware.cpu_usage;
  $: ram_percentage = parseFloat(
    calculatePercentage(
      workstation_data.details.hardware.ram_used_MB,
      workstation_data.details.hardware.ram_total_MB,
    ).toFixed(1),
  );
  $: disk_percentage = parseFloat(
    calculatePercentage(
      workstation_data.details.hardware.disk_used_GB,
      workstation_data.details.hardware.disk_total_GB,
    ).toFixed(1),
  );
</script>

<div class="details-card">
  <h3>{workstation_data.details.client_name}</h3>
  <strong>Version:</strong>
  {workstation_data.details.client_sw_version}
  <br />
  <strong>Hostname:</strong>
  {workstation_data.details.hostname}
  <br />
  <strong>Network Name:</strong>
  {workstation_data.details.network_name}
  <br />
  <strong>JSON Version:</strong>
  {workstation_data.details.json_version}
  <br />
  <strong>Local Time:</strong>
  {workstation_data.details.local_time}
  <br />
  <strong>Last Update (UTC):</strong>
  {workstation_data.last_update_utc}
  <br />
  <strong>Timed Out:</strong>
  {workstation_data.timed_out ? "Yes" : "No"}
  <br />
  <strong>New Version Available:</strong>
  {workstation_data.new_version_available || "No"}

  <div class="section-title">Hardware</div>
  <strong>Serial Number:</strong>
  {workstation_data.details.hardware.serial_number}
  <br />

  <!-- CPU Usage -->
  <strong>CPU Usage:</strong>
  <div
    class="progress-bar"
    data-progress-value={progressBarThresholdClass(cpu_percentage)}
  >
    <div class="progress-fill" style="width: {cpu_percentage}%"></div>
    <span class="progress-text">
      {cpu_percentage}%
    </span>
  </div>

  <!-- RAM Usage -->
  <strong>RAM Usage:</strong>
  <div
    class="progress-bar"
    data-progress-value={progressBarThresholdClass(ram_percentage)}
  >
    <div class="progress-fill" style="width: {ram_percentage}%"></div>
    <span class="progress-text">
      {workstation_data.details.hardware.ram_used_MB} MB / {workstation_data
        .details.hardware.ram_total_MB} MB - {calculatePercentage(
        workstation_data.details.hardware.ram_used_MB,
        workstation_data.details.hardware.ram_total_MB,
      ).toFixed(1)}%
    </span>
  </div>

  <!-- Disk Usage -->
  <strong>Disk Usage:</strong>
  <div
    class="progress-bar"
    data-progress-value={progressBarThresholdClass(disk_percentage)}
  >
    <div class="progress-fill" style="width: {disk_percentage}%"></div>
    <span class="progress-text">
      {workstation_data.details.hardware.disk_used_GB} GB / {workstation_data
        .details.hardware.disk_total_GB} GB - {disk_percentage}%
    </span>
  </div>

  <div class="section-title">OS Information</div>
  <strong>OS Name:</strong>
  {workstation_data.details.os.os_name}
  <br />
  <strong>OS Platform:</strong>
  {workstation_data.details.os.os_platform}
  <br />
  <strong>Uptime:</strong>
  {workstation_data.details.os.uptime}
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
          <td>{net.ip_addresses.join(", ")}</td>
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

<style>
  .details-card {
    background-color: var(--card-background);
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    padding: 20px;
    width: 80vw;
    max-width: 600px;
    max-height: 80vh;
    overflow-y: auto;
    position: relative;
    font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    color: #333;
  }

  h3 {
    font-size: 1.8em;
    color: #007bff;
  }

  strong {
    font-weight: bold;
    color: #495057;
  }

  .section-title {
    margin-top: 20px;
    font-size: 1.3em;
    font-weight: bold;
    color: #495057;
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 5px;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }

  table,
  th,
  td {
    border: 1px solid #dee2e6;
  }

  th,
  td {
    padding: 10px;
    text-align: left;
    font-size: 0.9em;
  }

  th {
    background-color: #f8f9fa;
    color: #495057;
    font-weight: 600;
    border-bottom: 2px solid var(--primary-color);
  }

  tr:nth-child(even) {
    background-color: #f2f2f2;
  }

  .progress-bar {
    background-color: #e9ecef;
    border-radius: 4px;
    width: 100%;
    height: 18px;
    margin-bottom: 10px;
    position: relative;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    overflow: hidden; /* Nasconde qualsiasi overflow del contenuto */
  }

  .progress-fill {
    height: 100%;
    border-radius: 4px;
    width: var(--progress);
    background-color: var(--progress-color);
    transition:
      width 0.3s ease,
      background-color 0.3s ease; /* Cambia colore e larghezza con una transizione fluida */
  }

  .progress-text {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    color: black;
    font-size: 0.85em;
  }

  /* Cambia il colore della barra in base al valore di progress */
  .progress-bar[data-progress-value] .progress-fill {
    background-color: rgb(
      98,
      179,
      98
    ); /* Default verde per progress minori del 20% */
  }

  .progress-bar[data-progress-value="medium"] .progress-fill {
    background-color: rgb(232, 232, 27); /* Giallo per progress tra 20% e 80% */
  }

  .progress-bar[data-progress-value="high"] .progress-fill {
    background-color: red; /* Rosso per progress maggiori dell'80% */
  }
</style>
