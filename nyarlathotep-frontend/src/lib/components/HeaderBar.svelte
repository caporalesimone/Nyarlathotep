<script lang="ts">
  export let version: string;

  let theme = "light"; // Default theme

  // Load theme from local storage on mount
  if (typeof window !== "undefined") {
    theme = localStorage.getItem("data-theme") || "light";
    document.documentElement.setAttribute("data-theme", theme);
  }

  function toggleTheme() {
    theme = theme === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("data-theme", theme);
  }

  function openGitHub() {
    window.open("https://github.com/caporalesimone/Nyarlathotep", "_blank");
  }
</script>

<nav class="top-bar">
  <div class="github">
    <button class="btn btn-sm" on:click={openGitHub}>
      <i class="bi bi-github"></i>
    </button>
  </div>

  <div class="title-section">
    <div class="title-text">Nyarlathotep - Workstations Monitor</div>
    <div class="version">Version: {version}</div>
  </div>

  <div class="theme-changer">
    <button on:click={toggleTheme} class="btn btn-sm">
      <i class={theme === "light" ? "bi bi-moon-fill" : "bi bi-sun-fill"}></i>
    </button>
  </div>
</nav>

<style>
  .top-bar {
    background: linear-gradient(
      90deg,
      var(--secondary-color),
      var(--primary-color)
    );
    margin: 0;
    display: flex;
    justify-content: space-between; /* Spazio tra gli elementi */
    align-items: center; /* Allinea verticalmente gli elementi */
    height: 65px; /* Adjust height if needed */
    padding: 0 15px; /* Aggiungi padding per il contenuto */
  }

  .title-section {
    font-family: Arial, sans-serif;
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-align: center;
    display: flex; /* Usa Flexbox per l'allineamento interno */
    flex-direction: column; /* Allinea gli elementi verticalmente */
    justify-content: center; /* Centra verticalmente il contenuto */
    align-items: center; /* Allinea orizzontalmente al centro */
    flex-grow: 1; /* Il titolo occuperà lo spazio rimanente */
  }

  .title-text {
    margin: 0;
  }

  .version {
    font-family: "Courier New", Courier, monospace;
    font-size: 0.7rem;
    color: black;
    margin: 0;
    line-height: 1.2; /* Riduci l'altezza della linea per avvicinare il testo e la versione */
  }

  .github,
  .theme-changer {
    display: flex;
    align-items: center; /* Allinea verticalmente */
  }

  .github button,
  .theme-changer button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 1.3rem;
    font-weight: bold;
    transition: color 0.5s ease;
  }

  /* Cambia il colore delle icone all'hover */
  .github button:hover,
  .theme-changer button:hover {
    color: black;
  }
</style>
