"""

Loads users from the follows table, calls get_home_timeline repeatedly, and measures calls per second.

"""

import time
import random
from typing import Optional, List

from twitter_api import TwitterAPI

# CONFIG
MYSQL_USER = "root"
MYSQL_PASSWORD = "033506szh"
MYSQL_DATABASE = "twitter_db"
MYSQL_HOST = "localhost"

NUM_CALLS = 10000

WARMUP_CALLS = 200

MAX_USERS_TO_SAMPLE: Optional[int] = None


def get_candidate_users(api: TwitterAPI) -> List[int]:
    """
    Pick users who actually follow someone (so timeline isn't empty).
    Uses DISTINCT follower_id from follows.
    """
    df = api.dbu.execute("SELECT DISTINCT follower_id FROM follows")
    users = df["follower_id"].tolist()

    if MAX_USERS_TO_SAMPLE is not None and len(users) > MAX_USERS_TO_SAMPLE:
        users = random.sample(users, MAX_USERS_TO_SAMPLE)

    if not users:
        raise RuntimeError("No users found in follows table. Did you load follows data?")

    return users


def main():
    api = TwitterAPI(MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, MYSQL_HOST)

    users = get_candidate_users(api)

    for _ in range(WARMUP_CALLS):
        uid = random.choice(users)
        api.get_home_timeline(uid)

    t0 = time.perf_counter()
    for _ in range(NUM_CALLS):
        uid = random.choice(users)
        api.get_home_timeline(uid)
    elapsed = time.perf_counter() - t0

    cps = NUM_CALLS / elapsed if elapsed > 0 else 0.0

    print("\n=== GET_HOME_TIMELINE BENCHMARK RESULTS ===")
    print(f"Calls measured: {NUM_CALLS:,}")
    print(f"Candidate users: {len(users):,}")
    print(f"Elapsed: {elapsed:,.3f} sec")
    print(f"Throughput: {cps:,.2f} calls/sec")

    api.close()


if __name__ == "__main__":
    main()
