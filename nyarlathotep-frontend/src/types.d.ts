export interface Hardware {
  cpu_usage: number;
  disk_total_GB: number;
  disk_used_GB: number;
  ram_total_MB: number;
  ram_used_MB: number;
  serial_number: string;
}

export interface NetInterface {
  interface: string;
  ip_addresses: string[];
  mac: string;
}

export interface OS {
  os_name: string;
  os_platform: string;
  uptime: string;
}

export interface User {
  idle_time: string;
  logged: boolean;
  login_time: string;
  session_id: string;
  session_name: string;
  status: string;
  username: string;
}

export interface WorkstationDetails {
  client_name: string;
  client_sw_version: string;
  hardware: Hardware;
  hostname: string;
  json_version: string;
  local_time: string;
  net_interfaces: NetInterface[];
  network_name: string;
  os: OS;
  users: User[];
  project_name: string;
}

export interface WorkstationStatus {
  details: WorkstationDetails;
  last_update_epoch: number;
  last_update_utc: string;
  new_version_available: string;
  timed_out: boolean;
}
