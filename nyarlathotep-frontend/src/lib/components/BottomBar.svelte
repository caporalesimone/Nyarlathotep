<script lang="ts">
  export let totalTime: number; // Tempo totale in millisecondi
  export let resetProgressBar: boolean; // Trigger per resettare la progress bar
  
  let timeRemaining: number = totalTime;
  let progress: number = 100;
  let interval: NodeJS.Timeout | null = null;

  function startProgress() {
    if (interval) clearInterval(interval);
    
    timeRemaining = totalTime;
    progress = 100;

    interval = setInterval(() => {
      timeRemaining -= 1000; // Aggiorna ogni secondo
      progress = (timeRemaining / totalTime) * 100; // Aggiorna la percentuale di progresso

    }, 1000);
  }

  // Ogni volta che il trigger cambia, riavvia la progress bar
  $: if (resetProgressBar) {
    startProgress();
  }
</script>

<style>
  .bottom-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 10px;
    background-color: var(--background-color);
  }

  .progress {
    height: 100%;
    background-color: var(--primary-color);
    transition: width 1s linear;
  }
</style>

<div class="bottom-bar">
  <div class="progress" style="width: {progress}%;"></div>
</div>
