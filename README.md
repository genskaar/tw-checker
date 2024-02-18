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
