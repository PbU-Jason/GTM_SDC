# 使用說明

這個程式主要完成以下幾項工作：

1. 加載數據：從pickle文件中加載軌道和SAA數據。

2. 創建經緯度網格：在地球表面創建經緯度網格，用於後續的插值操作。

3. 插值數據：將SAA數據插值到經緯度網格上，以便進行可視化。

4. 繪製圖表：使用Matplotlib和Plotly繪製交互式地圖，顯示軌道、SAA數據和預測軌道。

5. 記錄軌道進入和離開SAA：識別軌道何時進入或離開SAA區域，並將軌道進入和離開SAA的時間和位置保存為CSV文件。

## 修改常量和文件路徑

- `DATA_PICKLE_SCATTER` 和 `DATA_PICKLE_CONTOUR`：這些變量指定了pickle文件的路徑，所需要的data分別存為df_for_scatter.pkl以及df_for_contour.pkl兩個檔案中。

- `GRID_X_POINTS` 和 `GRID_Y_POINTS`：這些變量控制創建經緯度網格的精度。

- `CONTOUR_LEVELS` 和 `CONTOUR_SPECIFIC_LEVEL`：這些變量控制等高線圖的級別和特定等高線的值。

## 執行完成


在執行完程式後，將獲得一個名為`interactive_map.html`的地圖和一個名為`saa_positions.csv`的CSV文件。





