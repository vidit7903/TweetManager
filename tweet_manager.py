import tweepy
import sqlite3
import time

# Set up your Twitter API credentials
API_KEY = 'YOUR_API_KEY'
API_SECRET_KEY = 'YOUR_API_SECRET_KEY'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

# Authenticate to Twitter
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Check if authentication was successful
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

# Function to set up the database
def setup_database():
    conn = sqlite3.connect('twitter_bot.db')
    cursor = conn.cursor()

    # Create a table to store tweets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tweet TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Function to post a tweet
def post_tweet(tweet):
    try:
        api.update_status(tweet)
        print("Tweet posted successfully")
        save_tweet_to_db(tweet)  # Save to database
    except Exception as e:
        print(f"An error occurred: {e}")

# Function to save a tweet to the database
def save_tweet_to_db(tweet):
    conn = sqlite3.connect('twitter_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO tweets (tweet) VALUES (?)', (tweet,))
    conn.commit()
    conn.close()

# Function to retrieve and display tweets from the database
def retrieve_tweets():
    conn = sqlite3.connect('twitter_bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tweets ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    
    for row in rows:
        print(f"ID: {row[0]}, Tweet: {row[1]}, Timestamp: {row[2]}")
    
    conn.close()

# Main loop to post tweets
if __name__ == "__main__":
    setup_database()  # Ensure the database and table are set up
    tweet = "Hello Twitter! This is my first tweet from my bot! #Python #TwitterBot"
    post_tweet(tweet)
    retrieve_tweets()
