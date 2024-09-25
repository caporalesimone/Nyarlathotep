<script lang="ts">
  export let name: string;
  export let status: boolean;
</script>

<div class="card mb-3">
  <div class="card-body">
    <h5 class="card-title">{name}</h5>
    <p class="card-text">Status: {status}</p>
  </div>
</div>
