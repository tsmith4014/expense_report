this is key for oracle cloud for my instance
the app will be aval at port 8000
selfs.key = key for this oracle instance
ssh -i <private_key_file> <username>@<public-ip-address>
ssh -i selfs.key opc@132.145.210.86

# Define working directory

WORK_DIR="/home/opc/expense_report" # Corrected the directory name
VENV_PATH="/home/opc/expense_report/venv"
SYSTEMD_SERVICE_FILE="/etc/systemd/system/expense-report-webapp.service"

# Update package manager with sudo

sudo yum update -y

# Install Git, Python 3.8, and Python 3.8 Development package with sudo

sudo yum install git python38 python38-devel -y

# Navigate to opc's home directory

cd /home/opc/

# Clone the Expense Report Webapp repository

git clone https://github.com/tsmith4014/expense_report.git

# Navigate to the cloned repository

cd $WORK_DIR

# Install Python-Pip with sudo

sudo yum install python3-pip -y

# Edit requirements.txt to include gunicorn

echo "gunicorn" >> requirements.txt

# Create a Python virtual environment using Python 3.8

python3.8 -m venv venv

# Activate the virtual environment

source $VENV_PATH/bin/activate

# Install Python dependencies

pip install -r requirements.txt

# Create Gunicorn config file

echo "bind = '0.0.0.0:8000'
workers = 4" > gunicorn_config.py

# Create systemd service file with sudo

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

# Reload systemd daemon with sudo

sudo systemctl daemon-reload

# Enable the service with sudo

sudo systemctl enable expense-report-webapp.service

# Start the service with sudo

sudo systemctl start expense-report-webapp.service

# Checking the service status doesn't require sudo

systemctl status expense-report-webapp.service

## Troubleshooting

### SELinux Configuration

- If encountering issues related to SELinux (like inability to execute scripts), check SELinux status:
  ```bash
  sestatus
  ```
- Temporarily set SELinux to permissive:
  ```bash
  sudo setenforce 0
  ```
- Try starting the service again:
  ```bash
  sudo systemctl start expense-report-webapp.service
  ```

### Service Failure

- Check systemd service logs for errors:
  ```bash
  sudo journalctl -u expense-report-webapp.service
  ```
- Verify the Gunicorn executable path in the service file.

### Dependency Issues

- If Python packages fail to install, check for missing dependencies:
  ```bash
  sudo yum install python38-devel
  ```

## Application Updates

- Restart the application service:
  ```bash
  sudo systemctl restart expense-report-webapp.service
  ```

---
