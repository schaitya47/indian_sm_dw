# GCP Deployment Steps 
- Create VM (Compute Engine)
- e2-medium-2 (2 vCPUs, 4 GB Memory)
- Ubuntu 22.04 LTSp Steps 
- Create VM (Compoute Engine)
- e2-medium-2 (2 vCPUs, 4 GB Memory)
- Ubuntu 22.04 LTS
- 50Gb Space (Balance persistent)
- Setup network_tags: mage-server (This will be used for creating firewall rules to allow external traffic)
- Allow full access to all cloud APIs (under security). This will ensure that you can run the gcloud cmd using the terminal. For better security you can use IAM and SSH based access
- After creation save your instance name it'll used further

## Prerequisites
- GCP account with billing enabled
- Basic familiarity with Linux commands
- Your public IP address (find using: `curl ifconfig.me`)

# Steps once you login to terminal using browser
- sudo apt-get update && sudo apt-get upgrade -y
- curl -fsSL https://get.docker.com -o get-docker.sh
- sudo sh get-docker.sh
- Clone the repo's docker_devlop branch (git clone -b docker_devlop https://github.com/schaitya47/indian_sm_dw.git)
- cd indian_sm_dw
- mv .env.example .env
- vi .env (edit your file and setup the creds)
- sudo docker compose up --build

## Firewall Configuration

- If you skipped creating network tags use this command to create them: 
    - gcloud compute instances add-tags <instance_name> \
    --zone=<instance_zone/location> \
    --tags=mage-server

- gcloud compute firewall-rules create allow-postgres-5432 \
    --project=indian-sm-dw \
    --network=default \
    --action=ALLOW \
    --rules=tcp:5432 \
    --source-ranges=<YOUR_PUBLIC_IP>/32 \
    --target-tags=mage-server \
    --direction=INGRESS \
    --priority=1000

- gcloud compute firewall-rules create allow-mage-6789 \
    --project=indian-sm-dw \
    --network=default \
    --action=ALLOW \
    --rules=tcp:6789 \
    --source-ranges=<YOUR_PUBLIC_IP>/32 \
    --target-tags=mage-server \
    --direction=INGRESS \
    --priority=1000

## Accessing Your Services
- Mage AI: `http://<EXTERNAL_IP>:6789`
- PostgreSQL: Connect using host `<EXTERNAL_IP>:5432`

**Note**: Replace `<YOUR_PUBLIC_IP>`, `<instance_name>`, `<instance_zone>`, and `<EXTERNAL_IP>` with your actual values.

# Instance Scheduling
- You can easily schedule your instance up and down using gcloud instance schedules
- It helps in reducing your cost.

## Troubleshooting
- Check container logs: `sudo docker compose logs`
- Restart services: `sudo docker compose restart`
- Check firewall rules: `gcloud compute firewall-rules list`

## Access your instance remotely
- https://cloud.google.com/sdk/docs/install#linux -- Install gcloud cli