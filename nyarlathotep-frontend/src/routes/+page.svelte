<script lang="ts">
    import { onMount } from 'svelte';
    import WorkstationCard from '../lib/components/WorkstationCard.svelte';
    import type { WorkstationStatus } from '../types';
  
    // Usa un oggetto singolo invece di un array
    let workstationStatus: WorkstationStatus | null = null;
  
    async function fetchWorkstations() {
      try {
        const response = await fetch('/workstations_status');
        const data = await response.json();
        workstationStatus = data as WorkstationStatus; // Assicurati che il JSON sia conforme all'interfaccia
      } catch (error) {
        console.error('Error fetching workstations:', error);
      }
    }
  
    onMount(() => {
      fetchWorkstations();
      setInterval(fetchWorkstations, 30000); // Aggiorna ogni 30 secondi
    });
  </script>
  
  <main class="container mt-4">
    <h1 class="mb-4">Workstation Status</h1>
    {#if workstationStatus}
      <!-- Mostra solo se workstationStatus non è nullo -->
      <WorkstationCard name={workstationStatus.WORKSTATION.details.client_name} status={workstationStatus.WORKSTATION.timed_out} />
    {:else}
      <p>Loading...</p>
    {/if}
  </main>
  