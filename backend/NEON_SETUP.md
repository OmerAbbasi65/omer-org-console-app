# Neon PostgreSQL Setup Guide

This guide walks you through setting up a Neon PostgreSQL database for the Todo API (Phase 2 Level 1).

## What is Neon?

Neon is a serverless PostgreSQL platform that offers:
- **Serverless**: No infrastructure management
- **Auto-scaling**: Scales based on usage
- **Auto-suspend**: Pauses when inactive (cost savings)
- **Instant branching**: Create database branches for testing
- **Generous free tier**: Perfect for development

## Step 1: Create Neon Account

1. Go to https://neon.tech
2. Click "Sign Up" (free account, no credit card required)
3. Sign up with GitHub, Google, or email

## Step 2: Create a New Project

1. After logging in, click **"New Project"**
2. Configure your project:
   - **Project Name**: `todo-app` (or your preferred name)
   - **PostgreSQL Version**: 16 (recommended) or 15
   - **Region**: Choose closest to your location (e.g., US East, EU West)
3. Click **"Create Project"**

## Step 3: Get Connection String

After creating the project, you'll see the connection details:

1. **Connection String** format:
   ```
   postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
   ```

2. **Example**:
   ```
   postgresql://neondb_owner:AbCdEf123456@ep-cool-breeze-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

3. **Copy the full connection string** (you'll need this for the `.env` file)

## Step 4: Configure Backend Environment

1. Navigate to `backend/` directory:
   ```bash
   cd backend
   ```

2. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` file and paste your Neon connection string:
   ```env
   DATABASE_URL=postgresql://neondb_owner:AbCdEf123456@ep-cool-breeze-12345678.us-east-2.aws.neon.tech/neondb?sslmode=require

   API_V1_PREFIX=/api/v1
   PROJECT_NAME=Todo API
   FRONTEND_URL=http://localhost:3000
   ENVIRONMENT=development
   ```

## Step 5: Test Database Connection

1. Install backend dependencies:
   ```bash
   cd backend
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate

   pip install -r requirements.txt
   ```

2. Run the backend to test connection:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. If successful, you should see:
   ```
   🚀 Starting Todo API...
   ✅ Database tables created
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```

4. Check the database in Neon Console:
   - Go to https://console.neon.tech
   - Select your project
   - Click "Tables" tab
   - You should see the `tasks` table created

## Step 6: Verify Database Schema

1. In Neon Console, go to **SQL Editor**

2. Run this query to verify the `tasks` table:
   ```sql
   SELECT
     column_name,
     data_type,
     is_nullable
   FROM
     information_schema.columns
   WHERE
     table_name = 'tasks';
   ```

3. Expected output:
   ```
   column_name   | data_type                   | is_nullable
   --------------+-----------------------------+-------------
   id            | uuid                        | NO
   title         | character varying(200)      | NO
   description   | character varying(1000)     | YES
   completed     | boolean                     | NO
   created_at    | timestamp without time zone | NO
   updated_at    | timestamp without time zone | NO
   ```

## Neon Console Features

### 1. SQL Editor
- Run SQL queries directly
- Useful for debugging and data inspection

### 2. Database Branches
- Create instant database copies for testing
- Each branch has its own connection string
- Perfect for feature development without affecting production data

### 3. Monitoring
- View query performance
- Monitor database size and usage
- Track connection activity

### 4. Connection Pooling
- Neon automatically manages connection pooling
- No additional configuration needed

## Connection String Components

Breaking down the connection string:

```
postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
```

| Component | Description | Example |
|-----------|-------------|---------|
| `user` | Database user | `neondb_owner` |
| `password` | Database password | `AbCdEf123456` |
| `endpoint` | Neon endpoint | `ep-cool-breeze-12345678.us-east-2.aws.neon.tech` |
| `database` | Database name | `neondb` |
| `sslmode` | SSL mode (required) | `require` |

## Troubleshooting

### Error: "Could not connect to server"

**Cause**: Invalid connection string or network issue

**Solution**:
1. Verify connection string is correct (no extra spaces)
2. Check if SSL mode is set to `require`
3. Ensure you're using the correct endpoint region

### Error: "password authentication failed"

**Cause**: Incorrect password in connection string

**Solution**:
1. Go to Neon Console → Project Settings → Connection Details
2. Copy the connection string again (password may have been reset)
3. Update `.env` file with new connection string

### Error: "database does not exist"

**Cause**: Database name is incorrect

**Solution**:
1. Default Neon database name is `neondb`
2. Verify database name in Neon Console
3. Update connection string if needed

### Tables not created

**Cause**: SQLModel metadata not initialized

**Solution**:
1. Restart the FastAPI application
2. Check logs for database connection errors
3. Verify `create_db_and_tables()` is called in `app/main.py`

## Database Migrations (Future)

For Level 1, tables are auto-created on startup. For production or Level 2+, use Alembic migrations:

```bash
# Initialize Alembic (future)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add priority and tags"

# Apply migration
alembic upgrade head
```

## Security Best Practices

1. **Never commit `.env` file** to version control
   - ✅ `.env` is in `.gitignore`
   - ✅ Use `.env.example` as template

2. **Rotate database passwords** periodically
   - Go to Neon Console → Project Settings
   - Click "Reset password"
   - Update `.env` file

3. **Use separate databases** for development/production
   - Create multiple Neon projects
   - Use different connection strings per environment

4. **Enable IP restrictions** (optional, for production)
   - Go to Neon Console → Project Settings → IP Allow
   - Whitelist specific IP addresses

## Neon Free Tier Limits

As of 2026, the Neon free tier includes:
- **Storage**: 3 GB
- **Compute**: 300 hours/month
- **Branches**: 10 per project
- **Projects**: Unlimited

This is sufficient for development and small production apps.

## Next Steps

Once Neon is configured:
1. ✅ Backend should connect successfully
2. ✅ Tables are created automatically
3. ✅ Ready to test API endpoints
4. ✅ Start the frontend and test end-to-end

## Useful SQL Queries

**View all tasks**:
```sql
SELECT * FROM tasks ORDER BY created_at DESC;
```

**Count tasks by completion status**:
```sql
SELECT completed, COUNT(*) FROM tasks GROUP BY completed;
```

**Clear all tasks** (development only):
```sql
TRUNCATE TABLE tasks;
```

**Drop and recreate table** (use with caution):
```sql
DROP TABLE IF EXISTS tasks;
-- Restart backend to recreate
```

## Support

- **Neon Documentation**: https://neon.tech/docs
- **Neon Discord**: https://discord.gg/neon
- **Project Spec**: `../specs/002-todo-web-app-level1/spec.md`
