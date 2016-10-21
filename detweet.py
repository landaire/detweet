#!/usr/bin/env python3

from __future__ import print_function
import argparse
import tweepy
import os
import sys
import csv
import re

ENVIRON_CONSUMER_KEY = 'CONSUMER_KEY'
ENVIRON_CONSUMER_SECRET = 'CONSUMER_SECRET'
ENVIRON_ACCESS_TOKEN = 'ACCESS_TOKEN'
ENVIRON_ACCESS_TOKEN_SECRET = 'ACCESS_TOKEN_SECRET'


def main():
    parser = argparse.ArgumentParser(description='Delete tweets en masse')
    parser.add_argument('--csv', help='the path to your tweets.csv file located in your twitter archive', required=True)
    parser.add_argument('--dry', type=bool, default=False, help='do a dry run')
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

    with open(args.csv) as csv_file:
        reader = csv.DictReader(csv_file)

        matching_tweets = []
        for row in reader:
            if tweet_matches_patterns(row['text'], args.pattern):
                matching_tweets.append(row)

        for tweet in matching_tweets:
            print(tweet['text'])


def eprint(*args, **kwargs):
    """Helper function that prints to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def tweet_matches_patterns(tweet, patterns):
    """Checks if a tweet matches a pattern
    :param tweet: tweet to search for the given pattern
    :param patterns: patterns to check against
    """

    for pattern in patterns:
        if re.search(pattern, tweet, re.IGNORECASE) is not None:
            return True

    return False


if __name__ == '__main__':
    main()
