<script lang="ts">
  import type { WorkstationStatus } from '../../types.js';

  export let workstation_data: WorkstationStatus;

  // Calcolo dello stato di workstation_busy
  $: workstation_busy = workstation_data.details.users.some(user => user.logged);

  // Calcola il tempo trascorso dall'ultimo aggiornamento quando offline
  $: timeSinceLastUpdate = calculateTimeSince(workstation_data.last_update_epoch);

  function calculateTimeSince(lastUpdateEpoch: number): string {
    const now = Date.now();
    const lastUpdate = new Date(lastUpdateEpoch * 1000);
    const difference = now - lastUpdate.getTime();

    const seconds = Math.floor(difference / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    const displaySeconds = seconds % 60;
    const displayMinutes = minutes % 60;
    const displayHours = hours % 24;

    return `${days}d ${displayHours}h ${displayMinutes}m ${displaySeconds}s`;
  }
</script>

<style>
  .card {
    position: relative;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Ombra per effetto 3D */
    border-radius: 8px; /* Angoli arrotondati */
    background-color: #fff; /* Sfondo bianco per la card */
  }

  .card.offline {
    opacity: 0.5; /* Grigiato per l'effetto disabilitato */
    filter: grayscale(100%); /* Ulteriore effetto grigiato */
  }

  .card-header {
    display: flex;
    align-items: center; /* Allinea verticalmente il contenuto al centro */
    margin: 0;
  }

  .card-title {
    font-weight: bold;
    color: #0562a9;
    margin: 0;
  }

  .led {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background-color: #ff0000; /* Default red */
    border: 2px solid #fff;
    margin-left: auto; /* Moves LED to right */
  }

  .led.green {
    background-color: #32cd32; /* Green */
  }

  .status {
    font-size: 0.875rem;
    margin: 0;
  }
</style>

<div class="card mb-3 {workstation_data.timed_out ? 'offline' : ''}">
  <div class="card-header">
    <h5 class="card-title">{workstation_data.details.client_name}</h5>
    <div class="led { workstation_busy == false ? 'green' : ''}"></div>
  </div>
  
  <div class="card-body">
    <p class="status">
      {#if workstation_data.timed_out}
        Last Seen: {timeSinceLastUpdate}
      {:else}
        Uptime: {workstation_data.details.os.uptime}
      {/if}

      {#if workstation_busy}
        <br />
        Logged user: <strong>{workstation_data.details.users.filter(user => user.logged).map(user => user.username).join(', ')}</strong>
      {/if}

    </p>
  </div>
</div>
