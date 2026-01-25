"""
Inserts tweets from tweets.csv one by one and reports tweets per second

"""

import csv
import time
from typing import Optional, Dict

from twitter_api import TwitterAPI
from twitter_objects import Tweet

MYSQL_USER = "root"
MYSQL_PASSWORD = "033506szh"
MYSQL_DATABASE = "twitter_db"
MYSQL_HOST = "localhost"

TWEET_CSV = "tweet.csv"
MAX_TWEETS: Optional[int] = None
PRINT_EVERY = 5000

# CSV parsing
def _norm_keys(row: Dict[str, str]) -> Dict[str, str]:
    return {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}

def extract_user_and_text(row: Dict[str, str]) -> tuple[int, str]:
    """
    Supports common header variants:
      user_id / USER_ID / userid / uid
      tweet_text / TWEET_TEXT / text / tweet / content
    """
    r = _norm_keys(row)

    user_keys = ["user_id", "userid", "uid", "user", "author_id"]
    text_keys = ["tweet_text", "text", "tweet", "content", "message", "body"]

    user_val = next((r[k] for k in user_keys if k in r and r[k] != ""), None)
    text_val = next((r[k] for k in text_keys if k in r and r[k] != ""), None)

    if user_val is None or text_val is None:
        raise ValueError(
            f"Row missing required fields. CSV headers={list(row.keys())}. "
            f"Need a user id column and a tweet text column."
        )

    return int(user_val), str(text_val)

# Main benchmark
def main():
    api = TwitterAPI(MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST)

    ok = 0
    failed = 0
    total = 0

    t0 = time.perf_counter()

    with open(TWEET_CSV, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise RuntimeError("tweet.csv has no header row (DictReader needs headers).")

        for row in reader:
            total += 1
            try:
                user_id, text = extract_user_and_text(row)
                tweet = Tweet(user_id=user_id, tweet_text=text)
                api.post_tweet(tweet)   # one-at-a-time insert
                ok += 1
            except Exception as e:
                failed += 1
                if failed <= 5:
                    print(f"[WARN] row {total} failed: {e}")

            if PRINT_EVERY and total % PRINT_EVERY == 0:
                elapsed = time.perf_counter() - t0
                cps = ok / elapsed if elapsed > 0 else 0.0
                print(f"Inserted ok={ok:,} failed={failed:,} | {cps:,.2f} calls/sec")

            if MAX_TWEETS is not None and total >= MAX_TWEETS:
                break

    elapsed = time.perf_counter() - t0
    cps = ok / elapsed if elapsed > 0 else 0.0

    print("\n=== POST_TWEET BENCHMARK RESULTS ===")
    print(f"File: {TWEET_CSV}")
    print(f"Attempted: {total:,}")
    print(f"Inserted OK: {ok:,}")
    print(f"Failed: {failed:,}")
    print(f"Elapsed: {elapsed:,.3f} sec")
    print(f"Throughput: {cps:,.2f} calls/sec")

    api.close()

if __name__ == "__main__":
    main()
