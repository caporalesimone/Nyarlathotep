<script lang="ts">
    export let title: string;
    export let value: number;
    export let textOnBar: string = "";

    const progressTresholds = {
        low: 40,
        high: 80,
    };

    function progressBarThresholdClass(value: number) {
        if (value < progressTresholds.low) {
            return "low";
        } else if (value >= progressTresholds.high) {
            return "high";
        } else {
            return "medium";
        }
    }
</script>

<strong>{title}:</strong>
<div
    class="progress-bar"
    data-progress-value={progressBarThresholdClass(value)}
>
    <div class="progress-fill" style="width: {value}%"></div>
    <span class="progress-text">
        {#if textOnBar}
            {textOnBar} - {value}%
        {:else}
            {value}%
        {/if}
    </span>
</div>

<style>
    .progress-bar {
        background-color: #e9ecef;
        border-radius: 4px;
        width: 100%;
        height: 18px;
        margin-bottom: 10px;
        position: relative;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
        overflow: hidden; /* Nasconde qualsiasi overflow del contenuto */
    }

    .progress-fill {
        height: 100%;
        border-radius: 4px;
        width: var(--progress);
        background-color: var(--progress-color);
        transition:
            width 0.3s ease,
            background-color 0.3s ease; /* Cambia colore e larghezza con una transizione fluida */
    }

    .progress-text {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        color: black;
        font-size: 0.85em;
    }

    /* Cambia il colore della barra in base al valore di progress */
    .progress-bar[data-progress-value] .progress-fill {
        background-color: rgb(
            98,
            179,
            98
        ); /* Default verde per progress minori del 20% */
    }

    .progress-bar[data-progress-value="medium"] .progress-fill {
        background-color: rgb(
            232,
            232,
            27
        ); /* Giallo per progress tra 20% e 80% */
    }

    .progress-bar[data-progress-value="high"] .progress-fill {
        background-color: red; /* Rosso per progress maggiori dell'80% */
    }
</style>
