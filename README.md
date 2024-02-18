# TW Checker

Uses data from Barbarossa's TW logs to write a report on all teams that were
multi-tapped.

## Usage

``` Shell
python <tw_checker_script> <xlsx_file>
```

## Versions

Contained here are two versions of the code. The numpy version is much
less readable but runs ~10x faster.

## Requirements

- python3
- python requirements can be installed using

```Shell
python3 -m pip install -r requirements.txt
```

## Obtaining xlsx data

[GuildCommander Website](https://swgoh-guild-commander.azurewebsites.net/)
-> TWLog

## Output

Output is written in markdown which can be copy-pasted into discord for
automatic formatting.

The attacks are separated into "META" teams and "Non-META" teams. What is counted
as a meta team can be adjusted at the start of the python scripts.

The in-game unit names must be used, which can be found at the bottom of the swgoh.gg
page for that unit.

### Example Output

The following is example output from the code:

# TW Multi-tap Report :parrot:
Version: 0.0.6alpha
Date: 14 February 2024
Number active players (that set def): 44
## Our Misplays
### Non-Meta
```
[+] GenSkaar hit team BOSSK placed by FakeName : 2 times
[+] FunName hit team PHASMA placed by SillyName : 2 times
[+] Multiple player hit team MONMOTHMA placed by NoobName - FunName, GenSkaar - 3 total battles
```
### Meta (CAPITALEXECUTOR, CAPITALLEVIATHAN, CAPITALNEGOTIATOR, CAPITALPROFUNDITY, CEREJUNDA, DARTHMALGUS, EMPERORPALPATINE, GLLEIA, GLREY, JABBATHEHUTT, JEDIMASTERKENOBI, LORDVADER, THIRDSISTER)
```
[+] Multiple player hit team CAPITALEXECUTOR placed by SillyName - DumbName, MoreFakeName - 2 total battles
[+] GenSkaar hit team THIRDSISTER placed by FakeName : 2 times
```
### Enemy Misplays
```
[+] Multiple players hit team EMPERORPALPATINE placed by GenSkaar - FakeName, NoobName - 2 total battles
```
