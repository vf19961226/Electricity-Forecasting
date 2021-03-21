# Electricity-Forecasting
## 簡介
使用台灣電力公司提供之過去電力供需資訊搭配天氣資料以及是否為上班日，並基於長短期記憶（Long Short-Term Memory，LSTM）建立一預測模型，用以預測未來七天之電力備轉容量。
## 使用數據
除了基本的電力資料外，還使用氣象資料以及工作日資料。目標為預測未來7天之電力備轉容量，電力備轉容量為系統運轉尖峰能力減去系統瞬時負載，其中在2019年1月1日至2021年1月31日期間系統運轉尖峰能力與系統瞬時負載大致呈現M形曲線，在同一期間氣溫資料也呈現M形曲線，並且仔細觀察資料後發現工作日之系統運轉尖峰能力及系統瞬時負載明顯比非工作日高。
### 電力
* 資料來源：[台灣電力股份有限公司（台灣電力公司_過去電力供需資訊）]( https://data.gov.tw/dataset/19995)
* 時間範圍：2019年1月1日至2021年1月31日
* 說明：資料中包含台灣每日各發電廠發電量與民生、工業用電量，進而推算淨尖峰供電能力、尖峰負載、備轉容量以及備轉容率。在時間範圍中系統運轉尖峰能力與系統瞬時負載大致呈現M形曲線。  
![GITHUB](https://github.com/vf19961226/Electricity-Forecasting-DSAI-HW1-/blob/main/figure/Power.png "Power")  
### 天氣
* 資料來源：[中央氣象局（觀測資料）]( https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp)
* 時間範圍：2019年1月1日至2021年1月31日
* 地區：臺北市、新北市、桃園市、台中市、台南市、高雄市
* 說明：台灣人口約70％集中於六個直轄市中（臺北市、新北市、桃園市、臺中市、臺南市、高雄市），在六個直轄市中各取一個氣象觀測站作為代表，由北至南分別為臺北 TAIPEI （466920）、板橋 BANQIAO （466880）、中壢 Zhongli （C0C700）、臺中 TAICHUNG （467490）、臺南 TAINAN （467410）、高雄 KAOHSIUNG （467440），並依據當地人口數將氣度加權平均，取得訓練用之平均氣溫。在時間範圍中各地氣溫大致呈現M形曲線。  
![GITHUB](https://github.com/vf19961226/Electricity-Forecasting-DSAI-HW1-/blob/main/figure/Temperature.png "Temperature")
### 是否為工作日
* 資料來源：[行政院人事行政總處（中華民國政府行政機關辦公日曆表）](https://data.gov.tw/dataset/14718)
* 時間範圍：2019年（民國108年）至2021年（民國110年）
* 說明：紀錄台灣行政機關當日是否為工作日，資料中包含日期、星期、是否放假（0：否，2：是）以及備註。觀察數據後發現工作日之系統運轉尖峰能力及系統瞬時負載明顯比非工作日高。  

| Date| Supply Power| Load Power| Holiday
| --- | :---: | :---: | :---:
|20190101|26429|23872|2
|20190102|30047|28148|0
|20190103|	30343|	28452|	0
|20190104|	30301|	28490|	0
|20190105|	27957|	26054|	2
|20190106|	26950|	24617|	2
## 數據清洗
由於資料中有許多訓練時用不到的數據，故先使用[**data_processing.py**](https://github.com/vf19961226/Electricity-Forecasting-DSAI-HW1-/blob/main/data_processing.py)去除不需要的數據，並將其整合為[**training_data.csv**](https://github.com/vf19961226/Electricity-Forecasting-DSAI-HW1-/blob/main/data/training_data.csv)輸出以方便後續訓練。  
### 環境要求

| Name| Version
|:---:|---:
|Python|
|Argparse|
|Numpy|
### 命令參數

|Name|Input|Default
|:---:|---|---
|--data1|電力資料|./data/台灣電力公司_過去電力供需資訊.csv
|--data2|天氣資料所在資料夾|./data/Weather/
|--data3|辦公日曆表所在資料夾|./data/Holiday/
|--output|輸出資料位置與名稱|./data/training_data.csv
