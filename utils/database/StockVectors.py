import psycopg2


def store_vector(Chunks, embeddings,dbname,user,host,password,port):
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        host=host,
        password=password,
        sslmode='require',
        port=port
    )

    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS docs(
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(384)
    );
    """)

    conn.commit()
    data = list(zip(Chunks, embeddings))

    cur.executemany(
        """
        INSERT INTO docs (content, embedding)
        VALUES (%s, %s)
        """,
        data
    )

    conn.commit()

    cur.execute("""
    CREATE INDEX ON docs
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
    """)

    conn.commit()

    cur.execute("ANALYZE docs;")
    conn.commit()
    conn.close()

    print("Data stored successfully in the database.")