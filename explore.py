import duckdb

conn = duckdb.connect()

# --- TRANSACTIONS ---
print("=== TRANSACTIONS ===")
df_trans = conn.execute("""
    SELECT *
    FROM read_csv_auto('data/raw/transactions_train.csv')
    LIMIT 5
""").df()
print(df_trans)

trans_count = conn.execute("""
    SELECT COUNT(*) FROM read_csv_auto('data/raw/transactions_train.csv')
""").fetchone()[0]
print(f"Transaction rows: {trans_count:,}")

# --- CUSTOMERS ---
print("\n=== CUSTOMERS ===")
df_cust = conn.execute("""
    SELECT *
    FROM read_csv_auto('data/raw/customers.csv')
    LIMIT 5
""").df()
print(df_cust)

cust_count = conn.execute("""
    SELECT COUNT(*) FROM read_csv_auto('data/raw/customers.csv')
""").fetchone()[0]
print(f"Customer rows: {cust_count:,}")

# --- ARTICLES ---
print("\n=== ARTICLES ===")
art_count = conn.execute("""
    SELECT COUNT(*) FROM read_csv_auto('data/raw/articles.csv')
""").fetchone()[0]
print(f"Article rows: {art_count:,}")
