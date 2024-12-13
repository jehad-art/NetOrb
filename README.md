# NetBot - An Automated Router Hardening Solution for Small to Medium Enterprises

<h2>Abstract</h2>
Hardening the configuration of network assets has become an essential practice for both General-Purpose and Special-Purpose Operating Systems. Security regulations and standards mandate this process to minimize the risk of misconfiguration, which can lead to significant operational and security vulnerabilities. Misconfigurations leave networks exposed to various types of attacks, compromising the confidentiality, integrity, and availability (CIA) of critical assets. Network administrators often lack the specialized expertise required to implement security configurations, as their primary focus is typically on maintaining network performance and operational efficiency.

here, we are proposing a passive, automated solution for hardening the configurations of Special-Purpose network systems. The solution identifies critical assets and analyzes them for potential misconfigurations. It is designed to address all aspects of network security, including asset configuration, architectural segmentation, and Defense-In-Depth strategies.

This is an implementation of the paper made by H. M. D. G. V. Perera et al.<br>
<a href="https://ieeexplore.ieee.org/document/9623186"> H. M. D. G. V. Perera, K. M. Samarasekara, I. U. K. Hewamanna, D. N. W. Kasthuriarachchi, K. Y. Abeywardena and K. Yapa, "NetBot - An Automated Router Hardening Solution for Small to Medium Enterprises," 2021 IEEE 12th Annual Information Technology, Electronics and Mobile Communication Conference (IEMCON), Vancouver, BC, Canada, 2021 </a>

## Table of Content

- [Prerequisites]("#Prerequisites")
- [Table of Content](#table-of-content)
- [Environment Preparation](#env-description)
- [Virtual Network topology](#topology)
- [Colophon](#colophon)

## Prerequisites
<h3>Software Requirements</h3>
<b>Python: </b>Version 3.8 or higher.<br>
<b>Libraries:</b><br>
        &emsp; - json (for configuration structure)<br>
        &emsp; - pretteytable (for data tabular view)<br>
        &emsp; - netmiko (for network access)<br>
        &emsp; - GNS3 (for network emulation)<br>
        &emsp; - GNS3 VM (Hosting VM and separating network adapters)<br>
    <b>Automation Tools:</b><br>
        &emsp; - Ansible (for large-scale router configuration management, optional)<br>

<h3>Hardware Requirements</h3>
<b>System:</b><br>
   &emsp; - Minimum 4 GB of RAM.<br>
   &emsp; - Minimum 2 GHz dual-core CPU.<br>
<b>Network:</b><br>
   &emsp; - Stable internet connection for fetching vulnerability updates and remote SSH access.<br>

## Environment Preparation
<b>Install Network Emulation (GNS3)::</b><br>
- Install the client.<br>
- Install GNS3 VM.<br>
- Configure the network setting in vmware to make it bridge network.<br>
- Make sure the vm ip in the same subnet of the host’s.<br>
- After client finishes installation, in the setup wizard, choose <b style="color:#006633;">“run appliance in a virtual machine” </b>.<br>
- Install Cisco C3745 IOS v12.3.<br>
- Configure the preferences to add the run through local vm<br>
- Add a new template device with the installed image<br>
- Creating a loopback adapter and connect it through cloud template<br><br>

![image](https://github.com/user-attachments/assets/f0ee65b9-2660-418e-a7cb-6dc3d70b9260)
&emsp;&emsp;
![image](https://github.com/user-attachments/assets/62e196fa-f1d4-4b22-be9f-797eaa22516f)<br>
<p align='center'>Figure: Required settings for GNS3 VM</p>

## Virtual Network topology
<img src="https://github.com/user-attachments/assets/c934e534-911c-4986-8429-889e5e0d1687" />

<br>
<p align='center'>Figure: The somulated network topology</p>
<br>
<h2>Initial Configuration</h2>
<b>Sample configuration applied to the router</b><br>
<img src="https://github.com/user-attachments/assets/309f22d4-7234-419e-9707-3bef64f04a8a" /><br>
<p>Figure: snippet of sample Cisco IOSv12 configuration</p>
```bash

```


