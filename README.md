# Electricity-Forecasting-DSAI-HW1-
## 簡介
使用台灣電力公司提供隻過去電力供需資訊搭配天氣資料以及是否為上班日，並基於長短期記憶（Long Short-Term Memory，LSTM）建立一預測模型，用以預測未來七天之電力備轉容量。
## 使用數據
除了基本的電力資料外，還使用氣象資料以及工作日資料。目標為預測未來7天之電力備轉容量，電力備轉容量為系統運轉尖峰能力減去系統瞬時負載，其中在2019年1月1日至2021年1月31日期間系統運轉尖峰能力與系統瞬時負載大致呈現M形曲線，在同一期間氣溫資料也呈現M形曲線，並且仔細觀察資料後發現工作日之系統運轉尖峰能力與系統瞬時負載比非工作日高約4000MW。
### 電力
* 資料來源：台灣電力股份有限公司（台灣電力公司_過去電力供需資訊） https://data.gov.tw/dataset/19995
* 時間範圍：2019年1月1日至2021年1月31日
* 說明：  
![GITHUB](https://github.com/vf19961226/Electricity-Forecasting-DSAI-HW1-/blob/main/figure/Power.png "Power")
### 天氣
* 資料來源：中央氣象局 https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp
* 時間範圍：2019年1月1日至2021年1月31日
* 地區：臺北市、新北市、桃園市、台中市、台南市、高雄市
* 說明：台灣人口約70％集中於六個直轄市中（臺北市、新北市、桃園市、臺中市、臺南市、高雄市），在六個直轄市中各取一個氣象觀測站作為代表，由北至南分別為臺北 TAIPEI （466920）、板橋 BANQIAO （466880）、中壢 Zhongli （C0C700）、臺中 TAICHUNG （467490）、臺南 TAINAN （467410）、高雄 KAOHSIUNG （467440），並依據當地人口數將氣度加權平均，取得訓練用之平均氣溫。  
![GITHUB](https://github.com/vf19961226/Electricity-Forecasting-DSAI-HW1-/blob/main/figure/Temperature.png "Temperature")
### 是否為工作日
* 資料來源：行政院人事行政總處（中華民國政府行政機關辦公日曆表）https://data.gov.tw/dataset/14718
* 時間範圍：2019年（民國108年）至2021年（民國110年）
* 說明：  
## 數據清洗
