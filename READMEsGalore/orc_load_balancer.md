# Comprehensive Guide to Setting Up an HTTP Load Balancer in OCI

This guide walks you through the detailed process of setting up a public HTTP load balancer in Oracle Cloud Infrastructure (OCI) to distribute traffic to an Nginx server running on a single Oracle Compute Instance. This configuration enhances your application's availability and scalability.

## Prerequisites

- An OCI account with permissions to create and manage load balancers and compute instances.
- An Oracle Compute Instance running Nginx, ready to serve your application.
- A Virtual Cloud Network (VCN) properly set up in OCI.

## Step-by-Step Guide

### Step 1: Access the OCI Console

Log in to the OCI Console with your credentials and navigate to the **Networking** section, then **Load Balancers**.

### Step 2: Create a New Load Balancer

1. Click on **Create Load Balancer**.
2. For **Load Balancer Name**, enter a unique name (e.g., `lb_2024-0315-1505`).

### Step 3: Choose Visibility Type

- **Public**: Select if your load balancer will receive traffic from the internet.
  - For **Assign a public IP address**:
    - **Ephemeral IP Address**: Select if you want OCI to automatically assign a temporary public IP.
    - **Reserved IP Address**: Choose if you wish to use or create a permanent public IP address.

### Step 4: Configure Bandwidth

- Specify the **minimum** and **maximum bandwidth** for your load balancer (e.g., 10 Mbps to 8000 Mbps). The flexible shape allows you to scale the load balancer's bandwidth based on demand.

### Step 5: Enable IPv6 (Optional)

- Check **Enable IPv6 address assignment** if you require IPv6 support for your load balancer, enabling dual-stack IPv4/IPv6.

### Step 6: Choose Networking

- **Select a Virtual Cloud Network** and then choose a **Subnet**:
  - For a public load balancer, select a **single regional subnet** or **two availability domain-specific subnets** in different availability domains for high availability.

### Step 7: Configure Advanced Options (Optional)

- **Use Network Security Groups (NSGs)** to control traffic to and from your load balancer. NSGs are an optional but recommended security feature.

### Step 8: Configure Backend Set

- **Create a Backend Set** and add your compute instance as a backend. Specify the instance's **IP address** and the port where Nginx listens (typically port 80 for HTTP).
- Set up a health check policy with a simple HTTP check to ensure the load balancer can monitor the availability of your Nginx server.

### Step 9: Configure a Listener

- Add a listener for your load balancer, selecting **HTTP** as the protocol and specifying the listening port (80 for HTTP).
- Associate the listener with the backend set you created earlier.

### Step 10: Review and Create

- Review your configuration details and click **Create** to deploy your load balancer.

### Step 11: DNS Configuration (Optional)

- Once your load balancer is provisioned, it will be assigned a public IP address. You can update your DNS records to point your domain to this IP address, enabling users to access your application via a friendly URL.

### Final Steps and Testing

- Your load balancer will now start routing incoming HTTP traffic to your Nginx server.
- Test the setup by accessing your application through the load balancer's public IP address or domain name (if you've configured DNS), ensuring the application is reachable as expected.

By following these instructions, you've successfully configured a public HTTP load balancer in OCI, enhancing the scalability and availability of your application served via Nginx.


---
---

# OCI Load Balancer and Backend Set Configuration Guide

This guide provides a comprehensive overview of setting up, configuring, and troubleshooting a load balancer in Oracle Cloud Infrastructure (OCI) to route traffic to a web application served by Nginx running in Docker on an OCI compute instance.

## Overview

Deploying a web application on OCI involves configuring various resources to ensure high availability, performance, and security. This document covers the journey of setting up a load balancer to distribute incoming traffic across backend servers, specifically focusing on a scenario where the application and Nginx server are hosted on a single compute instance.

## Initial Setup

### Creating a Load Balancer

The process began with creating a public load balancer within OCI to route external traffic to the application:

1. **Load Balancer Creation**: A public load balancer was created, specifying the necessary bandwidth and associating it with a regional subnet for broad availability across an OCI region.

2. **Backend Set Configuration**: A backend set was configured for the load balancer, intended to include the compute instance running the Nginx server and the application.

3. **Listener Configuration**: An HTTP listener was set up to listen on port 80, the default for HTTP traffic.

### Security and Subnet Configurations

Security lists for the subnet hosting the load balancer and the compute instance were adjusted to allow ingress and egress traffic on the necessary ports for the application and health checks.

## Troubleshooting and Debugging

### Direct Access Verification

Initial testing involved directly accessing the application through its public IP and designated port to verify that the Nginx server and application were running as expected.

### Load Balancer Health Checks

The primary issue encountered was with load balancer health checks failing. The backend set was initially configured with a health check targeting port 80, while the application was serving traffic on a different port.

#### Steps Taken:

1. **Backend Set and Health Check Reconfiguration**: Commands were executed using the OCI CLI to update the backend set configuration, explicitly setting the health check to target the correct port (`8001`) where the application was actually running.

2. **Security List Adjustments**: Security lists were reviewed and adjusted to ensure traffic on the new port could flow between the load balancer and the compute instance.

3. **CLI Commands for Debugging**: Various OCI CLI commands were utilized to list backend sets, update backend set configurations, and check the health status of backends.

### Resolution

The successful update of the health check configuration to the correct port and path, coupled with ensuring proper security list settings, resolved the health check failures, allowing the load balancer to route traffic effectively to the backend server.

## Commands Used

Here is a summary of key OCI CLI commands used during the troubleshooting process:

- List backend sets: `oci lb backend-set list --load-balancer-id <load-balancer-ocid>`
- Update backend set: `oci lb backend-set update --options`
- Check backend health: `oci lb backend-health get --backend-set-name <name> --backend-name <ip:port> --load-balancer-id <load-balancer-ocid>`

## Lessons Learned

- **Health Check Port Alignment**: Ensure the health check port and path correctly align with where the application is actually running.
- **Security List Configurations**: Adjust security lists to permit traffic for both the load balancer's listener and backend health checks.
- **OCI CLI Utility**: The OCI CLI is a powerful tool for managing OCI resources and troubleshooting.

## Conclusion

Setting up a load balancer in OCI involves careful configuration of the load balancer itself, backend sets, health checks, and network security settings. Through systematic troubleshooting and the use of the OCI CLI for configuration and debugging, we were able to resolve issues related to health check failures and ensure the load balancer effectively routes traffic to the intended backend application.

---

This README provides a structured overview of the process you've gone through, highlighting key steps, challenges, and resolutions in configuring your load balancer setup in OCI. Feel free to adjust the content to better fit your specific scenario or add additional details as necessary.
