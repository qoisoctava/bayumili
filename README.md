# 🌬️ BayuMili

> A lightweight task scheduler dashboard built with Flask + MySQL.
> Inspired by Apache Airflow but designed for simplicity and cPanel shared hosting.

---

## 📋 Overview

BayuMili is a web-based task scheduler dashboard that allows you to:

- Schedule Python scripts using **cron expressions**
- Monitor task runs and view detailed logs
- Manage encrypted environment variables
- Receive email alerts based on task events
- Trigger tasks manually from the dashboard

---

## 🚀 Features

| Feature            | Description                                     |
| ------------------ | ----------------------------------------------- |
| 📅 Task Scheduling | Schedule Python scripts using cron expressions  |
| 📊 Dashboard       | Real-time stats and recent run history          |
| 📋 Logs Viewer     | View detailed logs for every task run           |
| 🔐 Env Vars        | Encrypted environment variable management       |
| 🔔 Alerts          | Email notifications for task events             |
| 👤 Auth            | Simple admin login with public read-only access |
| ⚙️ Scheduler       | Heartbeat-based scheduler via cPanel cron job   |

---

## 🛠️ Tech Stack

| Component  | Technology                    |
| ---------- | ----------------------------- |
| Backend    | Flask 3.0.3                   |
| Database   | MySQL + Flask-SQLAlchemy      |
| Auth       | Flask-Login                   |
| Forms      | Flask-WTF + WTForms           |
| Migration  | Flask-Migrate (Alembic)       |
| Encryption | cryptography (Fernet)         |
| Scheduler  | croniter + cPanel Cron        |
| Frontend   | Bootstrap 5 + Bootstrap Icons |
| Deployment | cPanel Passenger (WSGI)       |

---

## 📁 Project Structure

```
bayumili/
├── app/
│   ├── __init__.py         # Application factory
│   ├── extensions.py       # db, login, csrf, migrate
│   ├── utils.py            # encryption, masking, decorators
│   ├── forms.py            # WTForms form classes
│   ├── models/             # SQLAlchemy models
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── task_run.py
│   │   ├── task_log.py
│   │   ├── env_var.py
│   │   └── alert_config.py
│   ├── routes/             # Flask blueprints
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── tasks.py
│   │   ├── logs.py
│   │   ├── envs.py
│   │   ├── alerts.py
│   │   └── api.py
│   ├── scheduler/          # Scheduler engine
│   │   ├── engine.py
│   │   ├── worker.py
│   │   └── alerting.py
│   ├── templates/          # Jinja2 HTML templates
│   └── static/             # CSS, JS, images
├── scripts/                # Your Python task scripts
├── config.py               # App configuration
├── passenger_wsgi.py       # cPanel entry point
├── seed.py                 # Initial admin user seeder
├── run.py                  # Development server
├── requirements.txt
├── .env                    # Not committed to git
└── .gitignore
```

---

## ⚡ Quick Start (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/bayumili.git
cd bayumili
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key
FERNET_KEY=your-fernet-key
DB_HOST=localhost
DB_PORT=3306
DB_NAME=bayumili
DB_USER=root
DB_PASSWORD=your-password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com
```

Generate keys:

```bash
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# FERNET_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 5. Create Database

```sql
CREATE DATABASE bayumili CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run Migrations

```bash
flask --app run.py db upgrade
```

### 7. Seed Admin User

```bash
python3 seed.py
```

Default credentials:

```
Username : admin
Password : admin123
```

> ⚠️ Change the password after first login!

### 8. Run the App

```bash
python3 run.py
```

Visit `http://localhost:5000`

---

## 🔒 Access Control

| Page                    | Guest   | Admin   |
| ----------------------- | ------- | ------- |
| Dashboard               | ✅ View | ✅ View |
| Tasks List              | ✅ View | ✅ View |
| Task Detail             | ✅ View | ✅ View |
| Task Create/Edit/Delete | ❌      | ✅      |
| Task Trigger            | ❌      | ✅      |
| Logs View               | ✅ View | ✅ View |
| Env Vars                | ❌      | ✅      |
| Alerts                  | ❌      | ✅      |

---

## ⚙️ Scheduler

BayuMili uses a **heartbeat-based scheduler** [1]:

```
cPanel Cron (every 1 min)
        ↓
GET /api/scheduler/heartbeat
        ↓
Evaluate active tasks via croniter
        ↓
Execute due tasks
        ↓
Save logs + Send alerts
```

cPanel cron job command:

```
*/1 * * * * curl -s https://yourdomain.com/api/scheduler/heartbeat > /dev/null
```

---

## 📧 Alert Triggers

| Trigger              | When                        |
| -------------------- | --------------------------- |
| `on_failure`         | Task fails on any attempt   |
| `on_retry_exhausted` | All retries are used up     |
| `on_sla_breach`      | Task exceeds SLA duration   |
| `on_success`         | Task completes successfully |

---

## 🗄️ Database Models

| Model         | Description                       |
| ------------- | --------------------------------- |
| `User`        | Admin user accounts               |
| `Task`        | Scheduled task definitions        |
| `TaskRun`     | Individual task execution records |
| `TaskLog`     | Log entries per task run          |
| `EnvVar`      | Encrypted environment variables   |
| `AlertConfig` | Alert rules per task              |

---

## 🌐 Deployment (cPanel)

1. Upload files to `/home/yourusername/bayumili`
2. Create MySQL database in cPanel
3. Setup Python App via cPanel
4. Install dependencies via terminal
5. Run migrations and seed
6. Setup cron job for heartbeat [1]

See full deployment guide in [DEPLOY.md](DEPLOY.md)

---

## 📝 Log Retention

Logs are automatically cleaned up after **90 days** to save storage space.

---

## 🤝 Contributing

This is a personal portfolio project. Feel free to fork and adapt for your own use!

---

## 📄 License

MIT License — feel free to use and modify.

---

## 👤 Author

Built with ❤️ by **[Your Name]**

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your@email.com

---

> 💡 BayuMili means "owned by the wind" in Javanese —
> letting your scripts run freely on a schedule!
