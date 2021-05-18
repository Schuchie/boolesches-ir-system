# WPP2 - Gruppe 7

## Install

```sh
pip install -r requirements.txt
```

## Usage

The program is an interactive shell. Start with

```sh
python main.py
```

## Commands

```sh
search '<Query>'
```

## Info

To use Proximity Queries use a forward slash '/' and not '\\' because the "click" package parses it wrong

## Benchmarks

- Setup index: 3.41s

- Search `search '(blood OR pressure) AND cardiovascular'`: 0.001s

- Search `search '(blood OR presure) AND cardiovascular'` (with spell check): 0.011s
