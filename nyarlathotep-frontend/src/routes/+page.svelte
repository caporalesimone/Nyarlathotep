<script lang="ts">
  import { onMount } from 'svelte';
  import WorkstationCard from '../lib/components/WorkstationCard.svelte';
  import type { WorkstationStatus } from '../types';
  import HeaderBar from '$lib/components/HeaderBar.svelte';

  let workstations: WorkstationStatus[] = [];

  async function fetchWorkstations() {
    try {
      const response = await fetch('/workstations_status');
      const data = await response.json();
      workstations = data as WorkstationStatus[]; // Ora è un array di WorkstationStatus
    } catch (error) {
      console.error('Error fetching workstations:', error);
    }
  }

  onMount(() => {
    fetchWorkstations();
    setInterval(fetchWorkstations, 15000); // Aggiorna ogni 15 secondi
  });
</script>

<main>
  <HeaderBar version="1.0.1"/>
  <div class="container mt-4">
    <div class="row">
      {#each workstations as workstation}
        <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3 mb-4">
          <WorkstationCard workstation_data={workstation} />
        </div>
      {/each}
    </div>
  </div>
</main>
