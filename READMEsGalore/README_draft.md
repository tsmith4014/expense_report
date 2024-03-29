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

So, binding to 0.0.0.0 inside the Docker container is generally safe and recommended. However, you should be careful when mapping the container's ports to the host's ports, especially when running on a host that's exposed to the internet.Below is a detailed markdown document summarizing the steps for installing Docker on Oracle Linux 8, managing Docker as a non-root user, and resolving common permissions issues, along with how to push an image to Docker Hub.

````markdown
# Docker Setup and Management on Oracle Linux 8

This guide provides step-by-step instructions for installing Docker on Oracle Linux 8, managing Docker permissions for non-root users, troubleshooting common issues, and pushing images to Docker Hub.

## Installing Docker

1. **Add the Docker Repository:**

   ```bash
   sudo dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
   ```

2. **Install Docker Engine:**

   ```bash
   sudo dnf install docker-ce docker-ce-cli containerd.io -y
   ```

3. **Start and Enable Docker:**

   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

4. **Verify Docker Installation:**

   ```bash
   docker run hello-world
   ```

   This command should run without errors, indicating Docker is correctly installed.

## Managing Docker as a Non-Root User

1. **Add Your User to the Docker Group:**

   ```bash
   sudo usermod -aG docker $USER
   ```

   This command adds your user to the `docker` group, allowing you to run Docker commands without `sudo`.

2. **Log Out and Log Back In:**

   You need to log out and log back in for the group changes to take effect.

3. **Verify Your User is in the Docker Group:**

   ```bash
   groups
   ```

   Ensure `docker` is listed in the output.

## Troubleshooting Common Docker Issues

### Permission Denied Error

If you encounter a permission denied error when trying to run Docker commands:

1. **Ensure You're in the Docker Group:**

   Double-check your user's group membership with `groups`.

2. **Restart Docker Service:**

   ```bash
   sudo systemctl restart docker
   ```

3. **Reboot Your System (If Necessary):**

   If the issue persists, a reboot might be required:

   ```bash
   sudo reboot
   ```

4. **Try Running Docker Commands Again:**

   After logging back in, test Docker without `sudo`:

   ```bash
   docker run hello-world
   ```

## Pushing an Image to Docker Hub

1. **Login to Docker Hub:**

   ```bash
   docker login
   ```

   Enter your Docker Hub username and password when prompted.

2. **Tag Your Docker Image:**

   Before pushing, tag your image with your Docker Hub username:

   ```bash
   docker tag local-image-name:tag your-dockerhub-username/repository-name:tag
   ```

3. **Push the Image to Docker Hub:**

   ```bash
   docker push your-dockerhub-username/repository-name:tag
   ```

4. **Verify the Image on Docker Hub:**

   Check your Docker Hub account to ensure the image was pushed successfully.

This guide covers the essentials for getting started with Docker on Oracle Linux 8, including installation, basic management, and interacting with Docker Hub.
````

This document should serve as a comprehensive guide for managing Docker on your Oracle Linux 8 instance. Save this content as a `.md` file for easy reference and sharing with others who might benefit from these instructions.
