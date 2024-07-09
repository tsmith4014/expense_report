# HTTPS Setup and Certificate Renewal Guide for OCI Load Balancer with SSL/TLS Certificate

This guide provides a step-by-step approach to setting up HTTPS for an application deployed on Oracle Cloud Infrastructure (OCI) using a Load Balancer and securing it with an SSL/TLS certificate. It also includes the steps to renew the SSL/TLS certificate when necessary.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Domain Configuration](#domain-configuration)
4. [SSL/TLS Certificate Acquisition](#ssltls-certificate-acquisition)
   - [Generate Certificate with Certbot](#generate-certificate-with-certbot)
5. [Certificate Import into OCI](#certificate-import-into-oci)
6. [Load Balancer Configuration](#load-balancer-configuration)
7. [Listener Setup for HTTPS](#listener-setup-for-https)
8. [Certificate Renewal](#certificate-renewal)
9. [Conclusion](#conclusion)

## Overview

The process involves several major steps:

1. Domain Configuration
2. SSL/TLS Certificate Acquisition
3. Certificate Import into OCI
4. Load Balancer Configuration
5. Listener Setup for HTTPS
6. Certificate Renewal

## Prerequisites

- An OCI account and basic understanding of OCI services.
- A registered domain.
- Access to modify DNS records for your domain.
- An Oracle Compute Instance running your Flask application (with or without Nginx as a proxy).
- An SSL/TLS certificate for securing the communication.

## Domain Configuration

Ensure you have a domain ready and have access to modify its DNS settings. If you're setting up a subdomain, decide on the subdomain name (e.g., `expenseapp.devopschad.com`).

## SSL/TLS Certificate Acquisition

We will use Let's Encrypt for a free certificate. Ensure Certbot is installed on a server where you can run it.

### Generate Certificate with Certbot

1. **Generate Certificate with Certbot**:
   Run Certbot with the DNS plugin for your DNS provider, or manually if the plugin is not available. For a subdomain, use:

   ```bash
   sudo certbot certonly --manual --preferred-challenges=dns -d expenseapp.devopschad.com
   ```

2. **Update DNS TXT Record**:
   During the Certbot process, a TXT record will be required to verify domain ownership. The required TXT record will be provided by Certbot.

3. **Verify DNS Record**:
   Confirm the TXT records are visible globally before continuing with Certbot. This might take a few minutes. Use tools like `dig` to verify:

   ```bash
   dig _acme-challenge.expenseapp.devopschad.com TXT
   ```

4. **Retrieve Certificate and Private Key**:
   After Certbot successfully generates the certificate, use the following commands to view the certificate and private key:

   ```bash
   sudo cat /etc/letsencrypt/live/expenseapp.devopschad.com/fullchain.pem
   sudo cat /etc/letsencrypt/live/expenseapp.devopschad.com/privkey.pem
   ```

## Certificate Import into OCI

After obtaining the certificate, import it into OCI for use with the Load Balancer.

1. **Access Certificates Service in OCI**: Navigate to the OCI console, select "Certificates" under "Identity & Security".
2. **Import Certificate**: Click on "Import Certificate". You will need the certificate, the private key, and the certificate chain.

   - **Certificate**: Copy the first certificate from `/etc/letsencrypt/live/expenseapp.devopschad.com/fullchain.pem`
   - **Certificate Chain**: Copy the entire contents of `/etc/letsencrypt/live/expenseapp.devopschad.com/fullchain.pem`
   - **Private Key**: Copy the contents of `/etc/letsencrypt/live/expenseapp.devopschad.com/privkey.pem`

3. **Fill in the Details**: Provide the requested information and paste/upload the respective files.

## Load Balancer Configuration

Ensure your application is correctly configured to be served through an OCI Load Balancer.

1. **Navigate to Your Load Balancer**: In OCI Console, go to "Networking" > "Load Balancers" and select your load balancer.
2. **Create/Edit HTTPS Listener**:

   - Click on "Listeners".
   - Choose to create a new listener or edit an existing one.
   - Set the protocol to HTTPS and select the imported SSL certificate.
   - Specify other details as required (protocol, port, backend set).

3. **Update DNS**: Point your domain (or subdomain) to the Load Balancer's IP using an A record. For subdomains, a CNAME record pointing to the main domain can also work, depending on your setup.

4. **Test Your Setup**: Once DNS changes propagate, access your domain via HTTPS in a browser to verify the setup.

## Listener Setup for HTTPS

Configure your Load Balancer's listener to serve HTTPS traffic.

1. **Add a Listener for Your Load Balancer**:
   - Select **HTTPS** as the protocol and specify the listening port (443 for HTTPS).
   - Select the SSL/TLS certificate you uploaded.
   - Associate the listener with the backend set you created earlier.

## Certificate Renewal

### Scenario:

The HTTPS served app was running in a Docker container, and to renew the SSL certificate, the app was temporarily spun up in an Oracle instance to obtain a new certificate and update the load balancer.

### Steps Taken:

1. **Requesting a Certificate with Certbot**:

   ```bash
   sudo certbot certonly --manual --preferred-challenges=dns -d expenseapp.devopschad.com
   ```

2. **Update DNS TXT Record**:
   During the Certbot process, a TXT record was required to verify domain ownership. The required TXT record was provided by Certbot.

3. **Verify DNS Record**:
   Use tools like `dig` to verify that the TXT record has been correctly propagated:

   ```bash
   dig _acme-challenge.expenseapp.devopschad.com TXT
   ```

4. **Retrieve Certificate and Private Key**:
   After Certbot successfully generates the certificate, use the following commands to view the certificate and private key:

   ```bash
   sudo cat /etc/letsencrypt/live/expenseapp.devopschad.com/fullchain.pem
   sudo cat /etc/letsencrypt/live/expenseapp.devopschad.com/privkey.pem
   ```

5. **Import the New Certificate into OCI**:

   - **Access Certificates Service in OCI**: Navigate to "Identity & Security" > "Certificates".
   - **Create a New Certificate**: Upload the new certificate and private key obtained from Certbot.
     - **Certificate**: Copy the first certificate from `fullchain.pem`
     - **Certificate Chain**: Copy the entire contents of `fullchain.pem`
     - **Private Key**: Copy the contents of `privkey.pem`
   - **Update Load Balancer**: Associate the new certificate with the load balancer and remove the old one.

6. **Test the New Certificate**:
   Confirm that the new certificate is working by accessing your application via HTTPS:

   ```bash
   https://expenseapp.devopschad.com
   ```

## Conclusion

This guide covered setting up HTTPS for an application on OCI using a Load Balancer and SSL/TLS certificate. Remember, SSL certificate renewal needs to be handled periodically, depending on the certificate authority's policies.

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

By following these instructions, you've successfully configured a public HTTPS load balancer in OCI, enhancing the scalability and availability of your application served via Flask, with or without Nginx as a proxy, and ensured that you can renew the SSL certificate when necessary.
