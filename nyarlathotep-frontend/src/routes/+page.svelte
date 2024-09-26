<script lang="ts">
  import { onMount } from 'svelte';
  
  import type { WorkstationStatus } from '../types';
  
  import '../styles/main-colors.css';

  import WorkstationCard from '../lib/components/WorkstationCard.svelte';
  import HeaderBar from '$lib/components/HeaderBar.svelte';
  import BottomBar from '$lib/components/BottomBar.svelte';

  const refreshInterval = 10000; // Refresh time of the page in milliseconds

  let resetProgressBar: boolean = false;

  let workstations: WorkstationStatus[] = [];

  async function fetchWorkstations() {
    try {
      const response = await fetch('/workstations_status');
      const data = await response.json();

      // This allows svelte to re-render the component
      workstations = [...data]; 

      // Resets the progress bar
      resetProgressBar = true;
      setTimeout(() => resetProgressBar = false, 100);

    } catch (error) {
      console.error('Error fetching workstations:', error);
    }
  }

  onMount(() => {
    fetchWorkstations();
    setInterval(fetchWorkstations, refreshInterval);
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
  <BottomBar totalTime={refreshInterval} resetProgressBar={resetProgressBar}/>
</main>
