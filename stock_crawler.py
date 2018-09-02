# -*- coding: utf-8 -*-
import requests
import datetime
import pandas as pd
import lxml.html

SECURITY_CODE = 1321 # 1321 日経225連動型上場投資信託
EXCEL_BOOK = "1321_from2018.xlsx"
EXCEL_SHEET = "1321_from2018"


def yahoo_url(begin_date, end_date):
    code = SECURITY_CODE
    sy = begin_date.year
    sm = begin_date.month
    sd = begin_date.day
    ey = end_date.year
    em = end_date.month
    ed = end_date.day
    return f"https://info.finance.yahoo.co.jp/history/?code={code}.T&sy={sy}&sm={sm}&sd={sd}&ey={ey}&em={em}&ed={ed}&tm=d&p=1"


def next_yahoo_url(dom):
    url = ""
    page_nodes = dom.xpath("/html/body/div/div[2]/div[2]/div[1]/ul/a");
    if page_nodes != None:
        last_node = page_nodes[-1]
        if last_node.text == "次へ":
            url = last_node.attrib["href"]
    return url


def write_excel(candles):
    # データフレームの作成
    df_ary = []
    for cnd in candles:
        str_date = cnd["date"].strftime("%Y/%m/%d")
        df = pd.DataFrame([[str_date, cnd["open"], cnd["high"], cnd["low"], cnd["close"], cnd["volume"]]])
        df_ary.append(df)
    df = pd.concat(df_ary)

    # データフレームをExcelファイルに書き込む
    df.to_excel(EXCEL_BOOK, sheet_name=EXCEL_SHEET, header=None, index=None)


def number(str):
    return int(str.replace(",", ""))


def main():
    # url取得
    url = yahoo_url(datetime.date(2018, 1, 1), datetime.date.today())

    # ローソク足取得
    candles = []
    while(len(url) > 0):
        contents = requests.get(url)
        dom = lxml.html.fromstring(contents.text)
        tr_nodes = dom.xpath("/html/body/div/div[2]/div[2]/div[1]/div[5]/table/tr")
        for node in tr_nodes:
            if node[0].tag == "th":
                continue
            cnd = {}
            cnd["date"] = datetime.datetime.strptime(node[0].text, '%Y年%m月%d日')
            cnd["open"] = number(node[1].text)
            cnd["high"] = number(node[2].text)
            cnd["low"] = number(node[3].text)
            cnd["close"] = number(node[4].text)
            cnd["volume"] = number(node[5].text)
            candles.append(cnd)
        url = next_yahoo_url(dom)

    # EXCELに書き込み
    write_excel(candles)


if __name__ == '__main__':
    main()
