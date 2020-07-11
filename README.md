# Texas Daily Deaths from COVID-19

```bash
python main.py --do-download --window 7
```

![covid deaths vs time](https://raw.githubusercontent.com/notmatthancock/txcovid/master/example.png)


```bash
usage: main.py [-h] [--do-download] [--data-url DATA_URL]
               [--data-dir DATA_DIR] [--counties COUNTIES [COUNTIES ...]]
               [--window WINDOW]

optional arguments:
  -h, --help            show this help message and exit
  --do-download
  --data-url DATA_URL
  --data-dir DATA_DIR
  --counties COUNTIES [COUNTIES ...]
  --window WINDOW
```


### Requirements

- matplotlib
- numpy
- pandas
