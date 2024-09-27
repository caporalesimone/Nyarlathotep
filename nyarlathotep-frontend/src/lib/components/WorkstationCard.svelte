<script lang="ts">
  import type { WorkstationStatus } from "../../types.js";
  import { calculateTimeSince } from "$lib/utils/utils";
  import WorkstationDetailsCard from "$lib/components/WorkstationDetailsCard.svelte";

  export let workstation_data: WorkstationStatus;

  let showDetails = false; // Stato per mostrare/nascondere il dettaglio

  // Calculate workstation_busy status
  $: workstation_busy = workstation_data.details.users.some(
    (user) => user.logged,
  );

  // Calculate time since last update when offline
  $: timeSinceLastUpdate = calculateTimeSince(
    workstation_data.last_update_epoch,
  );

  function toggleDetails(event: MouseEvent) {
    event.stopPropagation();
    showDetails = !showDetails;
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      showDetails = false;
    }
  }

  $: {
    if (showDetails) {
      window.addEventListener("keydown", handleKeydown);
    } else {
      window.removeEventListener("keydown", handleKeydown);
    }
  }
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="card mb-3 {workstation_data.timed_out ? 'offline' : ''}"
  on:click={toggleDetails}
>
  <div class="card-header d-flex justify-content-between align-items-center">
    <h5 class="mb-0">{workstation_data.details.client_name}</h5>
    <div class={`led ${workstation_busy == false ? "green" : ""}`}></div>
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
        Logged user:
        <strong
          >{workstation_data.details.users
            .filter((user) => user.logged)
            .map((user) => user.username)
            .join(", ")}</strong
        >
      {:else}
        <br />
        {#if workstation_data.timed_out}
          Workstation is offline
        {:else}
          Workstation is available
        {/if}
      {/if}
    </p>
  </div>
</div>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
{#if showDetails}
  <div class="overlay" on:click={() => (showDetails = false)}>
    <WorkstationDetailsCard {workstation_data} />
  </div>
{/if}

<style>
  .card {
    position: relative;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Shadow for 3D effect */
    border-radius: 8px; /* Rounded corners */
    background-color: var(--card-background);
    transition:
      transform 0.2s ease,
      box-shadow 0.2s ease,
      border 0.2s ease; /* Smooth transition for hover effect */
    cursor: pointer; /* Change cursor to pointer */
    border: 1px solid transparent; /* Default border, transparent */
  }

  .card.offline {
    opacity: 0.5; /* Grayed out for disabled effect */
    filter: grayscale(100%); /* Additional gray effect */
  }

  .card:hover {
    transform: scale(1.02); /* Slightly enlarge the card */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover */
    border: 2px solid var(--primary-color); /* Blue border on hover */
  }

  .card-header {
    display: flex;
    align-items: center; /* Center align items vertically */
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

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.5); /* Semi-transparent */
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000; /* Sovrascrive altri elementi */
  }
</style>
