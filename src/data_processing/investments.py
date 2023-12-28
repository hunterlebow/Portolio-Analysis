def read_tickers():
    with open("data/investment_tickers.txt", 'r') as file:
        tickers = file.readlines()

    # Optionally, strip the newline characters from each ticker
    tickers = [ticker.strip() for ticker in tickers]

    return tickers
