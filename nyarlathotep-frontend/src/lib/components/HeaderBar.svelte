<script lang="ts">
    export let version: string;
</script>

<style>
    .top-bar {
        background: linear-gradient(90deg, #429fde, #32cd32);
        padding: 16px;
        margin: 0;
        position: relative;
    }

    .top-bar h1 {
        margin: 0;
        font-family: Arial, sans-serif;
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
        text-align: center;
    }

    .version {
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.75rem;
        color: white;
        position: absolute;
        bottom: 4px;
        right: 10px;
    }
</style>

<nav class="top-bar">
    <h1>🖥️ Nyarlathotep - Workstation Monitor 🖥️</h1>
    <div class="version">Version: {version}</div>
</nav>
