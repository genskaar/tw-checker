"""
Script for scouting tw logs for all double attacks.

Usage: python tw_checker.py excel_file

Genskaar

Changelog

Alpha
- Moved pname, pname2 check for speed
- Added DTMG to META
- Change list(set(list( to list(dict( to stop reordering
- Added file output
- Split into Meta and not meta
- Initial version with black reformating
"""

import datetime
import sys
import time
import pandas as pd

VERSION = "0.0.5alpha"
META = [
    "CAPITALEXECUTOR",
    "CAPITALLEVIATHAN",
    "CAPITALNEGOTIATOR",
    "CAPITALPROFUNDITY",
    "CEREJUNDA",
    "DARTHMALGUS",
    "EMPERORPALPATINE",
    "GLLEIA",
    "GLREY",
    "JABBATHEHUTT",
    "JEDIMASTERKENOBI",
    "LORDVADER",
    "MOFFGIDEONS3", # Dark Trooper Moff Gideon
    "THIRDSISTER",
]
OUTFILE = datetime.datetime.now().strftime("twchecker-%d-%B-%Y.dat")

def remove_defensive_teams(d_f):
    """Remove def teams from logs.

    ARGS:
      d_f (pandas df)

    Returns
      dataframe with initial rows removed
    """
    ourplayers = []
    defensive_vals = ["Available"]
    for idx, val in enumerate(d_f["Squad Status"]):
        if not val in defensive_vals:
            n_remove = idx
            break
        ourplayers.append(d_f["Log by"][idx])
    ourplayers = list(set(ourplayers))
    d_f.drop(index=d_f.index[:n_remove], axis=0, inplace=True)
    return d_f, ourplayers


def write_logfile(logs, outfile):
    """Write mistakes to logfile.

    ARGS:
        logs - list of strings to Write
        outfile - name of file to write
    """
    with open(outfile, "w", encoding="UTF-8") as ofile:
        for log in logs:
            ofile.write(log)


def get_mistakes(
    twlog,
    ourside,
):
    """Find multitaps in twlog."""
    multitaps = []
    mistakes = ""
    enemy_mistakes = ""
    our_meta_mistakes = ""
    for pname in twlog["Player Name"]:
        for pname2 in twlog["Squad Leader"]:
            if (pname, pname2) in multitaps:
                continue
            battlog = twlog[
                (twlog["Player Name"] == pname) & (twlog["Squad Leader"] == pname2)
            ]
            if len(battlog) <= 2:
                continue
            # This is where multitaps happen
            if len(set(battlog["Log by"])) == 1:
                player = list(battlog["Log by"])[0]
                enemyplayer = list(battlog["Player Name"])[0]
                leader = list(battlog["Squad Leader"])[0].split(":")[0]
                times = max(list(battlog["Successful Defends"]))
                if str(list(battlog["Log by"])[0]) in (ourside):
                    if leader not in META:
                        print(
                            f"[+] {player} hit team {leader} placed by {enemyplayer} "
                            + f": {times} times"
                        )
                        mistakes += (
                            f"[+] {player} hit team {leader} placed by"
                            + f" {enemyplayer} : {times} times\n"
                        )
                    else:
                        our_meta_mistakes += (
                            f"[+] {player} hit team {leader} placed by"
                            + f" {enemyplayer} : {times} times\n"
                        )

                else:
                    enemy_mistakes += (
                        f"[+] {player} hit team {leader} placed by"
                        + f" {enemyplayer} : {times} times\n"
                    )
            if len(set(battlog["Log by"])) > 1:
                players = list(dict.fromkeys((battlog["Log by"])))
                enemyplayer = list(battlog["Player Name"])[0]
                leader = list(battlog["Squad Leader"])[0].split(":")[0]
                times = max(list(battlog["Successful Defends"]))
                if str(list(battlog["Log by"])[0]) in (ourside):
                    if leader not in META:
                        print(
                            f"[+] Multiple player hit team {leader} placed by {enemyplayer}"
                            + " - "
                            + ", ".join(players)
                            + f" - {times} total battles"
                        )
                        mistakes += (
                            f"[+] Multiple player hit team {leader} placed "
                            + f"by {enemyplayer} - "
                            + ", ".join(players)
                            + f" - {times} total battles:\n"
                        )
                    else:
                        our_meta_mistakes += (
                            f"[+] Multiple player hit team {leader} placed "
                            + f"by {enemyplayer} - "
                            + ", ".join(players)
                            + f" - {times} total battles:\n"
                        )
                else:
                    enemy_mistakes += (
                        f"[+] Multiple player hit team {leader} placed "
                        + f"by {enemyplayer} - {times} total battles:\n"
                    )
            multitaps.append((pname, pname2))
    return mistakes, our_meta_mistakes, enemy_mistakes


def main():
    """Main method."""

    print("# TW Multi-tap Report :parrot:")
    print(f"Version: {VERSION}")
    print(f"Date: {datetime.datetime.now().strftime('%d %B %Y')}")

    twlog = pd.read_excel(sys.argv[1])
    twlog, ourside = remove_defensive_teams(twlog)

    print(f"Number active players (that set def): {len(ourside)}")
    print("## Our Misplays")

    print("### Non-Meta")
    print("```")
    start_time = time.time()
    mistakes, our_meta_mistakes, enemy_mistakes = get_mistakes(twlog, ourside)
    print("```")

    print(f"### Meta ({', '.join(META)})")
    print("```")
    print(our_meta_mistakes)
    print("```")

    print("### Enemy Misplays")
    print("```")
    print(enemy_mistakes)
    print("```")

    end_time = time.time()
    print(f"Total time: {end_time-start_time} seconds")

    write_logfile(
        ["US\n", mistakes, "META\n", our_meta_mistakes, "THEM\n", enemy_mistakes],
        OUTFILE,
    )
    print(f"[+] Wrote output to {OUTFILE}")


main()
