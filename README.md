# NetOrb Backend

**NetOrb** is a network security configuration analysis platform designed to automate the discovery, auditing, and hardening of special-purpose infrastructure devices — including routers, switches, and firewalls. This backend is built with **FastAPI** and supports agent-based config collection, rule-based security analysis, and cross-device interconnection validation.

## Table of Content

- [API Endpoint](#API-Endpoints)
- [Prerequisites](#Prerequisites)
- [Table of Content](#table-of-content)
- [Environment Preparation](#Environment-Preparation)
- [Virtual Network topology](#Virtual-Network-topology)
- [Getting Started](#Getting-Started)
- [Expected Output](#Expected-Output)

## Features

- **Security Analysis Engine**: Detects misconfigurations and missing security best practices per device.
- **Interconnection Checks**: Identifies interconnection issues between devices and applies architecture validation.
- **FastAPI Backend**: Handles config ingestion, analysis, and secure credential access.
- **Rule-Based Analyzer**:
  - Device-specific rules (e.g., Cisco IOS routers/switches, Juniper, Aruba, etc.)
  - Shared base rules (e.g., telnet enabled, plaintext passwords) in Cisco IOS L2 & L3.
  - Interconnection rules (e.g., trunk mismatches, bypassed security zones)
- **Agent-Compatible**: Works with a lightweight Python agent running inside EVE-NG or other labs.


## Example Rules

Misconfiguration

| Rule ID | Description                                                  | Severity |
|---------|--------------------------------------------------------------|----------|
| R01   | Telnet is enabled on VTY lines   | High     |
| R03   | enable_plaintext	Enable password stored in plaintext        | High     |
| R09   | nat_no_overload	NAT is used without overload flag   | Medium   |

Missing Recommendations

| Rule ID | Description                                                  | Severity |
|---------|--------------------------------------------------------------|----------|
| R17   | SSH version 2 not configured   | Medium     |
| R18   | Password encryption service is not enabled   | Medium   |

Interconnection Issues

| Rule ID | Description                                                  | Severity |
|---------|--------------------------------------------------------------|----------|
| INT01   | Trunk mismatch between connected switch ports   | Medium     |
| INT02   | Trunk port connected to unknown/rogue device   | Medium   |
| INT03   | BPDU Guard / Root Guard misalignment across switches   | High   |
| INT04   | Firewall bypass: traffic reaching app server directly, skipping WAF   | Medium   |
	

## Prerequisites
<h3>Software Requirements</h3>
<b>Python: </b>Version 3.8 or higher.<br>
<b>Libraries:</b><br>
        &emsp; - json (for configuration structure)<br>
        &emsp; - pretteytable (for data tabular view)<br>
        &emsp; - netmiko (for network access)<br>
	&emsp; - FastAPI (for backend)<br>
 	&emsp; - Pymongo (for database integration)<br>
	&emsp; - Cryptography (Fernet)<br>
 	&emsp; - Uvicorn (for development)<br>
    <b>Network Emulation</b><br>
        &emsp; - Eve-ng (Cloud virtual lab - Cloudmylab)<br>
        &emsp; - Cisco Anyconnect (VPN Access to cloud)<br>

<h3>Hardware Requirements</h3>
<b>System:</b><br>
   &emsp; - Minimum 32 GB of RAM.<br>
   &emsp; - Minimum 2 GHz dual-core CPU with 8 cores for the VM.<br>
<b>Network:</b><br>
   &emsp; - Stable internet connection for fetching vulnerability updates and remote SSH access.<br>

## Environment Preparation
<b>Install Anyconnect</b><br>
- Connect to "https://new-jersey01.cloudmylab.com"<br>
- Username: jehad_alhussien<br>
- Password: Alaacl@53$$$$$<br>
- Then access the server through: https://10.20.51.2 <br>
- Credentials: admin/eve<br>
- The lab name: Heteroginous lab<br>
- Cloud running on frontend: https://vercel.com/jehads-projects-f04d7275/net-orb-dashboard<br>
- Cloud running on backend: https://dashboard.render.com/web/srv-d0jt36juibrs73913hdg/logs<br>
- Cloud running for database: mogodb atlas<br>


## Virtual Network topology
<img src="https://github.com/user-attachments/assets/1357cce1-db45-4682-b0f6-eb862b498d88" /><br>
<p align='center'>Figure: The somulated network topology</p>
<br>
<h2>Initial Configuration</h2>
<b>Sample configuration applied to the router</b><br>
<img src="https://github.com/user-attachments/assets/309f22d4-7234-419e-9707-3bef64f04a8a" /><br>
<p>Figure: snippet of sample Cisco IOSv12 configuration</p><br>

## Agent Integration

# The agent perform
- Device discovery via TCP scanning
- Config extraction via SSH (Netmiko)
- Mode + CDP neighbor parsing
- Posts JSON configs to `submit_config` for full analysis

# Agent must include:
- `cdp_neighbors`: output of show `cdp neighbors detail`
- `raw_config`: full running config
- `interfaces`: parsed with mode + neighbor info injected

## Getting Started
### Download the code locally
Using the `git` command from the terminal:

```bash
$ git clone https://github.com/jehad-art/NetOrb.git
```

or by clicking on `Code >> Local >> Download ZIP` on the repository main page.

### Install required Packages
You can install all these dependencies using `pip`:<br>
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Implementation code structure
The code structured into the following files:<br>
NetOrb/
- analyzer/
  - analyzer.py # Main analysis logic
  - base_rules.py # Generic security checks
  - router_rules.py # Router-specific rules
  - switch_rules.py # Switch-specific rules
  - interconnection_rules.py # Cross-device analysis
- db.py # MongoDB collections
- routes
  - devices.py # FastAPI router for config endpoints
- crypto_utils.py # Fernet encryption/decryption
- settings.py # App settings and agent token


## API Endpoints

### `POST /devices/submit_config`

Submit a full device configuration JSON for analysis.

- Detects misconfigurations
- Applies device-type specific rules
- Performs interconnection analysis (if other devices exist)

**Returns**:  
```json
{
  "message": "Configuration and analysis received",
  "score": 65,
  "issues": 7,
  "analysis": {
    "misconfigurations": [],
    "missing_recommendations": [],
    "interconnection_issues": []
  }
}
```
### `GET /devices/`

Returns a list of all discovered/provisioned devices.
### `GET /devices/secrets/{ip}`

Returns decrypted credentials for the agent (protected by token auth).
### `POST /devices/discovered`

Registers or updates a discovered device (used by the agent after scanning).
### `GET /interconnection_issues`

Re-analyzes all saved configurations for interconnection issues only.

 ## Notes

- Interconnection issues only appear if both ends of a link are discovered.
- Device hostname must match the `cdp_neighbor["device_id"]` for rules to link devices.
- `mode` must be properly extracted from interface configs `(switchport mode)`

## Expected Output
Sample output for the implemented work:<br>

<img src="https://github.com/user-attachments/assets/7657a906-1edf-4264-82b5-0c45570b7db5" /><br>
<p align='center'>Figure: The output of a sample device's configuration result</p><br><br>


## Contact

Developed as part of a cybersecurity MX project. For questions or contributions, open an issue or reach out via GitHub.


