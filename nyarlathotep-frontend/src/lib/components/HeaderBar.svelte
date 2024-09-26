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
  </script>
  
  <style>
    .top-bar {
      background: linear-gradient(90deg, var(--secondary-color), var(--primary-color));
      margin: 0;
      position: relative;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 65px; /* Adjust height if needed */
    }
  
    .top-bar h1 {
      margin: 0;
      font-family: Arial, sans-serif;
      font-size: 1.5rem;
      font-weight: bold;
      color: white;
      text-align: center;
      flex: 1; /* Center the heading */
    }
  
    .version {
      font-family: 'Courier New', Courier, monospace;
      font-size: 0.75rem;
      color: white;
      position: absolute;
      bottom: 0px;
      right: 3px;
    }
  
    .icon-large {
      font-size: 1.1rem; /* Aumenta la dimensione dell'icona */
      font-weight: bold; /* Rendi l'icona più spessa */
    }

  </style>
  
  <nav class="top-bar">
    <h1>🖥️ Nyarlathotep - Workstation Monitor 🖥️</h1>
    <div class="version">Version: {version}</div>

    <div class="mode-switch">
      <button on:click={toggleTheme} class="btn btn-sm">
        <i class={theme === 'light' ? 'bi bi-moon-fill icon-large' : 'bi bi-sun-fill icon-large'}></i>
      </button>
    </div>
  </nav>
  