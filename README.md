# AStockBacktrader
A project base on backtrader doing research on AStock CN

命令行使用举例：

1.更新股票基础数据
python run.py -i base=True

2.更新股票日线数据
* 更新所有股票数据至最新
python run.py -d
* 更新指定股票数据
python run.py -d fromdate=20100101,todate=20200101,stock=\'sh600000\'

3.查询股票数据
python run.py -qry fromdate=20100101,todate=20200101,stock=\'sh600000\'

4.回测命令

python run.py --csvformat btcsv \
              --data ../../datas/2006-day-001.txt \
              --plot \
              --strategy :SMA_CrossOver

python run.py -c localdb \
                --stock sh600000 \
                -f 20200101 \
                -t 20210202 \
                --plot \
                --strategy :SMA_CrossOver

python3 run.py -c localdb \
                --stock sh600000 \
                --fromdate 20200101 \
                --todate 20210202 \
                -d xxx \
                --plot \
                --strategy bt/strategies/lightvolume.py:Light_Volume:printlog=True \
                -cash 20000 \
                --commission 2.0 \
                --sizer :PercentSizer:percents=20 \
                --analyzer :SharpeRatio
