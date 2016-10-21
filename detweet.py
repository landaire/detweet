#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser(description='Delete tweets en masse')
    parser.add_argument('--csv', help='the path to your tweets.csv file located in your twitter archive', required=True)
    parser.add_argument('--dry', type=bool, default=False, help='do a dry run')
    parser.add_argument('keyword', help='keywords to delete', nargs='+')

    args = parser.parse_args()

    print(args.keyword)
    print(args.csv)


if __name__ == '__main__':
    main()
