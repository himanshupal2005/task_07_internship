import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the existing SQLite database
db_path = "sales_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Insert some sample data into the sales table
sample_data = [
    ("2025-04-01", "Alice", "Widget", 5, 20.0),
    ("2025-04-01", "Bob", "Gadget", 3, 15.0),
    ("2025-04-02", "Alice", "Widget", 2, 20.0),
    ("2025-04-03", "Charlie", "Thingamajig", 4, 10.0),
    ("2025-04-03", "Bob", "Gadget", 1, 15.0),
    ("2025-04-04", "Dana", "Widget", 6, 20.0),
]

cursor.executemany("""
INSERT INTO sales (date, customer_name, product, quantity, price)
VALUES (?, ?, ?, ?, ?)
""", sample_data)

conn.commit()

# Query: total quantity and revenue per product
query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue 
FROM sales 
GROUP BY product
"""

# Load data into pandas DataFrame
df = pd.read_sql_query(query, conn)

# Print the DataFrame
print(df)

# Plot a bar chart of revenue by product
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.ylabel("Revenue ($)")
plt.xlabel("Product")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

# Close the database connection
conn.close()
