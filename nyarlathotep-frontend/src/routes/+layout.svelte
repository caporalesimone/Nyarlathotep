<script lang="ts">
    import { onMount } from 'svelte';
    import "bootstrap/dist/css/bootstrap.min.css";
    import "bootstrap-icons/font/bootstrap-icons.min.css";
    
    // Import Bootstrap JS only on client side
    onMount(async () => {
        await import("bootstrap/dist/js/bootstrap.bundle.min.js");
    });
</script>

<slot />