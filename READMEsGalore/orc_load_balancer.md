# How to Set Up a Public HTTPS Load Balancer in Oracle Cloud Infrastructure (OCI) for a Flask Application

## Prerequisites

- An OCI account with permissions to create and manage load balancers and compute instances.
- An Oracle Compute Instance running your Flask application (with or without Nginx as a proxy).
- A Virtual Cloud Network (VCN) properly set up in OCI.
- An SSL/TLS certificate for securing the communication.

## Step-by-Step Guide

### Step 1: Access the OCI Console

Log in to the OCI Console with your credentials and navigate to the Networking section, then Load Balancers.

### Step 2: Create a New Load Balancer

1. Click on **Create Load Balancer**.
2. For **Load Balancer Name**, enter a unique name (e.g., `lb_2024-0315-1505`).

### Step 3: Choose Visibility Type

- **Public**: Select if your load balancer will receive traffic from the internet.
- For **Assign a public IP address**:
  - **Ephemeral IP Address**: Select if you want OCI to automatically assign a temporary public IP.
  - **Reserved IP Address**: Choose if you wish to use or create a permanent public IP address. CHOOSE THIS to make life less difficult

### Step 4: Configure Bandwidth

Free accounts only have 10Mbps options as of when i created this so below is kinda moot.
Specify the minimum and maximum bandwidth for your load balancer (e.g., 10 Mbps to 8000 Mbps). The flexible shape allows you to scale the load balancer's bandwidth based on demand.

### Step 5: Enable IPv6 (Optional)

Check **Enable IPv6 address assignment** if you require IPv6 support for your load balancer, enabling dual-stack IPv4/IPv6.  No idea if this is even still an option just choose IPv$

### Step 6: Choose Networking

Select a Virtual Cloud Network and then choose a Subnet:

- For a public load balancer, select a single regional subnet or two availability domain-specific subnets in different availability domains for high availability.  For https proxy just choose one subnet as we are not using this load balancer in the traditional sense but its being setup for that if this server does need load balancing.  Our goal is using it for our https endpoint config and proxy.

### Step 7: Configure Advanced Options (Optional)

Use Network Security Groups (NSGs) to control traffic to and from your load balancer. NSGs are an optional but recommended security feature.  Do this after everything works not in this intial config.

### Step 8: Import and Configure SSL/TLS Certificate

1. **Generate or Obtain an SSL/TLS Certificate**:
   - If you don't already have an SSL/TLS certificate, you can generate one using tools like OpenSSL or obtain one from a Certificate Authority (CA) such as Let's Encrypt, DigiCert, etc.  Or use the other readme I created it hits on just about all the steps in order.  
2. **Prepare Certificate Files**:

   - Ensure you have the following files ready:
     - **Certificate**: `yourdomain.crt`
     - **Certificate Chain**: `yourdomain-ca-bundle.crt`
     - **Private Key**: `yourdomain.key`

3. **Upload Certificate to OCI**:
   - Navigate to the **Load Balancers** section in the OCI Console.
   - Select your load balancer and click on **Certificates**.
   - Click **Upload Certificate** and provide the following:
     - **Certificate Name**: Give your certificate a name.
     - **Certificate**: Upload the `yourdomain.crt` file.
     - **Intermediate Certificates (if applicable)**: Upload the `yourdomain-ca-bundle.crt` file.
     - **Private Key**: Upload the `yourdomain.key` file.
   - Click **Upload** to import your certificate.

### Step 9: Configure Backend Set

#### Scenario A: Flask App Without Nginx Proxy

1. Create a Backend Set and add your compute instance as a backend.
2. Specify the instance's **private IP address** and the port where the Flask app listens (e.g., port 8001).
3. Set up a health check policy with a simple HTTPS check to ensure the load balancer can monitor the availability of your Flask app.

#### Scenario B: Flask App with Nginx Proxy

1. Create a Backend Set and add your compute instance as a backend.
2. Specify the instance's **private IP address** and the port where Nginx listens (typically port 443 for HTTPS).
3. Set up a health check policy with a simple HTTPS check to ensure the load balancer can monitor the availability of your Nginx server.

### Step 10: Configure a Listener

1. Add a listener for your load balancer, selecting **HTTPS** as the protocol and specifying the listening port (443 for HTTPS).
2. Select the SSL/TLS certificate you uploaded in Step 8.
3. Associate the listener with the backend set you created earlier.

### Step 11: Review and Create

Review your configuration details and click **Create** to deploy your load balancer.

### Step 12: DNS Configuration (Optional)

Once your load balancer is provisioned, it will be assigned a public IP address. You can update your DNS records to point your domain to this IP address, enabling users to access your application via a friendly URL.

## Final Steps and Testing

- **Scenario A**: Your load balancer will now start routing incoming HTTPS traffic to your Flask app on port 8001. Test the setup by accessing your application through the load balancer's public IP address or domain name (if you've configured DNS), ensuring the application is reachable as expected.
- **Scenario B**: Your load balancer will now start routing incoming HTTPS traffic to your Nginx server on port 443, which will forward it to your Flask app on port 8001. Test the setup by accessing your application through the load balancer's public IP address or domain name (if you've configured DNS), ensuring the application is reachable as expected.

By following these instructions, you've successfully configured a public HTTPS load balancer in OCI, enhancing the scalability and availability of your application served via Flask, with or without Nginx as a proxy.

---

### Example Commands for OCI CLI

Here is a summary of key OCI CLI commands used during the configuration process:

- **List backend sets**:

  ```bash
  oci lb backend-set list --load-balancer-id <load-balancer-ocid>
  ```

- **Update backend set**:

  ```bash
  oci lb backend-set update --options
  ```

- **Check backend health**:

  ```bash
  oci lb backend-health get --backend-set-name <name> --backend-name <ip:port> --load-balancer-id <load-balancer-ocid>
  ```

---
