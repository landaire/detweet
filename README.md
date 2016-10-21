# detweet

Have some spam on your profile? Maybe an association with someone you want to get rid of? detweet allows you todelete tweets before or after a specific date that match a given regular expression.

## Usage

### Set up your API credentials

1. Create an application for use with this script (https://dev.twitter.com/apps)
2. Get your client token/secret and access token/token secret
3. Create a credentials file containing:

```
export CONSUMER_KEY=''
export CONSUMER_SECRET=''
export ACCESS_TOKEN=''
export ACCESS_TOKEN_SECRET=''
```

Replace the empty strings with their respective values.

In your terminal run:

```
source credentials
```

### Example run

```
$ ./detweet.py --csv ~/Downloads/tweeter_archive/tweets.csv --before '2014-06-01' 'some(thing)?' 'maybe a swear here'
```
