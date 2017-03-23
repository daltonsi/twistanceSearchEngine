import tweepy
import itertools

def retrieve_tweets(screen_name):
    consumer_key = "ZWlV50x0Z4810fI9egAn1e3Qn"
    consumer_secret = "GHi5jCXpbV8j4vYfHvXRU1WAo1qTWp97f9JJcZGBgTcTMCbXp8"
    access_token = "242924072-hgfQEF73VQtcvOM95kLLWcc8Il1oozOI0GXWBjN8"
    access_token_secret = "mXP7BoVeW7bNk6OBT22nM6QZQkfNLLwplRNwbDT7XMtIh"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    alltweets = []
    ids = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    for tweet in new_tweets:
        alltweets.append(screen_name + "," + tweet.text)
    ids.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = ids[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        for tweet in new_tweets:
            alltweets.append(screen_name + "," + tweet.text)
        ids.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = ids[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    return alltweets

def main():
    tweets = [["Screen Name, Tweet"]]
    screen_names = ["altusda", "alt_fda", "ActualEPAFacts", "ungaggedEPA",
                    "Alt_CDC", "AltUSFWS", "AltHHS", "Alt_NIH", "BadHombreNPS", "NotAltWorld",
                    "AltForestServ", "RogueNASA", "Alt_NASA", "altNOAA"]
    for screen_name in screen_names:
        print(screen_name.upper())
        tweets.append(retrieve_tweets(screen_name))
    import itertools
    tweets = list(itertools.chain.from_iterable(tweets))
    thefile = open('intial_pull.csv', 'w')

    for item in tweets:
        thefile.write("%s\n" % item)

if __name__ == "__main__":
    main()