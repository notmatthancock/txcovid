import argparse
import datetime
import os
import pathlib
import ssl
import urllib

import matplotlib.pyplot as plt
import numpy as np
import pandas
from pandas.plotting import register_matplotlib_converters


DEFAULT_DATA_URL = "https://dshs.texas.gov/coronavirus/TexasCOVID19DailyCountyFatalityCountData.xlsx"
EXCEL_NAME = pathlib.Path(DEFAULT_DATA_URL)


def download(url, path):
    print(f'Downloading latest data to {path}')
    context = ssl._create_unverified_context()
    response = urllib.request.urlopen(url, context=context)
    with open(path, 'wb') as f:
        f.write(response.read())


def read_excel(path):
    data_frame = pandas.read_excel(
        io=path,
        index_col=[0, 1],
        header=2,
        skipfooter=10,
    )
    dates = []
    for column in data_frame.columns:
        month, day = map(int, column.split(' ')[1].split('/'))
        date = datetime.date(2020, month, day)
        dates.append(date)
    deaths = {
        county: row_series.values
        for (county, _), row_series in data_frame.iterrows()
    }
    return dates, deaths


if __name__ == '__main__':
    register_matplotlib_converters()

    parser = argparse.ArgumentParser()
    parser.add_argument('--do-download', default=False, action='store_true')
    parser.add_argument('--data-url', default=DEFAULT_DATA_URL)
    parser.add_argument('--data-dir', default='.')
    parser.add_argument('--counties', nargs='+')
    parser.add_argument('--window', default=5, type=int)
    args = parser.parse_args()

    file_name = pathlib.Path(args.data_url).name
    file_path = pathlib.Path(args.data_dir) / file_name

    if args.do_download or not file_path.exists():
        if file_path.exists():
            os.remove(file_path)
        download(url=args.data_url, path=file_path)

    dates, deaths = read_excel(file_path)

    if args.counties is None:
        deaths = np.sum([data for data in deaths.values()], axis=0)
    else:
        deaths = np.sum([deaths[county] for county in args.counties], axis=0)

    daily_deaths = np.r_[0, np.diff(deaths)]
    as_series = pandas.Series(daily_deaths)
    rolling_mean = as_series.rolling(args.window).mean().values
    rolling_std = as_series.rolling(args.window).std().values

    plt.fill_between(
        dates,
        rolling_mean - rolling_std,
        rolling_mean + rolling_std,
        alpha=0.5,
        color='0.7',
        label=f'{args.window} day \u00b1 std dev',
    )
    plt.plot(dates, daily_deaths, 'o', c='0.3',
             label='Daily Count')
    plt.plot(dates, rolling_mean, '-', c='0.3',
             label=f'{args.window} day average')

    plt.xticks(rotation=45)
    plt.ylabel('Daily Deaths')
    plt.grid(ls=':')
    plt.legend()
    plt.tight_layout()
    plt.show()
