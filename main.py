from binance import Client
import pandas as pd
import time

api_key = '-'
secret_key = '-'

client = Client(api_key, secret_key)


def xrp_usdt_now():
    """
    Получение данных о цене XRTUSDT в настоящий момент
    :return: float (цена XRTUSDT)
    """
    tickers = pd.DataFrame(client.get_all_tickers())
    tickers = tickers[tickers.symbol.str.contains('XRPUSDT')]
    xrp_usdt = float(tickers['price'])
    return xrp_usdt


def xrp_usdt_hour_high():
    """
    Получение максимальной цены XRTUSDT за последний час с помощью библиотеки binance и pandas
    :return: float (цена XRTUSDT макс за последний час)
    """
    frame = pd.DataFrame(client.get_klines(symbol='XRPUSDT', interval=Client.KLINE_INTERVAL_1HOUR))
    frame = frame.iloc[:, :3]
    frame.columns = ['Time', 'Open', 'High']
    frame = frame.drop(columns=['Open'])
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit='ms')
    frame = frame.tail(1)
    frame = frame.astype(float)
    high_xrt_usdt_last = frame.values[0][0]
    return high_xrt_usdt_last


def alert(xrp_usdt_now=xrp_usdt_now(), xrp_usdt_hour_high=xrp_usdt_hour_high()):
    """
    Сравнение макс цены за последний час с текущей ценой
    :param xrp_usdt_now:
    :param xrp_usdt_hour_high:
    :return:
    """
    while True:
        try:
            if xrp_usdt_now <= 0.99 * xrp_usdt_hour_high:
                print(
                    f'ВНИМАНИЕ! ПАДЕНИЕ ЦЕНЫ! Сейчас: {xrp_usdt_now}, максимум за последний час: {xrp_usdt_hour_high}')
            else:
                print(f'Цена сейчас: {xrp_usdt_now}, Максимум за последний час: {xrp_usdt_hour_high}')
            time.sleep(10)
        except:
            print('Нет данных.Повторное соединение через 10 секунд')
            time.sleep(10)
            # xrp_usdt_now = xrp_usdt_now()
            # xrp_usdt_hour_high = xrp_usdt_hour_high()


alert()
