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


## Project Structure
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

## Run Locally
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Virtual Network topology
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
- Posts JSON configs to submit_config for full analysis

# Agent must include:
- cdp_neighbors: output of show cdp neighbors detail
- raw_config: full running config
- interfaces: parsed with mode + neighbor info injected

## Getting Started
### Download the code locally
Using the `git` command from the terminal:

```bash
$ git clone https://github.com/jehad-art/NetOrb.git
```

or by clicking on `Code >> Local >> Download ZIP` on the repository main page.

### Install required Packages
You can install all these dependencies using `pip`:<br>
`Netmiko`<br>
```bash
pip install netmiko 
```
`prettytable`<br>
```bash
python -m pip install -U prettytable 
```
### Implementation code structure
The code structured into the following files:<br>
- `Extract_config.py` (to extract the router configuration to a string variable)<br>
- `Original_config.txt` (the extracted config)<br>
- `Structure_config.py` (to read the extracted config and convert it to final json form)<br>
- `Config_C3745.json` (structure file to be analyzed)<br>
- `Analyze_config.py` (to analyze the structured file line by line and identify the misconfiguration and suggested fixes)<br>
- `Print_config.py` (print the resultant output in a tabular format for human readable)<br>
- `Main.py` (the main file to call all previous functions in and run it)<br>


### Required changes
After installation and preparating the prerequisites, open the `Extract_config.py` file and update the router ip address, username and password to match your set of configured access in the router:<br>
```bash
from netmiko import ConnectHandler
def extract_connfig(output):
    device = ConnectHandler(device_type='cisco_ios', ip='<your router ip>', username='<router username>', password='<router password>')
    output = device.send_command("show run")
    device.disconnect() 
```
Once this done, just open the file `main.py` and run it. or you can make yours and add the following code:<br>
```bash
from extract_config import *
from structure_config import *
from analyze_config import *
from print_config import *
output = ""
extract_connfig(output)
structure(output)
analyze(output)
printing(output)
```

## Expected Output
Sample output for the implemented work:<br>

<img src="https://github.com/user-attachments/assets/00cda780-d3a4-4f8b-aea6-6bb20edcce4e" /><br>
<p align='center'>Figure: The output of a sample router's configuration result</p><br><br>


[![image](https://github.com/user-attachments/assets/adf50973-c55f-4203-a40c-7f2385a479cf)](https://youtu.be/Q3LzE3wRGoY)


