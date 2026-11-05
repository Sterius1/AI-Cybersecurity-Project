import psycopg2

# Database connection parameters matching your Docker setup
DB_PARAMS = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Sterius_", 
    "host": "localhost",
    "port": "5432"
}

def setup_database():
    try:
        # Connect to the local Docker PostgreSQL instance
        conn = psycopg2.connect(**DB_PARAMS)
        conn.autocommit = True
        cursor = conn.cursor()

        # Enable pgvector for Feature Lead 3's RAG pipeline
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("pgvector extension enabled.")

        # Table for Feature Lead 1: Vulnerability Prioritization
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id SERIAL PRIMARY KEY,
                cve_id VARCHAR(50),
                cvss_score NUMERIC(3, 1),
                asset_name VARCHAR(100),
                description TEXT
            );
        """)
        print("'vulnerabilities' table created.")

        # Table for Feature Lead 2: SIEM Alert Analyzer
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_alerts (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rule_description TEXT,
                source_ip VARCHAR(50),
                severity_level INTEGER,
                status VARCHAR(20) DEFAULT 'New'
            );
        """)
        print("'active_alerts' table created.")

        # Table for Feature Lead 3: Compliance & Policy Chatbot
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS policy_documents (
                id SERIAL PRIMARY KEY,
                document_name VARCHAR(255),
                chunk_text TEXT,
                embedding vector(768) 
            );
        """)
        print("'policy_documents' table created.")

        cursor.close()
        conn.close()
        print("Database setup complete!")

    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    setup_database()