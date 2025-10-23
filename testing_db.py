import duckdb

conn = duckdb.connect("scraped.ddb")
result = conn.sql("""
                  SELECT * FROM mens
""")

print(result)
