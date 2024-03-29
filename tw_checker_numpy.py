"""
Script for scouting tw logs for all double attacks.

Usage: python tw_checker.py excel_file

Genskaar

Changelog

Alpha
- Added players to guild based off of guild id (fixed to mec)
- Kelleran Beq is now meta
- Removed statement about no preloading data => no preload
- Added preload checker
- Fixed listing of names for enemy misplays
- Moved pandas to numpy for >10x speedup
- Moved pname, pname2 check for speed
- Added DTMG to META
- Change list(set(list( to list(dict( to stop reordering
- Added file output
- Split into Meta and not meta
- Initial version with black reformating
"""

import datetime
import numpy as np
import sys
import time
import pandas as pd

VERSION = "0.0.8alpha"
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
    "KELLERANBEQ",
    "LORDVADER",
    "MOFFGIDEONS3", # Dark Trooper Moff Gideon
    "THIRDSISTER",
]
OUTFILE = datetime.datetime.now().strftime("twchecker-%d-%B-%Y.dat")
PRELOADING = True
OURGUILD = "7YJBGkk8ROOFw1A1kjOACQ"

def remove_defensive_teams(d_f):
    """Remove def teams from logs.

    ARGS:
      d_f (pandas df)

    Returns
      dataframe with initial rows removed
    """
    ourplayers = []
    defensive_vals = ["Available"]
    for idx, val in enumerate(d_f.transpose()[5]):
        if not val in defensive_vals:
            n_remove = idx
            break
        ourplayers.append(d_f[idx][2])
    for row in d_f:
        if row[7] == OURGUILD:
            ourplayers.append(row[1])
    ourplayers = list(set(ourplayers))
    return d_f[n_remove:], ourplayers


def write_logfile(logs, outfile):
    """Write mistakes to logfile.

    ARGS:
        logs - list of strings to Write
        outfile - name of file to write
    """
    with open(outfile, "w", encoding="UTF-8") as ofile:
        for log in logs:
            ofile.write(log)

def get_preload_status(logs, times):
    """ Look at Locked battles to determine if preloaded.
    
    ARGS:
        logs - list of battles from tw data
        times - Number of battles there should have been
    
    Returns:
        string containing list of preloaded battles
    """
    if not PRELOADING:
        return ""
    seen_battles = [state for state in logs if state[5] == "Locked"]
    #print(times, len(seen_battles))
    if times != len(seen_battles):
        return " └─ No preloaded TM data available\n"
    outstr = f""
    #print(seen_battles)
    for itx,state in enumerate(seen_battles[:-1]):
        #print(seen_battles[itx+1][6])
        if seen_battles[itx+1][6]:
            outstr += f" └─ Battle: {itx+1} ({state[1]}) preloaded tm (but may have taken out units!)\n"
    return outstr

def get_mistakes(
    twlog,
    ourside,
):
    """Find multitaps in twlog."""
    multitaps = []
    mistakes = ""
    enemy_mistakes = ""
    our_meta_mistakes = ""
    for pname in twlog.transpose()[2]:
        for pname2 in twlog.transpose()[3]:
            if (pname, pname2) in multitaps:
                continue
            battlog = twlog[twlog[:,2] == pname]
            battlog = battlog[battlog[:,3] == pname2]
            if len(battlog) <= 2:
                continue
            # This is where multitaps happen
            if len(set(battlog.transpose()[1])) == 1:
                player = battlog[0][1]
                enemyplayer = battlog[0][2]
                leader = battlog[0][3].split(":")[0]
                times = max(battlog.transpose()[4])
                if player in (ourside):
                    preload_status = get_preload_status(battlog, times)
                    if leader not in META:
                        print(
                            f"[+] {player} hit team {leader} placed by {enemyplayer} "
                            + f": {times} times"
                        )
                        if len(preload_status) > 2:
                            print(preload_status.strip("\n"))
                        mistakes += (
                            f"[+] {player} hit team {leader} placed by"
                            + f" {enemyplayer} : {times} times\n"
                        )
                        if len(preload_status) > 2:
                            mistakes += preload_status
                    else:
                        our_meta_mistakes += (
                            f"[+] {player} hit team {leader} placed by"
                            + f" {enemyplayer} : {times} times\n"
                        )
                        if len(preload_status) > 2:
                            our_meta_mistakes += preload_status
                else:
                    enemy_mistakes += (
                        f"[+] {player} hit team {leader} placed by"
                        + f" {enemyplayer} : {times} times\n"
                    )

            if len(set(battlog.transpose()[1])) > 1:
                players = list(dict.fromkeys(battlog.transpose()[1]))
                enemyplayer = battlog[0][2]
                leader = battlog[0][3].split(":")[0]
                times = max(battlog.transpose()[4])
                if players[0] in ourside:
                    preload_status = get_preload_status(battlog, times)
                    if leader not in META:
                        print(
                            f"[+] Multiple players hit team {leader} placed by {enemyplayer}"
                            + " - "
                            + ", ".join(players)
                            + f" - {times} total battles"
                        )
                        if len(preload_status) > 2:
                            print(preload_status.strip("\n"))
                        mistakes += (
                            f"[+] Multiple players hit team {leader} placed "
                            + f"by {enemyplayer} - "
                            + ", ".join(players)
                            + f" - {times} total battles\n"
                        )
                        if len(preload_status) > 2:
                            mistakes += preload_status
                    else:
                        our_meta_mistakes += (
                            f"[+] Multiple players hit team {leader} placed "
                            + f"by {enemyplayer} - "
                            + ", ".join(players)
                            + f" - {times} total battles\n"
                        )
                        if len(preload_status) > 2:
                            our_meta_mistakes += preload_status
                else:
                    enemy_mistakes += (
                        f"[+] Multiple players hit team {leader} placed "
                        + f"by {enemyplayer} - "
                        + ", ".join(players)
                        + f" - {times} total battles\n"
                    )
            multitaps.append((pname, pname2))
    return mistakes, our_meta_mistakes, enemy_mistakes


def main():
    """Main method."""

    print("# TW Multi-tap Report :parrot:")
    print(f"Version: {VERSION}")
    print(f"Date: {datetime.datetime.now().strftime('%d %B %Y')}")
    if PRELOADING:
        print(f"Preload Checking: ENABLED - Spotted preloading recorded")

    twlog = pd.read_excel(sys.argv[1]).to_numpy()
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
