# NetOrb Backend

**NetOrb** is a network security configuration analysis platform designed to automate the discovery, auditing, and hardening of special-purpose infrastructure devices — including routers, switches, and firewalls. This backend is built with **FastAPI** and supports agent-based config collection, rule-based security analysis, and cross-device interconnection validation.


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

🧪 Example Rules
Misconfiguration
ID	Tag	Description
R01	telnet_enabled	Telnet is enabled on VTY lines
R03	enable_plaintext	Enable password stored in plaintext
R09	nat_no_overload	NAT is used without overload flag
Missing Recommendations
ID	Tag	Description
R17	ssh_v2_missing	SSH version 2 not configured
R18	service_encryption_missing	Password encryption service is not enabled
Interconnection Issues
ID	Description
INT01	Trunk mismatch between connected switch ports
(planned) INT02	Trunk port connected to unknown/rogue device
(planned) INT03	BPDU Guard / Root Guard misalignment across switches
(planned) INT04	Firewall bypass: traffic reaching app server directly, skipping WAF
# NetOrb - An Automated Network security Hardening

<h2>Abstract</h2>
Hardening the configuration of network assets has become an essential practice for both General-Purpose and Special-Purpose Operating Systems. Security regulations and standards mandate this process to minimize the risk of misconfiguration, which can lead to significant operational and security vulnerabilities. Misconfigurations leave networks exposed to various types of attacks, compromising the confidentiality, integrity, and availability (CIA) of critical assets. Network administrators often lack the specialized expertise required to implement security configurations, as their primary focus is typically on maintaining network performance and operational efficiency.

This is a proposed passive, automated solution for hardening the configurations of the network architecture. The solution identifies critical assets and analyzes them for potential misconfigurations. It is designed to address all aspects of network security, including asset configuration, architectural segmentation, and Defense-In-Depth strategies.

## Table of Content

- [Prerequisites](#Prerequisites)
- [Table of Content](#table-of-content)
- [Environment Preparation](#Environment-Preparation)
- [Virtual Network topology](#Virtual-Network-topology)
- [Getting Started](#Getting-Started)
- [Expected Output](#Expected-Output)

## Prerequisites
<h3>Software Requirements</h3>
<b>Python: </b>Version 3.8 or higher.<br>
<b>Libraries:</b><br>
        &emsp; - json (for configuration structure)<br>
        &emsp; - pretteytable (for data tabular view)<br>
        &emsp; - netmiko (for network access)<br>
    <b>Automation Tools:</b><br>
        &emsp; - Ansible (for large-scale router configuration management, optional)<br>
    <b>Network Emulation</b><br>
        &emsp; - Eve-ng (for network emulation)<br>
        &emsp; - Eve-ng VM (Hosting VM and separating network adapters)<br>

<h3>Hardware Requirements</h3>
<b>System:</b><br>
   &emsp; - Minimum 32 GB of RAM.<br>
   &emsp; - Minimum 2 GHz dual-core CPU with 8 cores for the VM.<br>
<b>Network:</b><br>
   &emsp; - Stable internet connection for fetching vulnerability updates and remote SSH access.<br>

## Environment Preparation
<b>Install Network Emulation (Eve-ng)::</b><br>
- Install the client.<br>
- Install Eve-ng VM.<br>
- Configure the network setting in vmware to make it bridge network.<br>
- Make sure the vm ip in the same subnet of the host’s.<br>
- After client finishes installation, in the setup wizard, choose <b style="color:#006633;">“run appliance in a virtual machine” </b>.<br>
- Install the intended virtual system (if it is node in eve-ng, it must be qcow2 file).<br>
- Configure the preferences to add the run through local vm<br>
- Add a new template device with the installed image<br>
- Creating a new network adapter from within the virtualization system<br>
- After creating the virtual adapter and assiging an ip to it, assign an ip to eve-ng vm in the same subnet to any interface that would be selected for the cloud node which will be addedinside eve-ng. see below on how to do it by accessing the file in ```bash cat /etc/network/interfaces``` :<br>

![image](https://github.com/user-attachments/assets/92a7adff-0945-493b-ada4-c471eb6a7b90)
<br>
<p>Figure: Required settings for eve-ng VM</p>

## Virtual Network topology
<img src="https://github.com/user-attachments/assets/a2cce0ee-4db9-4420-8955-710239a62c6f" />
<br>
<p align='center'>Figure: The somulated network topology</p>
<br>
<h2>Initial Configuration</h2>
<b>Sample configuration applied to the router</b><br>
<img src="https://github.com/user-attachments/assets/309f22d4-7234-419e-9707-3bef64f04a8a" /><br>
<p>Figure: snippet of sample Cisco IOSv12 configuration</p><br>

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


