import websocket
import json
import time

start_time = time.monotonic()
current_time = time.monotonic()
cur_prise = 0.0
max_prise = 0.0


def on_open(ws):
    sub_msg = {
        "method": "SUBSCRIBE",
        "params": ["!miniTicker@arr"],
        "id": 1,
    }
    ws.send(json.dumps(sub_msg))
    print("Opened connection")
    print("\nТаймер на 1 час запущен\n")


def on_message(ws, message):
    data = json.loads(message)
    alert_prise("XRPUSDT", data)


def alert_prise(symbol, data):
    global cur_prise, max_prise, start_time, current_time

    for x in data:
        if x['s'] == symbol:
            print(x['s'] + ' ' + x['c'])
            cur_prise = float(x['c'])

            if float(x['c']) > max_prise:
                max_prise = float(x['c'])

            current_time = time.monotonic()
            if current_time - start_time >= 20:
                if max_prise - cur_prise >= max_prise * 0.00001:
                    print("\nМаксимальная цена за этот час - ", max_prise)
                    print("Текущая цена - ", cur_prise, " упала более чем на 1 %\n")
                start_time = current_time
                max_prise = cur_prise
                print("\nСброс таймера\n")


url = 'wss://fstream.binance.com/ws'

ws = websocket.WebSocketApp(url,
                            on_open=on_open,
                            on_message=on_message)

ws.run_forever()