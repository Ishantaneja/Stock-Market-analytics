import os

DATABASE_URL = os.getenv("postgresql://neondb_owner:npg_GVAuC4DUhLQ6@ep-soft-cake-addafwxu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

print("DATABASE_URL =", DATABASE_URL)