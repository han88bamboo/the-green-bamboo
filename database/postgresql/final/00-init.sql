-- Create the database only if it doesn't exist
CREATE EXTENSION IF NOT EXISTS dblink;
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_database
        WHERE datname = 'drinkx'
    ) THEN
        PERFORM dblink_exec('dbname=postgres', 'CREATE DATABASE drinkx');
    END IF;
END
$$;

-- Create the user only if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT FROM pg_roles
        WHERE rolname = 'drinkx'
    ) THEN
        CREATE USER drinkx WITH PASSWORD 'P@ssw0rd';
    END IF;
END
$$;

-- Connect to the newly created drinkx database
\c drinkx;

-- Grant privileges on existing tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO drinkx;

-- Connect to the newly created drinkx database
\c drinkx;

-- Grant privileges on existing tables
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO drinkx;

-- Grant privileges on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON TABLES TO drinkx;

-- Grant privileges on existing sequences
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO drinkx;

-- Grant privileges on future sequences
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON SEQUENCES TO drinkx;

-- Grant privileges on existing functions
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO drinkx;

-- Grant privileges on future functions
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL PRIVILEGES ON FUNCTIONS TO drinkx;