import pandas as pd
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

DATA: pd.DataFrame = None

def get_closing_history(ticker_str, start)-> pd.DataFrame:
    global DATA
    if DATA is None:
        DATA = yf.download(
                    tickers=ticker_str, 
                    start=start, 
                    end=date.today(), 
                    rounding=True, 
                    progress=False
                )
    return DATA

def generate_plots()-> None:
    data: pd.DataFrame = get_closing_history("HD ^GSPC", '2023-07-24').reset_index()
    data["Date"] = data["Date"].dt.strftime('%m/%d/%Y')

    fig, axs = plt.subplots(nrows=2, ncols=1, sharex=False)
    fig.tight_layout(pad=5.0)

    axs[0].plot(data["Date"], data["Close"]["HD"], color="orange")
    axs[0].set_title(f"Home Depot Closing Prices")
    
    axs[1].plot(data["Date"], data["Close"]["^GSPC"], color="green")
    axs[1].set_title(f"S&P 500 Index Values")

    for ax in axs:
        ax.xaxis.set_major_locator(mdates.DayLocator())
        for tick in ax.get_xticklabels():
            tick.set_rotation(15)

    plt.show()

def export_to_excel()-> None:
    data: pd.DataFrame = get_closing_history("HD ^GSPC", '2023-07-24')["Close"].reset_index()
    data["Date"] = data["Date"].dt.strftime('%m/%d/%Y')

    writer = pd.ExcelWriter("home_depot_milestone2.xlsx", engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Closing Prices', index=False)
    writer._save()

if __name__ == "__main__":
    generate_plots()
    export_to_excel()