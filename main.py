print('Preprocessing...')
import huggingface_hub as hf
hf.login('<READ_HF_TOKEN_HERE>')

import torch
import pandas as pd
import continuousintelligence as ci
from uuid import uuid4
import os



def predict_stocks(filepath: str, horizons: int, output_path: str) -> None:
    df = pd.read_csv(filepath)
    df = df.iloc[:200]
    features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    history = torch.tensor(df[features].T.values, dtype=torch.float32)
    model = ci.load_model('ContinuousIntelligence/ci-proto')
    prediction = model.forecast(history, horizon=horizons)
    fig = ci.plot_forecast(history, prediction, model.quantiles)
    for i, f in enumerate(features):
        fig.axes[i].set_title(f, fontdict={'fontsize': 24})
    fig.savefig(output_path)



def cls(): os.system('cls' if os.name == 'nt' else 'clear')
def wait(): input('\nPress "ENTER" to continue...')
def get_int_or_none(number_of: str, a: int = None, b: int = None) -> int | None:
    a = -float('inf') if a is None else a
    b =  float('inf') if b is None else b
    while True:
        q = input(f'Enter number of {number_of} (leave blank to return): ')
        if q == '': return None
        try:
            q = int(q)
        except:
            print(f'ERROR: Enter a valid integer in range [{a}, {b}]\n')
            continue
        if not a <= q <= b:
            print(f'ERROR: Enter a valid integer in range [{a}, {b}]\n')
            continue
        break
    print()
    return q


while True:
    cls()
    print('Main Menu: \n'
          ' 1 - AAPL Apple \n'
          ' 2 - MSFT Microsoft \n'
          ' 3 - NVDA Nvidia \n'
          ' 0 - Exit \n')

    match choice := input('Enter choice [1 / 2 / 3 / 0]: '):
        case '1': csv = 'AAPL'
        case '2': csv = 'MSFT'
        case '3': csv = 'NVDA'
        case '0':
            cls()
            exit()
        case _:
            print(f'\nERROR: invalid input: {choice}')
            wait()
            continue

    horizons = get_int_or_none('horizons', 1, 100)
    if horizons is None: continue
    predict_stocks(csv + '.csv', horizons, (file := csv + f'_h={horizons}_' + str(uuid4()) + '.png'))
    cls()
    print(f'Prediction figure was generated and saved to: "{file}"')
    wait()


