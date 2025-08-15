# CI/CD Deployment Guide for Indian SM DW

## 🚀 **Recommended Approach: Automated CI/CD with GitHub Actions**

This eliminates most manual prerequisites and provides automated, reliable deployments.

## **Option 1: Full CI/CD Pipeline (Recommended)**

### Prerequisites (One-time setup):
1. A Linux server (Ubuntu 22.04+ recommended)
2. SSH access to your server
3. GitHub repository with this code

### Server Setup (One-time):
1. **Automated setup script**:
   ```bash
   # On your server, run:
   curl -fsSL https://raw.githubusercontent.com/schaitya47/indian_sm_dw/main/scripts/setup-server.sh | bash
   ```

2. **Configure GitHub Secrets**:
   Go to your GitHub repo → Settings → Secrets and variables → Actions, add:
   - `DEPLOY_HOST`: Your server IP address
   - `DEPLOY_USER`: SSH username (e.g., `ubuntu`)
   - `DEPLOY_SSH_KEY`: Your private SSH key
   - `DEPLOY_PORT`: SSH port (usually 22)

### Deployment:
- **Automatic**: Push to `main` branch → automatically deploys
- **Manual**: Go to GitHub Actions tab → Run "Deploy Indian SM DW" workflow

---

## **Option 2: Simple SSH Deployment**

If you prefer simpler setup without container registry:

### Setup GitHub Secrets:
Same as Option 1

### Deployment:
- Push to `main` branch
- GitHub Actions will SSH to your server and run:
  ```bash
  cd /srv/mage_project
  git pull
  docker compose up -d --build
  ```

---

## **Option 3: Manual Deployment (Fallback)**

If you can't use GitHub Actions:

### One-time Server Setup:
```bash
# Run the setup script
curl -fsSL https://raw.githubusercontent.com/schaitya47/indian_sm_dw/main/scripts/setup-server.sh | bash

# Edit environment variables
sudo nano /srv/mage_project/.env
# Set strong POSTGRES_PASSWORD
```

### Deploy/Update:
```bash
cd /srv/mage_project
git pull
docker compose up -d --build
```

---

## **Benefits of CI/CD Approach:**

✅ **Eliminates Manual Steps**: No more manual Docker commands
✅ **Automatic Testing**: Code is tested before deployment  
✅ **Rollback Capability**: Easy to revert to previous versions
✅ **Consistent Deployments**: Same process every time
✅ **Zero-Downtime**: Docker Compose handles rolling updates
✅ **Automated Backups**: Can be integrated into pipeline
✅ **Security**: Secrets managed by GitHub, not in code

## **Monitoring Your Deployment:**

### Check Status:
```bash
cd /srv/mage_project
docker compose ps
docker compose logs -f mage
```

### Access:
- Mage UI: `http://your-server-ip:6789`
- Postgres: `localhost:5432` (from server only)

### Backup:
```bash
# Manual backup
docker compose exec postgres pg_dump -U postgres -F c indian_sm_dw > backup_$(date +%F).dump

# Restore
docker compose exec -T postgres pg_restore -U postgres -d indian_sm_dw < backup_file.dump
```

## **Troubleshooting:**

### GitHub Actions failing:
1. Check Actions tab for error logs
2. Verify server SSH access
3. Ensure secrets are correctly set

### Deployment issues:
```bash
# Check logs
docker compose logs

# Restart services
docker compose restart

# Full restart
docker compose down && docker compose up -d
```

### Port conflicts:
```bash
# Check what's using port 5432
sudo ss -tulpn | grep :5432

# Stop PostgreSQL if running
sudo systemctl stop postgresql
```

---

## **Next Steps:**

1. **Set up GitHub Actions** (recommended)
2. **Run server setup script**
3. **Configure secrets in GitHub**
4. **Push to main branch to deploy**

This approach reduces deployment complexity from 10+ manual steps to just pushing code to GitHub! 🎉
