import duckdb
import pandas as pd

conn = duckdb.connect()

print("="*50)
print("H&M Dataset Sampling Script")
print("Run this ONCE before anything else")
print("="*50)

# ── Step 1: Get unique customers from transactions ──────────────────
print("\n[1/5] Reading unique customer IDs from transactions...")

all_customers = conn.execute("""
    SELECT DISTINCT customer_id
    FROM read_csv_auto('data/raw/transactions_train.csv')
""").df()

print(f"      Total unique customers: {len(all_customers):,}")

# ── Step 2: Sample 15% by customer ID ──────────────────────────────
print("\n[2/5] Sampling 15% of customers (seed=42)...")

sampled_customers = all_customers.sample(frac=0.17, random_state=42)

print(f"      Sampled customers: {len(sampled_customers):,}")

# ── Step 3: Pull all transactions for sampled customers ─────────────
print("\n[3/5] Pulling transactions for sampled customers...")
print("      (This will take 3-5 minutes, please wait)")

sampled_customers.to_csv('data/processed/sampled_customer_ids.csv', index=False)

transactions = conn.execute("""
    SELECT t.*
    FROM read_csv_auto('data/raw/transactions_train.csv') t
    INNER JOIN read_csv_auto('data/processed/sampled_customer_ids.csv') s
        ON t.customer_id = s.customer_id
""").df()

print(f"      Transaction rows pulled: {len(transactions):,}")

# ── Step 4: Pull matching customer metadata ─────────────────────────
print("\n[4/5] Pulling customer metadata for sampled customers...")

customers = conn.execute("""
    SELECT c.*
    FROM read_csv_auto('data/raw/customers.csv') c
    INNER JOIN read_csv_auto('data/processed/sampled_customer_ids.csv') s
        ON c.customer_id = s.customer_id
""").df()

print(f"      Customer rows pulled: {len(customers):,}")

# ── Step 5: Save all processed files ───────────────────────────────
print("\n[5/5] Saving processed files to data/processed/...")

transactions.to_csv('data/processed/transactions_sample.csv', index=False)
customers.to_csv('data/processed/customers_sample.csv', index=False)

# Articles are small enough — copy as-is
articles = conn.execute("""
    SELECT * FROM read_csv_auto('data/raw/articles.csv')
""").df()
articles.to_csv('data/processed/articles.csv', index=False)

# ── Verification ────────────────────────────────────────────────────
print("\n" + "="*50)
print("VERIFICATION")
print("="*50)

purchases_per_customer = transactions.groupby('customer_id')['article_id'].count()
repeat_rate = (purchases_per_customer > 1).mean()

print(f"Transactions    : {len(transactions):,}")
print(f"Customers       : {len(customers):,}")
print(f"Articles        : {len(articles):,}")
print(f"Date range      : {transactions['t_dat'].min()} to {transactions['t_dat'].max()}")
print(f"Repeat rate     : {repeat_rate:.1%}  (needs to be above 30%)")
print(f"Avg purchases   : {purchases_per_customer.mean():.1f} per customer")

if repeat_rate >= 0.30:
    print("\n✓ Sample looks healthy. You are good to proceed.")
else:
    print("\n✗ Repeat rate low — flag this in your README.")

print("\nFiles saved:")
print("  data/processed/transactions_sample.csv")
print("  data/processed/customers_sample.csv")
print("  data/processed/articles.csv")
print("\nDo NOT run this script again.")
print("All future scripts read from data/processed/ only.")