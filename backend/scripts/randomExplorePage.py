# import random
# from datetime import datetime, timedelta
# from flask import Flask, request, jsonify
# # from sqlalchemy import create_engine


# app = Flask(__name__)

# # Database connection
# DATABASE_URL = "sqlite:///bottles.db"  # Replace with your actual database
# engine = create_engine(DATABASE_URL)

# def get_random_time_frame():
#     """Selects a random time frame (2 weeks or 1 month) and generates a date range."""
#     today = datetime.utcnow()
    
#     # Pick either 14 days (2 weeks)
#     duration = random.choice([14])
    
#     # Randomly choose a start date within the last 6 months
#     max_past_days = 180 
#     random_days_back = random.randint(0, max_past_days)
#     start_date = today - timedelta(days=random_days_back)
#     end_date = start_date + timedelta(days=duration)

#     return start_date, end_date

# @app.route("/explore", methods=["GET"])
# def get_explore_bottles():
#     """Fetches a random set of bottles based on a random time frame."""
#     start_date, end_date = get_random_time_frame()

#     with engine.connect() as conn:
#         query = text("""
#             SELECT * FROM bottles
#             WHERE posted_at BETWEEN :start_date AND :end_date
#             ORDER BY RANDOM()
#             LIMIT 20
#         """)
#         results = conn.execute(query, {"start_date": start_date, "end_date": end_date}).fetchall()

#     bottles = [dict(row) for row in results]
#     return jsonify(bottles)

# if __name__ == "__main__":
#     app.run(debug=True)
