import discord
import os
import tweepy
import datetime

from discord.ext import tasks, commands
from dotenv import load_dotenv
from threading import Thread

load_dotenv()
discord.http.API_VERSION=9

client = discord.Client(intents=discord.Intents.all())

TOKEN =                 os.getenv('TOKEN')
GUILD =                 os.getenv('GUILD')
API_KEY =               os.getenv('API_KEY')
API_KEY_SECRET =        os.getenv('API_KEY_SECRET')
ACCESS_TOKEN =          os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET =   os.getenv('ACCESS_TOKEN_SECRET')


auth = tweepy.OAuth1UserHandler(
    API_KEY,
    API_KEY_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET
)

channel = None
url = 'https://twitter.com/PWr_Wroclaw/status/'

@client.event
async def on_ready():
    global channel
    channel = client.get_channel(1039280597677383711)
    for guild in client.guilds:
        if guild == GUILD:
            break
    print(
        f'[*] {client.user} is succesfully connected to'
        f'\t{guild.name} -id {guild.id}'
    )
    tweet.start()
    

@tasks.loop(minutes=1)
async def tweet():
    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name='PWr_Wroclaw', count=1)

    for tweet in tweets:
        tid = tweet.id
        isTweet = determine_tweet_type(tweet._json)
        # print(isTweet)

    id = 0
    fid = '' 
    with open('tweets-ids.tweets', 'r') as file:
        fid = file.read()
        file.close()

    try:
        id = int(fid)
    except:
        None
    if str(tid) != str(id) and isTweet:
        if isTweet:
            await channel.send(url+str(tid))
        with open('tweets-ids.tweets', 'r+') as file:
            file.truncate(0)
            file.write(str(tid))
            file.close()


# https://developer.twitter.com/en/docs/tutorials/determining-tweet-types
def determine_tweet_type(tweet):
    # Check for reply indicator first
    if tweet["in_reply_to_status_id"] is not None:
        tweet_type = False
    # Check boolean quote status field and make sure it's not a RT of a Quote Tweet 
    elif tweet["is_quote_status"] is True and not tweet["text"].startswith("RT"):
        tweet_type = False
    # Check both indicators of a Retweet
    elif tweet["text"].startswith("RT") and tweet.get("retweeted_status") is not None:
        tweet_type = False
    else:
        tweet_type = True
    return tweet_type

if __name__ == '__main__':
    client.run(TOKEN)
