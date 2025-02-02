from datetime import datetime
import random

import faker
import psycopg2

fake = faker.Faker()

def generate_transaction():
    user = fake.simple_profile()

    return {
        "transactionId": fake.uuid4(),
        "userId": user['username'],
        "timestamp": datetime.utcnow().timestamp(),
        "amount": round(random.uniform(10,1000),2),
        "currency": random.choice(['USD','GBP']),
        "city": fake.city(),
        "country": fake.country(),
        "merchantName": fake.company(),
        "paymentMethod": random.choice(['credit_card', 'debit_card','online_transfer']),
        "ipAddress": fake.ipv4(),
        "voucherCode": random.choice(['','DISCOUNT10','']),
        "affiliateId": fake.uuid4()
    }

def create_table(conn):
    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
            transaction_id VARCHAR(255) PRIMARY KEY,
            user_id VARCHAR(255),
            timestamp TIMESTAMP,
            amount DECIMAL,
            currency VARCHAR(255),
            city VARCHAR(255),
            country VARCHAR(255),
            merchant_name VARCHAR(255),
            payment_method VARCHAR(255),
            ip_address VARCHAR(255),
            voucher_code VARCHAR(255),
            affiliate_id VARCHAR(255)
            )
            """
        )

        conn.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"Error creating table: {e}")

    finally:
        cursor.close()

if __name__ == "__main__":
    conn = psycopg2.connect(
        host = 'localhost',
        database = 'financial_db',
        user = 'postgres',
        password = 'your_password',
        port = 5432
    )

    create_table(conn)

    transaction = generate_transaction()
    cur = conn.cursor()
    print(transaction)
    #
    # cur.execute(
    #     """
    #     INSERT INTO transactions (transaction_id, user_id, timestamp, amount, currency, city, country,
    #     merchant_name, payment_method,ip_address, voucher_code, affiliate_id
    #     )
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    #     """, (transaction["transactionId"],transaction["userId"],datetime.fromtimestamp(transaction["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
    #           transaction["amount"], transaction["currency"],transaction["city"],transaction["country"],
    #           transaction["merchantName"],transaction["paymentMethod"],transaction["ipAddress"],transaction["voucherCode"],
    #           transaction["affiliateId"])
    # )
    #
    # cur.close()
    # conn.commit()
    try:
        cur.execute(
            """
            INSERT INTO transactions (transaction_id, user_id, timestamp, amount, currency, city, country,
            merchant_name, payment_method, ip_address, voucher_code, affiliate_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (transaction["transactionId"], transaction["userId"],
             datetime.fromtimestamp(transaction["timestamp"]).strftime('%Y-%m-%d %H:%M:%S'),
             transaction["amount"], transaction["currency"], transaction["city"], transaction["country"],
             transaction["merchantName"], transaction["paymentMethod"], transaction["ipAddress"],
             transaction["voucherCode"], transaction["affiliateId"])
        )
        conn.commit()
        print("Transaction inserted successfully.")
    except Exception as e:
        print(f"Error inserting transaction: {e}")

        cur.close()
