<script lang="ts">
  import type { WorkstationStatus } from '../../types.js';

  export let workstation_data: WorkstationStatus;

  let name: string = workstation_data.details.client_name;
  let uptime: string = workstation_data.details.os.uptime;

let status: string = workstation_data.timed_out == true ? 'Offline' : 'Online';
</script>

<div class="card mb-3">
  <div class="card-body">
    <h5 class="card-title">{name}</h5>
    <p class="card-text">Uptime: {uptime}</p>
    <p class="card-text">Status: {status}</p>
  </div>
</div>
