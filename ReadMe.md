# Overview
## stock_crawler.py
- 株価をネットから取得するpythonスクリプト
- デフォルトでは銘柄コード「1321」(日経225連動型上場投資信託)の株価を取得
- 取得項目は日単位の始値、高値、安値、終値、出来高
- 取得期間は「2018年1月1日」～「このpythonスクリプトの実行日」
- 取得結果はexcelとして保存され(ファイル名「1321_from2018.xlsx」)、保存パスは実行時のカレントディレクトリ
- コード上にある「SECURITY_CODE」の値を1321以外に変更すると他の銘柄の株価も取得可能で、取得期間も容易に変更可能

## stock_rnn_simple.py
- AIを使って株価の予測値のグラフを出力するpythonスクリプト
- ライブラリはkeras(backendはtensorflow)を使用
- 過去10日間の株価を元に、次の日(11日目)の株価を予測
- 銘柄は、銘柄コード「1321」(日経225連動型上場投資信託)の株価
- 2001年7月13日から2018年3月2日までの株価データファイル「1321-from2001.xlsx」が既にあり、このデータの9割を学習させて、残り1割で検証を実施  
- グラフについて、実際の株価が赤の破線、予測した株価が黒線


# Requirement
- Windows10
- [Anaconda3](https://www.anaconda.com/distribution/#download-section) (Python 3.7 version)


# Setup & Usage
Anaconda Prompt (Anaconda3)にてコマンド実施
## stock_crawler.py
```
> python stock_crawler.py
```

## stock_rnn_simple.py
```
> conda env create -f sampleenv.yaml
> conda activate sampleenv
> python stock_rnn_simple.py
```
