# StockPopularitySearching

## In this API server, developer provide 3 main functionalities.
### 1.get_stock_history: Calculate the how much profit you will make when following BUY AND HOLD concept on certain stock, using YahooFinance API.
    **For example, when inpt** 
        "data": [
            {"stockName": "TSLA", "payPerMonth": "2000","isDividentReinvest":"true","endDate":"2021-07-04","startDate":"2020-07-04"},
            {"stockName": "MSFT", "payPerMonth": "2000","isDividentReinvest":"true","endDate":"2021-07-04","startDate":"2020-07-04"},
            {"stockName": "QQQ", "payPerMonth": "2000","isDividentReinvest":"true","endDate":"2021-07-04","startDate":"2020-07-04"}
        ]
        
    **The API will return**
        "result": [
            {
                "cost": 19065.920013427734,
                "endDate": "2021-07-04",
                "netLiq": 22677.60040283203,
                "profit": 3611.680389404297,
                "startDate": "2020-07-04",
                "stockName": "TSLA"
            },
            {
                "cost": 22479.680068969727,
                "endDate": "2021-07-04",
                "netLiq": 27351.3603515625,
                "profit": 4871.680282592773,
                "startDate": "2020-07-04",
                "stockName": "MSFT"
            },
            {
                "cost": 21921.559967041016,
                "endDate": "2021-07-04",
                "netLiq": 25519.900512695312,
                "profit": 3598.340545654297,
                "startDate": "2020-07-04",
                "stockName": "QQQ"
            }
        ]
  
  
### 2.get_ptt_stock_comments: search comments related to specific stock name during a paticular period of time from https://www.ptt.cc/bbs/Stock/index0.html
    ** For example, enter the URL **
        http://127.0.0.1:5000/api/StockData/PTT?start_date=2021/12/31&end_date=2022/3/1&stock_name=台積電&limit=50
    ** The API will return **
        "result": {
        "2022-02-24": [
            "聰明融資台積電買好買滿",
            "明天台積電崩到飽"
        ],
        "2022-02-25": [
            "材大炒一番,安集還是台積電太陽能廠商, 下半年南科3",
            "台積電持股75%",
            "外資手上還有70%的台積電，每天賣500億要賣一年",
            "小兒把台積電當垃圾倒 丸子",
            "韭菜以為最安全的688台積電才是套牢的零股塔",
            "台積電就賣超快300億....",
            "光台積電就291E",
            "我怎麼有種外資想幫台積電省錢的感覺",
            "台積電 優質企業！",
            "禁賣台積電晶片嗎？",
            "打7.5到8折 記得烙跑。 本益比比台積電還高呢",
            "台積電  表示；；：：：：",
            "這個要死不會只有台積電會死 是大家一起死",
            "我一直覺得放空台股很危險，因為有\"台積電\"這因子",
            "應該台積電又賣了幾萬張吧 爽爽提款",
            "今天買了4張604的台積電，怎麼辦？",
            "a9940597 :今天買了4張604的台積電<--睏霸數錢啊!",
            "真的台積電跌50%你們也不敢買啦",
            "台積電調整五分鐘成交佔1/4",
            "窩台積電套牢了 明年才能畢業惹",
            "到底是烏克蘭被打還是台積電被打啊？",
            "完全不懂買台積電的人在想什麼",
            "嗚嗚  今天台股開盤後我要對台積電用手指停止線",
            "折折講台積電會受烏克蘭影響 我印象是比誰都早講",
            "台積電不會真的要對折（？",
            "台積電目前看起來只是收斂溢價而已吧？ （對照富台",
            "台積電崩爽@[email protected]",
            "看新聞在那吹台積電現在市值第幾了 就知道差不多了",
            "台積電跌4% 富台還是紅的？",
            "600元以下的台積電是天上掉下來的禮物",
            "最爛就是台積電啊  今天破年線",
            "聯電上114？那台積電至少要一千才輪得到他吧",
            "我早就說了  你早晚要回頭找台積電的",
            "何不一開始就找台積電",
            "台積電還不噴",
            "上一個主力為了吃雞排狂壓台積電 小心股版主力多",
            "不會在乎台灣，會在乎台積電",
            "你要把台積電吹死了嗎？",
            "研華下一支台積電",
            "600元以下的台積電，是老天送給你的禮物～給我買爆",
            "600元以下的台積電，是老天送給你的禮物～給我買爆",
            "空軍只爽一天 唉 550的台積電沒有了",
            "台積電生氣了",
            "台積電期貨是假的XDDDD",
            "台積電不動了...",
            "台積電好便宜，大特價的時候不買嗎哈哈哈哈哈",
            "台積電掛17000張買是假的吧",
            "全部往下 台積電往上拉七塊",
            "拜託台積電跌多一點，才好逢低買進"
        ]
    }
    
### 3.get_tele_stock_comments: search comments related to specific stock name during a paticular period of time from https://t.me/joinchat/HxXH6k2NJyU-58Iv3uLR5A
    ** For example, enter the URL **
        http://127.0.0.1:5000/api/StockData/PTT?start_date=2021/12/31&end_date=2022/3/1&stock_name=台積電&limit=50
    ** The API will return **
        "result": {
            "2022-02-08": [
                "台積電 聯電  宏捷科 ，，，，",
                "大摩喊買台積電，預期台股可看萬九 - MoneyDJ理財網\nhttps://www.moneydj.com/kmdj/news/newsviewer.aspx?a=27d06630-c736-4c83-8e0c-b3b5cede533a",
                "https://liff.line.me/1454987169-1WAXAP3K/v2/article/Gg0gVw6?utm_source=copyshare"
            ],
            "2022-02-09": [
                "https://youtu.be/v9X9Uz3oPr0",
                "台積電",
                "持股求健檢\n國巨\n華通\n台積電\n台達電\n聯茂"
            ],
            "2022-02-10": [
                "台積電 有買貴  沒買錯",
                "台積電(2330) 公布了最新營收!\n2022/1: 172,176,110仟元 \n【YoY: 35.84%】\n【MoM: 10.81%】",
                "台積電",
                "99 台積電"
            ],
            "2022-02-11": [
                "https://www.moneydj.com/kmdj/news/newsviewer.aspx?a=f64d0653-33d4-4964-982a-b3df84c6cdb1",
                "台積電: 聽說你要打台灣喔\n\n歐洲 日本 美國 : 欸幹等等 你敢打你試試看"
            ], etc