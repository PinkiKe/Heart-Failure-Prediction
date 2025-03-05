import streamlit as st
import joblib
import pandas as pd
import numpy as np

# 1. 載入模型
model = joblib.load('random_forest_model.pkl')

# 2. Streamlit使用者介面
st.title("心衰竭風險評估")
st.write("請輸入以下健康參數以進行心衰竭風險評估")

# 健康參數輸入
Age = st.slider("年齡 (歲)", min_value=0, max_value=100, value=50, step=1)
Sex = st.selectbox("性別", options=["男性", "女性"])
ChestPainType = st.selectbox("胸痛類型", options=["典型心絞痛", "非典型心絞痛", "非心絞痛", "無症狀"])
RestingBP = st.number_input("靜息收縮壓 (mm Hg)", min_value=0, max_value=300, value=120)
Cholesterol = st.number_input("血清膽固醇濃度 (mm/dl)", min_value=0.0, max_value=1000.0, value=200.0, step=0.1, format="%0.1f")
FastingBS = st.selectbox("空腹血糖", options=["大於120 mg/dL", "小於、等於120 mg/dL"])
RestingECG = st.selectbox("靜止心電圖結果", options=["正常", "ST-T節段異常", "左心室肥大(LVH)"])
MaxHR = st.number_input("運動最大心率", min_value=0, max_value=300, value=120)
ExerciseAngina = st.selectbox("運動誘發的心絞痛", options=["是", "否"])
OldPeak = st.slider("ST波段下降斜率", min_value=-10.0, max_value=10.0, value=0.0, step=0.1, format="%0.1f")
ST_Slope = st.selectbox("運動期間ST波段斜率", options=["小於0", "等於0", "大於0"])

# 類別轉換數值
if Sex == "女性":
    Sex_numeric = 0
else:
    Sex_numeric = 1


if ChestPainType == "無症狀":
    ChestPainType_numeric = 0
elif ChestPainType == "非典型心絞痛":
    ChestPainType_numeric = 1
elif ChestPainType == "非心絞痛":
    ChestPainType_numeric = 2
else:
    ChestPainType_numeric = 3
    
if FastingBS == "大於120 mg/dL":
    FastingBS_numeric = 1
else:
    FastingBS_numeric = 0


if RestingECG == "左心室肥大(LVH)":
    ChestPainType_numeric = 0
elif RestingECG == "正常":
    ChestPainType_numeric = 1
else:
    ChestPainType_numeric = 2

if ExerciseAngina == "否":
    ExerciseAngina_numeric = 0
else:
    ExerciseAngina_numeric = 1

if ST_Slope == "小於0":
    ST_Slope_numeric = 0
elif ST_Slope == "等於0":
    ST_Slope_numeric = 1
else:
    ST_Slope_numeric = 2


# 3. 預測按鈕
if st.button("進行預測"):
    # 將輸入值轉換為模型可接受的格式
    input_data = np.array([[Age, Sex_numeric, ChestPainType_numeric, RestingBP, Cholesterol, FastingBS_numeric, ChestPainType_numeric, MaxHR, ExerciseAngina_numeric, OldPeak, ST_Slope_numeric]])
    
    # 模型預測
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)[:, 1][0]
# 4. 顯示結果
    if prediction[0] == 1:
        st.error(f"預測結果：高心衰竭風險！ (風險機率: {probability:.2%})")
    else:
        st.success(f"預測結果：低心衰竭風險 (風險機率: {probability:.2%})")
