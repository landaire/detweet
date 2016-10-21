# detweet

Have some spam on your profile? Maybe an association with someone you want to get rid of? detweet allows you todelete tweets before or after a specific date that match a given regular expression.

## Usage

```
usage: detweet.py [-h] --csv CSV [--dry] [--before BEFORE] [--after AFTER]
                  pattern [pattern ...]

Delete tweets en masse

positional arguments:
  pattern          regular expressions to match

optional arguments:
  -h, --help       show this help message and exit
  --csv CSV        the path to your tweets.csv file located in your twitter
                   archive
  --dry            do a dry run
  --before BEFORE  match tweets before this date (YYYY-M-D)
  --after AFTER    match tweets after this date (YYYY-M-D)
```

### Installation

1. Clone the repository: `git clone https://github.com/landaire/detweet.git`
2. Create a python3 virtualenv: `virtualenv -p python3 venv`
3. Activate the virtualenv: `source bin/activate`
4. Install the requirements: `pip install -r requirements.txt`

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
