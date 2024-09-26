<script lang="ts">
  export let version: string;

  let theme = 'light'; // Default theme

  // Load theme from local storage on mount
  if (typeof window !== 'undefined') {
    theme = localStorage.getItem('data-theme') || 'light';
    document.documentElement.setAttribute('data-theme', theme);
  }

  function toggleTheme() {
    theme = (theme === 'light') ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('data-theme', theme);
  }

  function openGitHub() {
    window.open('https://github.com/caporalesimone/Nyarlathotep', '_blank');
  }
</script>

<style>
  .top-bar {
    background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
    margin: 0;
    display: flex;
    justify-content: space-between; /* Spazio tra gli elementi */
    align-items: center; /* Allinea verticalmente gli elementi */
    height: 65px; /* Adjust height if needed */
    padding: 0 15px; /* Aggiungi padding per il contenuto */
  }

  .title {
    margin: 0;
    font-family: Arial, sans-serif;
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-align: center;
    flex-grow: 1; /* Il titolo occuperà lo spazio rimanente */
    display: flex; /* Per il centramento verticale */
    justify-content: center; /* Per il centramento orizzontale */
    align-items: center; /* Per il centramento verticale */
  }

  .version {
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.75rem;
    color: white;
    position: absolute;
    bottom: 0px;
    right: 3px;
  }

  .github, .theme-changer {
    display: flex;
    align-items: center; /* Allinea verticalmente */
  }

  .theme-changer button, .github button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 1.5rem;
    font-weight: bold;
    transition: color 0.3s ease; /* Aggiunge una transizione graduale */
  }

  /* Cambia il colore delle icone all'hover */
  .theme-changer button:hover, 
  .github button:hover {
    color: black;
  }
</style>

<nav class="top-bar">
  <div class="github">
    <button class="btn btn-sm" on:click={openGitHub}>
      <i class="bi bi-github"></i>
    </button>
  </div>

  <div class="title">
    Nyarlathotep - Workstations Monitor
  </div>

  <div class="theme-changer">
    <button on:click={toggleTheme} class="btn btn-sm">
      <i class={theme === 'light' ? 'bi bi-moon-fill' : 'bi bi-sun-fill'}></i>
    </button>
  </div>

  <div class="version">Version: {version}</div>
</nav>





