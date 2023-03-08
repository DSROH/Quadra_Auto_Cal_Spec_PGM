import pandas as pd
import Common_function as Lsi_func


def Rx_gain_average_mtm(df_Meas, Save_data_var):
    HSPA_RX_Gain = df_Meas[df_Meas["Item"].str.contains("_RX Gain ").to_list()]
    HSPA_RX_Gain_Value = HSPA_RX_Gain.iloc[:, 2:]
    HSPA_RX_Gain_Item = HSPA_RX_Gain["Item"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    HSPA_RX_Gain_Item.drop(columns=[1, 2, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    HSPA_RX_Gain_Item.columns = [
        "Band",
        "Antenna",
        "Path",
    ]

    HSPA_RX_Gain = pd.merge(HSPA_RX_Gain_Item, HSPA_RX_Gain_Value, left_index=True, right_index=True)
    HSPA_RX_Gain_Mean = round(HSPA_RX_Gain.groupby(["Band", "Antenna", "Path"]).mean(), 2)
    HSPA_RX_Gain_Data = round(
        HSPA_RX_Gain.groupby(["Band", "Antenna", "Path"]).agg(["mean", "max", "min"]),
        2,
    )
    HSPA_RX_Gain_Mean["Average"] = round(HSPA_RX_Gain_Mean.mean(axis=1), 2)

    Sub6_RX_Gain = df_Meas[df_Meas["Item"].str.contains("_Gain_Stage").to_list()]
    Sub6_RX_Gain_Value = Sub6_RX_Gain.iloc[:, 2:]
    Sub6_RX_Gain_Item = Sub6_RX_Gain["Item"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    Sub6_RX_Gain_Item.drop(columns=[3], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RX_Gain_Item.columns = ["Band", "Antenna", "Path", "Gain_Stage"]
    Sub6_RX_Gain = pd.merge(Sub6_RX_Gain_Item, Sub6_RX_Gain_Value, left_index=True, right_index=True)
    Sub6_RX_Gain_Mean = round(Sub6_RX_Gain.groupby(["Band", "Antenna", "Path", "Gain_Stage"]).mean(), 2)
    Sub6_RX_Gain_Data = round(
        Sub6_RX_Gain.groupby(["Band", "Antenna", "Path", "Gain_Stage"]).agg(["mean", "max", "min"]),
        2,
    )
    Sub6_RX_Gain_Mean["Average"] = round(Sub6_RX_Gain_Mean.mean(axis=1), 2)

    Sub6_RSRP_Offset = df_Meas[df_Meas["Item"].str.contains("_RSRP_Offset").to_list()]
    Sub6_RSRP_Offset_Value = Sub6_RSRP_Offset.iloc[:, 2:]
    Sub6_RSRP_Offset_Item = Sub6_RSRP_Offset["Item"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    Sub6_RSRP_Offset_Item.drop(columns=[3, 4], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RSRP_Offset_Item.columns = ["Band", "Antenna", "Path"]
    Sub6_RSRP_Offset = pd.merge(Sub6_RSRP_Offset_Item, Sub6_RSRP_Offset_Value, left_index=True, right_index=True)
    Sub6_RSRP_Offset_Mean = round(Sub6_RSRP_Offset.groupby(["Band", "Antenna", "Path"]).mean(), 2)
    Sub6_RSRP_Offset_Data = round(
        Sub6_RSRP_Offset.groupby(["Band", "Antenna", "Path"]).agg(["mean", "max", "min"]),
        2,
    )
    Sub6_RSRP_Offset_Mean["Average"] = round(Sub6_RSRP_Offset_Mean.mean(axis=1), 2)

    if Save_data_var.get():
        Lsi_func.Common_save_Excel("Excel_HSPA_RX_Gain.xlsx", HSPA_RX_Gain_Mean, HSPA_RX_Gain_Data)
        Lsi_func.Common_save_Excel("Excel_Sub6_RX_Gain.xlsx", Sub6_RX_Gain_Mean, Sub6_RX_Gain_Data)
        Lsi_func.Common_save_Excel("Excel_Sub6_RSRP_Offset.xlsx", Sub6_RSRP_Offset_Mean, Sub6_RSRP_Offset_Data)

    return (
        HSPA_RX_Gain_Mean["Average"],
        Sub6_RX_Gain_Mean["Average"],
        Sub6_RSRP_Offset_Mean["Average"],
    )


def Rx_2G_gain_average_mtm(df_Meas, Save_data_var):
    GSM_RX_Gain = df_Meas[df_Meas["Item"].str.contains("_RX_AGC ").to_list()]
    GSM_RX_Gain_Value = GSM_RX_Gain.iloc[:, 2:]
    GSM_RX_Gain_Item = GSM_RX_Gain["Item"].str.split("_| |\\[|\\]", expand=True)
    # 의미없는 컬럼 삭제
    GSM_RX_Gain_Item.drop(columns=[1, 2, 3, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    GSM_RX_Gain_Item.columns = ["Band"]
    GSM_RX_Gain = pd.merge(GSM_RX_Gain_Item, GSM_RX_Gain_Value, left_index=True, right_index=True)
    GSM_RX_Gain.drop_duplicates(["Band"], keep="last", inplace=True, ignore_index=True)
    GSM_RX_Gain_Mean = round(GSM_RX_Gain.groupby(["Band"]).mean(), 2)
    GSM_RX_Gain_Data = round(GSM_RX_Gain.groupby(["Band"]).agg(["mean", "max", "min"]), 2)
    GSM_RX_Gain_Mean["Average"] = round(GSM_RX_Gain_Mean.mean(axis=1), 2)

    if Save_data_var.get():
        Lsi_func.Common_save_Excel("Excel_GSM_RX_Gain.xlsx", GSM_RX_Gain_Mean, GSM_RX_Gain_Data)

    return GSM_RX_Gain_Mean["Average"]


def Rx_freq_average_mtm(df_Meas, Save_data_var):
    HSPA_RX_Freq = df_Meas[df_Meas["Item"].str.contains(" RX FREQ ").to_list()]
    HSPA_RX_Freq_Value = HSPA_RX_Freq.iloc[:, 2:]
    HSPA_RX_Freq_Item = HSPA_RX_Freq["Item"].str.split("_| |\\(|:|\\)", expand=True)
    # 의미없는 컬럼 삭제
    HSPA_RX_Freq_Item.drop(columns=[1, 2, 5, 6, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    HSPA_RX_Freq_Item.columns = ["Band", "Antenna", "Path", "Freq"]

    HSPA_RX_Freq = pd.merge(HSPA_RX_Freq_Item, HSPA_RX_Freq_Value, left_index=True, right_index=True)
    HSPA_RX_Freq_Mean = round(HSPA_RX_Freq.groupby(["Band", "Antenna", "Path", "Freq"]).mean(), 2)
    HSPA_RX_Freq_Data = round(
        HSPA_RX_Freq.groupby(["Band", "Antenna", "Path", "Freq"]).agg(["mean", "max", "min"]),
        2,
    )
    HSPA_RX_Freq_Mean["Average"] = round(HSPA_RX_Freq_Mean.mean(axis=1), 2)

    Sub6_RX_Freq_CA = df_Meas[df_Meas["Item"].str.contains("_CA1")].index
    df_Meas.drop(Sub6_RX_Freq_CA, inplace=True)
    Sub6_RX_Freq = df_Meas[df_Meas["Item"].str.contains("RX_Offset ").to_list()]
    Sub6_RX_Freq_Value = Sub6_RX_Freq.iloc[:, 2:]
    Sub6_RX_Freq_Item = Sub6_RX_Freq["Item"].str.split("\[([^]]+)\]", expand=True)
    Item1 = Sub6_RX_Freq_Item[0].str.split("_", expand=True)
    Item2 = Sub6_RX_Freq_Item[1].str.split(" ", expand=True)
    Sub6_RX_Freq_Item = pd.merge(Item1, Item2, left_index=True, right_index=True)
    # 의미없는 컬럼 삭제
    Sub6_RX_Freq_Item.drop(columns=[3, "1_y"], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RX_Freq_Item.columns = ["Band", "Antenna", "Path", "Freq"]
    Sub6_RX_Freq = pd.merge(Sub6_RX_Freq_Item, Sub6_RX_Freq_Value, left_index=True, right_index=True)
    Sub6_RX_Freq_Mean = round(Sub6_RX_Freq.groupby(["Band", "Antenna", "Path", "Freq"]).mean(), 2)
    Sub6_RX_Freq_Data = round(
        Sub6_RX_Freq.groupby(["Band", "Antenna", "Path", "Freq"]).agg(["mean", "max", "min"]),
        2,
    )
    Sub6_RX_Freq_Mean["Average"] = round(Sub6_RX_Freq_Mean.mean(axis=1), 2)

    if Save_data_var.get():
        Lsi_func.Common_save_Excel("Excel_HSPA_RX_Freq.xlsx", HSPA_RX_Freq_Mean, HSPA_RX_Freq_Data)
        Lsi_func.Common_save_Excel("Excel_Sub6_RX_Freq.xlsx", Sub6_RX_Freq_Mean, Sub6_RX_Freq_Data)

    return HSPA_RX_Freq_Mean["Average"], Sub6_RX_Freq_Mean["Average"]


def Rx_mixer_average_mtm(df_Meas, Save_data_var):
    Sub6_RX_Mixer = df_Meas[df_Meas["Item"].str.contains("_Mixer").to_list()]
    Sub6_RX_Mixer_Value = Sub6_RX_Mixer.iloc[:, 2:]
    Sub6_RX_Mixer_Item = Sub6_RX_Mixer["Item"].str.split("[_Mixer| ]", expand=True)
    # 의미없는 컬럼 삭제
    Sub6_RX_Mixer_Item.drop(columns=[1, 2, 3, 4, 5, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    Sub6_RX_Mixer_Item.columns = ["Band", "Mixer", "Path"]
    Sub6_RX_Mixer = pd.merge(Sub6_RX_Mixer_Item, Sub6_RX_Mixer_Value, left_index=True, right_index=True)
    Sub6_RX_Mixer_Mean = round(Sub6_RX_Mixer.groupby(["Band", "Mixer", "Path"]).mean(), 2)
    Sub6_RX_Mixer_Data = round(Sub6_RX_Mixer.groupby(["Band", "Mixer", "Path"]).agg(["mean", "max", "min"]), 2)
    Sub6_RX_Mixer_Mean["Average"] = round(Sub6_RX_Mixer_Mean.mean(axis=1), 2)

    if Save_data_var.get():
        Lsi_func.Common_save_Excel("Excel_Sub6_RX_Mixer.xlsx", Sub6_RX_Mixer_Mean, Sub6_RX_Mixer_Data)

    return Sub6_RX_Mixer_Mean["Average"]
