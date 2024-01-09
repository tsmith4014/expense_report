# README.md for Oracle Instance Flask App Deployment

## Table of Contents

1. [Introduction](#introduction)
2. [Environment Setup](#environment-setup)
3. [Application Deployment](#application-deployment)
4. [Oracle Cloud Instance Setup](#oracle-cloud-instance-setup)
5. [WSGI Server Setup with Gunicorn](#wsgi-server-setup-with-gunicorn)
6. [Systemd Service Configuration](#systemd-service-configuration)
7. [Testing and Validation](#testing-and-validation)

---

## Introduction

This README document outlines the steps to deploy a Flask-based web application, specifically an Expense Report Webapp, on an Oracle Cloud Instance. The application will be available at port 8000.

## Environment Setup

### Prerequisites

- Oracle Cloud Instance access with the provided key (`selfs.key`).
- SSH access to the Oracle Instance.

### Initial Steps

1. **Update Package Manager**

   ```bash
   sudo yum update -y
   ```

2. **Install Git, Python 3.8, and Development Package**

   ```bash
   sudo yum install git python38 python38-devel -y
   ```

3. **Clone the Expense Report Webapp Repository**
   ```bash
   cd /home/opc/
   git clone https://github.com/tsmith4014/expense_report.git
   ```

## Application Deployment

### Setting up the Working Environment

1. **Navigate to the Cloned Repository**

   ```bash
   WORK_DIR="/home/opc/expense_report"
   cd $WORK_DIR
   ```

2. **Install Python-Pip**

   ```bash
   sudo yum install python3-pip -y
   ```

3. **Modify `requirements.txt` to Include Gunicorn**

   ```bash
   echo "gunicorn" >> requirements.txt
   ```

4. **Create a Python Virtual Environment**

   ```bash
   VENV_PATH="/home/opc/expense_report/venv"
   python3.8 -m venv venv
   source $VENV_PATH/bin/activate
   pip install -r requirements.txt
   ```

5. **Create Gunicorn Configuration File**
   ```bash
   echo "bind = '0.0.0.0:8000'
   workers = 4" > gunicorn_config.py
   ```

## Oracle Cloud Instance Setup

Ensure that the Oracle Cloud instance is configured to allow traffic on port 8000.

## WSGI Server Setup with Gunicorn

Gunicorn serves as the WSGI server for the Flask application.

## Systemd Service Configuration

1. **Create Systemd Service File**

   ```bash
   SYSTEMD_SERVICE_FILE="/etc/systemd/system/expense-report-webapp.service"
   sudo bash -c "cat > $SYSTEMD_SERVICE_FILE" << EOF
   [Unit]
   Description=Gunicorn instance to serve expense-report-webapp
   Wants=network.target
   After=syslog.target network-online.target

   [Service]
   Type=simple
   WorkingDirectory=$WORK_DIR
   Environment="PATH=$VENV_PATH/bin"
   ExecStart=$VENV_PATH/bin/gunicorn -w 4 -b 0.0.0.0:8000 app:app
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   EOF
   ```

2. **Enable and Start the Service**

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable expense-report-webapp.service
   sudo systemctl start expense-report-webapp.service
   ```

3. **Check Service Status**
   ```bash
   systemctl status expense-report-webapp.service
   ```

## Testing and Validation

After completing the setup, test the application by accessing `http://[your-oracle-instance-ip]:8000` in a web browser. Ensure the application loads and functions as expected.

---
