import csv
import requests

API_ROOT = "https://aoe2.net/api/leaderboard?game=aoe2de"


def fetch_elos(leaderboard_id):
    start = 1
    count = 1000
    total = 1001

    elos = dict()

    while start <= total:
        url = f"{API_ROOT}&leaderboard_id={leaderboard_id}&start={start}&count={count}"
        resp = requests.get(url).json()
        total = resp["total"]

        for player in resp["leaderboard"]:
            player_id = player["profile_id"]
            name = player["name"]
            elo = player["rating"]

            elos[(player_id, name)] = elo

        start += count

    return elos


def fetch_tg_elos():
    return fetch_elos(4)


def fetch_solo_elos():
    return fetch_elos(3)


def join_elos(tg_elos, solo_elos):
    # Return mapping of name->(tg_elo, solo_elo)
    joined_elos = dict()

    for key, value in tg_elos.items():
        joined_elos[key] = (solo_elos.get(key, None), value)

    return joined_elos


def export_to_csv(joined_elos):
    with open("output.csv", "w") as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        for key, value in joined_elos.items():
            writer.writerow([key[0], key[1], value[0], value[1]])


def main():
    tg_elos = fetch_tg_elos()
    solo_elos = fetch_solo_elos()

    joined_elos = join_elos(tg_elos, solo_elos)

    export_to_csv(joined_elos)


if __name__ == "__main__":
    main()
