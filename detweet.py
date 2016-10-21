#!/usr/bin/env python3

from __future__ import print_function
from tweepy.error import TweepError
import argparse
import tweepy
import os
import sys
import csv
import re
import moment
import time

ENVIRON_CONSUMER_KEY = 'CONSUMER_KEY'
ENVIRON_CONSUMER_SECRET = 'CONSUMER_SECRET'
ENVIRON_ACCESS_TOKEN = 'ACCESS_TOKEN'
ENVIRON_ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'

DATE_FORMAT = 'YYYY-M-D'
TWEET_TIMESTAMP_FORMAT = 'YYYY-MM-DD'


def main():
    parser = argparse.ArgumentParser(description='Delete tweets en masse')
    parser.add_argument('--csv', help='the path to your tweets.csv file located in your twitter archive', required=True)
    parser.add_argument('--dry', action='store_true', default=False, help='do a dry run')
    parser.add_argument('--before', help='match tweets before this date (YYYY-M-D)')
    parser.add_argument('--after', help='match tweets after this date (YYYY-M-D)')
    parser.add_argument('pattern', help='regular expressions to match', nargs='+')

    args = parser.parse_args()

    # The consumer keys can be found on your application's Details
    # page located at https://dev.twitter.com/apps (under "OAuth settings")
    consumer_key = os.getenv(ENVIRON_CONSUMER_KEY)
    consumer_secret = os.getenv(ENVIRON_CONSUMER_SECRET)

    # The access tokens can be found on your applications's Details
    # page located at https://dev.twitter.com/apps (located
    # under "Your access token")
    access_token = os.getenv(ENVIRON_ACCESS_TOKEN)
    access_token_secret = os.getenv(ENVIRON_ACCESS_TOKEN_SECRET)

    required_environ_vars = [consumer_key, consumer_secret, access_token, access_token_secret]
    if None in required_environ_vars:
        required_environ_var_keys = [ENVIRON_ACCESS_TOKEN, ENVIRON_ACCESS_TOKEN_SECRET, ENVIRON_CONSUMER_KEY,
                                     ENVIRON_CONSUMER_SECRET]
        eprint('Missing a required environment variable. Make sure the following are set: {}'.format(
            ', '.join(required_environ_var_keys)))

        exit(1)

    # Set up tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # Parse the before/after dates if they exist
    before_date = None
    after_date = None
    if args.before is not None:
        before_date = moment.date(args.before, DATE_FORMAT)
    if args.after is not None:
        after_date = moment.date(args.after, DATE_FORMAT)

    # Read the CSV file
    matching_tweets = []
    with open(args.csv) as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            # slice the date here so that we don't bother parsing the time
            tweet_date = moment.date(row['timestamp'][:len(TWEET_TIMESTAMP_FORMAT)], TWEET_TIMESTAMP_FORMAT)

            if before_date is not None and tweet_date > before_date:
                continue

            if after_date is not None and tweet_date < after_date:
                continue

            if tweet_matches_patterns(row['text'], args.pattern):
                matching_tweets.append(row)

    # Begin doing tweet deletion
    if not args.dry:
        print('Beginning to delete tweets:\n\n')

    username = auth.get_username()
    for tweet in matching_tweets:
        print(tweet['timestamp'], 'https://twitter.com/{}/status/{}'.format(username, tweet['tweet_id']),
              tweet['text'], '\n')

        if not args.dry:
            try:
                api.destroy_status(int(tweet['tweet_id']))
            except TweepError as e:
                # Tweet with ID not found
                if e.api_code != 144:
                    raise e

            # Make 1 request every 10 seconds
            time.sleep(10)


def eprint(*args, **kwargs):
    """Helper function that prints to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def tweet_matches_patterns(tweet, patterns):
    """Checks if a tweet matches a pattern
    :param tweet: tweet to search for the given pattern
    :param patterns: patterns to check against
    """

    for pattern in patterns:
        # this could probably be optimized to use compiled patterns but that's not the bottleneck here
        if re.search(pattern, tweet, re.IGNORECASE) is not None:
            return True

    return False


if __name__ == '__main__':
    main()
