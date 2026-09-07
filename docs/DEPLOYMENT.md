# CareerPilot AI — Production Deployment Guide

This guide provides end-to-end instructions for deploying CareerPilot AI in production across multiple deployment targets.

---

## Architecture Topology in Production

```
+--------------------------------------------------------------------------------+
|  CLIENT: Next.js 14 Frontend (Vercel / AWS Amplify / Container Port 3000)      |
+---------------------------------------+----------------------------------------+
                                        | HTTPS / WSS
                                        v
+--------------------------------------------------------------------------------+
|  BACKEND: FastAPI API Gateway (Render / Railway / OCI / Fly.io / Port 8000)    |
+-------------------+--------------------+-------------------+-------------------+
                    |                    |                   |
                    v                    v                   v
            [PostgreSQL 16]     [pgvector 0.7+]       [Oracle AI 23ai]
            (Managed Database / Supabase / Neon / OCI Autonomous Database)
```

---

## Option 1: One-Click Docker Compose Deployment (VPS, AWS EC2, OCI VM, DigitalOcean)

This option deploys the Next.js Frontend, FastAPI Backend, and PostgreSQL with pgvector together using Docker Compose.

### Step 1: Provision your Virtual Server
- Provision an Ubuntu 22.04 LTS / 24.04 server (minimum 2 vCPU, 4GB RAM).
- Install Docker & Docker Compose:
  ```bash
  sudo apt-get update
  sudo apt-get install -y docker.io docker-compose-v2
  sudo systemctl enable --now docker
  ```

### Step 2: Clone and Configure Environment
```bash
git clone https://github.com/your-username/careerpilot-ai.git
cd careerpilot-ai

# Copy production environment configuration
cp .env.example .env
```

Edit `.env` with production credentials:
```bash
ENVIRONMENT=production
SECRET_KEY=generate-a-random-64-character-secret-key
POSTGRES_USER=careerpilot_admin
POSTGRES_PASSWORD=your_secure_db_password
POSTGRES_DB=careerpilot_production

DATABASE_URL=postgresql+asyncpg://careerpilot_admin:your_secure_db_password@postgres:5432/careerpilot_production
SYNC_DATABASE_URL=postgresql://careerpilot_admin:your_secure_db_password@postgres:5432/careerpilot_production

LLM_PROVIDER=gemini
LLM_API_KEY=your_google_gemini_api_key
LLM_MODEL=gemini-1.5-pro

FRONTEND_URL=https://your-domain.com
BACKEND_URL=https://api.your-domain.com
```

### Step 3: Build and Run Containers
```bash
docker compose up -d --build
```

### Step 4: Configure Nginx & SSL (Certbot)
Install Nginx and Let's Encrypt SSL:
```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

Configure `/etc/nginx/sites-available/careerpilot`:
```nginx
server {
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

server {
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable and secure:
```bash
sudo ln -s /etc/nginx/sites-available/careerpilot /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
sudo certbot --nginx -d your-domain.com -d api.your-domain.com
```

---

## Option 2: Managed Cloud Platform (Vercel + Render/Railway + Supabase/Neon)

This serverless architecture delivers maximum availability with zero DevOps overhead.

### Step 1: Database (Supabase or Neon with pgvector)
1. Create a project on [Supabase](https://supabase.com) or [Neon](https://neon.tech).
2. Enable `pgvector` in the SQL Editor:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
3. Copy the Connection Pooler and Direct Connection strings.

---

### Step 2: Deploy Backend to Render or Railway

#### On Render:
1. Create a **New Web Service** pointing to your GitHub repository.
2. Configure:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Add Environment Variables:
   - `ENVIRONMENT`: `production`
   - `SECRET_KEY`: `<Your 64-character secret>`
   - `DATABASE_URL`: `postgresql+asyncpg://<user>:<password>@<host>:5432/<db>`
   - `SYNC_DATABASE_URL`: `postgresql://<user>:<password>@<host>:5432/<db>`
   - `LLM_PROVIDER`: `gemini`
   - `LLM_API_KEY`: `<Your Gemini Key>`
   - `FRONTEND_URL`: `https://your-frontend.vercel.app`
4. Deploy Service and copy your backend URL (e.g. `https://careerpilot-api.onrender.com`).

---

### Step 3: Deploy Frontend to Vercel
1. Go to [Vercel](https://vercel.com) and click **Add New Project**.
2. Select your repository.
3. Set **Root Directory** to `frontend`.
4. Add Environment Variable:
   - `NEXT_PUBLIC_API_URL`: `https://careerpilot-api.onrender.com/api/v1`
5. Click **Deploy**.

---

## Option 3: Oracle Cloud Infrastructure (OCI) Deployment

1. **OCI Compute / Container Instances**:
   - Run the backend container on an OCI Ampere A1 or E4 Compute instance.
2. **Oracle AI Database 23ai / Autonomous AI Database**:
   - Enable Oracle AI Vector Search.
   - Set in backend environment:
     ```bash
     ORACLE_ENABLED=true
     ORACLE_USER=admin
     ORACLE_PASSWORD=YourPassword
     ORACLE_DSN=your_autonomous_db_high
     ```

---

## Post-Deployment Verification Checklist

1. [ ] Health Check: Navigate to `https://api.your-domain.com/api/v1/health` and verify `{"status": "healthy"}`.
2. [ ] User Flow: Register a new account, upload a resume, and verify deterministic score calculation.
3. [ ] RAG Search: Ingest a document and confirm vector similarity search returns grounded citations.
4. [ ] Mock Interview: Execute a 3-question adaptive session and confirm report generation.
