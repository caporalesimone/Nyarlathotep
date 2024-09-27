export function calculateTimeSince(lastUpdateEpoch: number): string {
    const now = Date.now();
    const lastUpdate = new Date(lastUpdateEpoch * 1000);
    const difference = now - lastUpdate.getTime();
  
    const seconds = Math.floor(difference / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
  
    const displaySeconds = seconds % 60;
    const displayMinutes = minutes % 60;
    const displayHours = hours % 24;
  
    return `${days}d ${displayHours}h ${displayMinutes}m ${displaySeconds}s`;
  }