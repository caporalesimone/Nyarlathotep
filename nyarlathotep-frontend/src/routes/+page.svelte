<script lang="ts">
  import { onMount } from 'svelte';
  
  import type { WorkstationStatus } from '../types';
  
  import '../styles/main-colors.css';
  import { FRONTEND_VERSION } from '../version';
  import { apiUrl } from '$lib/config';

  import WorkstationCard from '$lib/components/WorkstationCard.svelte';
  import HeaderBar from '$lib/components/HeaderBar.svelte';
  import BottomBar from '$lib/components/BottomBar.svelte';

  const refreshInterval = 5 * 1000; // Refresh time of the page in milliseconds

  let resetProgressBar: boolean = false;
  let workstations: WorkstationStatus[] = [];
  let expandedProjects: Record<string, boolean> = {};
  let backendVersion: string = "loading...";

  // Group workstations by project_name
  $: workstationsByProject = (() => {
    const grouped: Record<string, WorkstationStatus[]> = {};
    
    // Group workstations by project_name (any project_name is valid)
    workstations.forEach(workstation => {
      const projectName = workstation.details.project_name || "Unassigned";
      if (!grouped[projectName]) {
        grouped[projectName] = [];
      }
      grouped[projectName].push(workstation);
    });
    
    return grouped;
  })();

  // Get all project names that have workstations (sorted)
  $: projectsWithWorkstations = Object.keys(workstationsByProject).sort();

  // Initialize expanded state for new projects (default: all projects expanded)
  $: {
    // Ensure all current projects have an expanded state (default: true)
    projectsWithWorkstations.forEach(projectName => {
      if (!(projectName in expandedProjects)) {
        expandedProjects[projectName] = true;
      }
    });
  }

  function toggleProject(projectName: string) {
    expandedProjects[projectName] = !expandedProjects[projectName];
    expandedProjects = { ...expandedProjects }; // Trigger reactivity
  }

  async function fetchWorkstations() {
    try {
      const response = await fetch(apiUrl('/workstations_status'));
      const data = await response.json();

      // Extract workstations from the response
      // Support both new format (object with workstations) and old format (array)
      if (data.workstations) {
        workstations = [...data.workstations];
      } else if (Array.isArray(data)) {
        // Fallback for backward compatibility (if response is just an array)
        workstations = [...data];
      } else {
        workstations = [];
      }

      // Resets the progress bar
      resetProgressBar = true;
      setTimeout(() => resetProgressBar = false, 100);

    } catch (error) {
      console.error('Error fetching workstations:', error);
    }
  }

  onMount(() => {
    fetchBackendVersion();
    fetchWorkstations();
    setInterval(fetchWorkstations, refreshInterval);
  });
  
  async function fetchBackendVersion() {
    try {
      const res = await fetch(apiUrl('/version'));
      if (!res.ok) throw new Error('bad status');
      const data = await res.json();
      backendVersion = data.backend_version || 'unknown';
    } catch (e) {
      console.error('Error fetching backend version:', e);
      backendVersion = 'unreachable';
    }
  }
  
</script>

<main>
  <HeaderBar frontendVersion={FRONTEND_VERSION} backendVersion={backendVersion}/>
  <div class="container mt-4">
    {#each projectsWithWorkstations as projectName}
      {@const projectWorkstations = workstationsByProject[projectName]}
      {@const collapseId = `collapse-${projectName}`}
      {@const isExpanded = expandedProjects[projectName] || false}
      
      <div class="card mb-3 project-group-card">
        <div class="card-header project-header" on:click={() => toggleProject(projectName)} role="button" tabindex="0" on:keydown={(e) => e.key === 'Enter' && toggleProject(projectName)}>
          <div class="d-flex justify-content-between align-items-center">
            <h5 class="mb-0">
              {projectName} 
              <span class="badge bg-secondary ms-2">{projectWorkstations.length} {projectWorkstations.length === 1 ? 'workstation' : 'workstations'}</span>
            </h5>
            <i class="bi {isExpanded ? 'bi-chevron-up' : 'bi-chevron-down'}"></i>
          </div>
        </div>
        <div 
          class="collapse {isExpanded ? 'show' : ''}" 
          id="{collapseId}">
          <div class="card-body">
            <div class="row">
              {#each projectWorkstations as workstation}
                <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3 mb-4">
                  <WorkstationCard workstation_data={workstation} />
                </div>
              {/each}
            </div>
          </div>
        </div>
      </div>
    {/each}
    
    {#if projectsWithWorkstations.length === 0}
      <div class="alert alert-info mt-4" role="alert">
        No workstations available at the moment.
      </div>
    {/if}
  </div>
  <!--
  <BottomBar totalTime={refreshInterval} resetProgressBar={resetProgressBar}/>
  -->
</main>

<style>
  .project-group-card {
    border: 1px solid #dee2e6;
    border-radius: 0.375rem;
  }

  .project-header {
    background-color: #f8f9fa;
    cursor: pointer;
    user-select: none;
    transition: background-color 0.2s ease;
  }

  .project-header:hover {
    background-color: #e9ecef;
  }

  .project-header:focus {
    outline: 2px solid var(--primary-color, #0d6efd);
    outline-offset: -2px;
  }
</style>
