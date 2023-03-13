import os
import tkinter as tk
import pandas as pd

import tkinter.messagebox as msgbox

import Common_function as func
import LSI_cable as L_cable
import LSI_mtm as mtm
import LSI_et as L_et
import LSI_sub6 as L_sub6
import LSI_2g as L_2g
import LSI_3g as L_3g


def daseul_cable_average(df_Meas, Save_data_var):
    df_CableCheck = df_Meas[df_Meas["Test Conditions"].str.contains("CableCheck_").to_list()]
    df_CableCheck_Value = df_CableCheck.iloc[:, 2:]
    # New_String = re.split("[_=,\n]", line)
    df_CableCheck_Item = df_CableCheck["Test Conditions"].str.split("_| |\[MHz]|CH", expand=True)
    # 의미없는 컬럼 삭제
    df_CableCheck_Item.drop(columns=[0, 5, 6, 7, 8, 9], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_CableCheck_Item.columns = ["RAT", "Band", "Path", "CH_MHz"]
    df_CableCheck = pd.merge(df_CableCheck_Item, df_CableCheck_Value, left_index=True, right_index=True)
    df_CableCheck_Mean = round(df_CableCheck.groupby(["RAT", "Band", "Path", "CH_MHz"]).mean(), 1)
    df_CableCheck_Data = round(
        df_CableCheck.groupby(["RAT", "Band", "Path", "CH_MHz"]).agg(["mean", "max", "min"]),
        2,
    )
    df_CableCheck_Mean["Average"] = round(df_CableCheck_Mean.mean(axis=1), 1)

    if Save_data_var.get():
        filename = "Excel_CableCheck_Average.xlsx"
        func.Common_save_Excel(filename, df_CableCheck_Mean, df_CableCheck_Data)
        func.WB_Format(filename, 2, 5, 0)

    return df_CableCheck_Mean["Average"]


def daseul_rx_average(df_Meas, Save_data_var):

    PRX_Gain_2G, Ripple_2G = daseul_2g_rx_average(df_Meas)

    (
        PRX_Gain_3G,
        df_PRX_Gain_3G_mean,
        df_PRX_Gain_3G_data,
        PRX_Comp_3G,
        df_PRX_Comp_3G_mean,
        df_PRX_Comp_3G_data,
    ) = daseul_3G_rx_average(df_Meas)

    (
        RXGain_sub6,
        df_PRX_Gain_sub6_mean,
        df_PRX_Gain_sub6_data,
        RXRSRP_sub6,
        df_PRX_RSRP_sub6_mean,
        df_PRX_RSRP_sub6_data,
        RXComp_sub6,
        df_PRX_Comp_sub6_mean,
        df_PRX_Comp_sub6_data,
    ) = daseul_sub6_rx_average(df_Meas)

    if Save_data_var.get():
        filename = "Excel_RXCal.xlsx"
        with pd.ExcelWriter(filename) as writer:
            PRX_Gain_2G.to_excel(writer, sheet_name="PRX_Gain_2G")
            Ripple_2G.to_excel(writer, sheet_name="Ripple_2G")
            df_PRX_Gain_3G_mean.to_excel(writer, sheet_name="PRX_Gain_3G_mean")
            df_PRX_Gain_3G_data.to_excel(writer, sheet_name="PRX_Gain_3G_data")
            df_PRX_Comp_3G_mean.to_excel(writer, sheet_name="PRX_Comp_3G_mean")
            df_PRX_Comp_3G_data.to_excel(writer, sheet_name="PRX_Comp_3G_data")
            df_PRX_Gain_sub6_mean.to_excel(writer, sheet_name="PRX_Gain_sub6_mean")
            df_PRX_Gain_sub6_data.to_excel(writer, sheet_name="PRX_Gain_sub6_data")
            df_PRX_RSRP_sub6_mean.to_excel(writer, sheet_name="PRX_RSRP_sub6_mean")
            df_PRX_RSRP_sub6_data.to_excel(writer, sheet_name="PRX_RSRP_sub6_data")
            df_PRX_Comp_sub6_mean.to_excel(writer, sheet_name="PRX_Comp_sub6_mean")
            df_PRX_Comp_sub6_data.to_excel(writer, sheet_name="PRX_Comp_sub6_data")
        func.WB_Format(filename, 2, 5, 0)

    return PRX_Gain_2G, Ripple_2G, PRX_Gain_3G, PRX_Comp_3G, RXGain_sub6, RXRSRP_sub6, RXComp_sub6


def gsm_average(df_Meas, Save_data_var):

    df_gmsk = df_Meas[df_Meas["Test Conditions"].str.contains("CH_GMSK_").to_list()]
    df_gmsk_Value = df_gmsk.iloc[:, 2:]
    df_gmsk_Item = df_gmsk["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_gmsk_Item.drop(columns=[1, 2, 5, 7, 8, 9, 10, 11], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_gmsk_Item.columns = ["Band", "Type", "Gain", "Index"]
    df_gmsk_Item = df_gmsk_Item.replace(
        {"Band": {"GSM850": "G085", "GSM900": "G09", "DCS1800": "G18", "PCS1900": "G19"}}
    )
    df_gmsk = pd.merge(df_gmsk_Item, df_gmsk_Value, left_index=True, right_index=True)
    df_null = df_gmsk[df_gmsk["Index"].isnull()].index
    df_gmsk.drop(df_null, inplace=True)
    df_gmsk_Mean = round(df_gmsk.groupby(["Band", "Type", "Gain", "Index"], sort=False).mean(), 1)
    df_gmsk_Mean["Average"] = round(df_gmsk_Mean.mean(axis=1), 1)

    df_gmsk_TxL = df_Meas[df_Meas["Test Conditions"].str.contains("CH_GMSK_TxL").to_list()]
    df_gmsk_TxL_Value = df_gmsk_TxL.iloc[:, 2:]
    df_gmsk_TxL_Item = df_gmsk_TxL["Test Conditions"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    df_gmsk_TxL_Item.drop(columns=[1, 2, 3, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_gmsk_TxL_Item.columns = ["Band", "TXL"]
    df_gmsk_TxL_Item = df_gmsk_TxL_Item.replace(
        {"Band": {"GSM850": "G085", "GSM900": "G09", "DCS1800": "G18", "PCS1900": "G19"}}
    )
    df_gmsk_TxL = pd.merge(df_gmsk_TxL_Item, df_gmsk_TxL_Value, left_index=True, right_index=True)
    df_gmsk_TxL_Mean = round(df_gmsk_TxL.groupby(["Band", "TXL"], sort=False).mean(), 1)
    df_gmsk_TxL_Mean["Average"] = round(df_gmsk_TxL_Mean.mean(axis=1), 1)

    df_edge = df_Meas[df_Meas["Test Conditions"].str.contains("CH_EPSK_").to_list()]
    df_edge_Value = df_edge.iloc[:, 2:]
    df_edge_Item = df_edge["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_edge_Item.drop(columns=[1, 2, 5, 7, 8, 9, 10], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_edge_Item.columns = ["Band", "Type", "Gain", "Index"]
    df_edge_Item = df_edge_Item.replace(
        {"Band": {"GSM850": "G085", "GSM900": "G09", "DCS1800": "G18", "PCS1900": "G19"}}
    )
    df_edge = pd.merge(df_edge_Item, df_edge_Value, left_index=True, right_index=True)
    df_null = df_edge[df_edge["Index"].isnull()].index
    df_edge.drop(df_null, inplace=True)
    df_edge_Mean = round(df_edge.groupby(["Band", "Type", "Gain", "Index"], sort=False).mean(), 1)
    df_edge_Mean["Average"] = round(df_edge_Mean.mean(axis=1), 1)

    df_edge_TxL = df_Meas[df_Meas["Test Conditions"].str.contains("CH_EPSK_TxL").to_list()]
    df_edge_TxL_Value = df_edge_TxL.iloc[:, 2:]
    df_edge_TxL_Item = df_edge_TxL["Test Conditions"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    df_edge_TxL_Item.drop(columns=[1, 2, 3, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_edge_TxL_Item.columns = ["Band", "TXL"]
    df_edge_TxL_Item = df_edge_TxL_Item.replace(
        {"Band": {"GSM850": "G085", "GSM900": "G09", "DCS1800": "G18", "PCS1900": "G19"}}
    )
    df_edge_TxL = pd.merge(df_edge_TxL_Item, df_edge_TxL_Value, left_index=True, right_index=True)
    df_edge_TxL_Mean = round(df_edge_TxL.groupby(["Band", "TXL"], sort=False).mean(), 1)
    df_edge_TxL_Mean["Average"] = round(df_edge_TxL_Mean.mean(axis=1), 1)

    if Save_data_var.get():
        filename = "Excel_2G_TX.xlsx"
        with pd.ExcelWriter("Excel_2G_TX.xlsx") as writer:
            df_gmsk_Mean.to_excel(writer, sheet_name="GMSK_Mean")
            df_gmsk_TxL_Mean.to_excel(writer, sheet_name="GMSK_TXL_Mean")
            df_edge_Mean.to_excel(writer, sheet_name="EDGE_Mean")
            df_edge_TxL_Mean.to_excel(writer, sheet_name="EDGE_TXL_Mean")
        func.WB_Format(filename, 2, 5, 0)

    return (
        df_gmsk_Mean["Average"],
        df_gmsk_TxL_Mean["Average"],
        df_edge_Mean["Average"],
        df_edge_TxL_Mean["Average"],
    )


def daseul_2g_rx_average(df_Meas):
    df_2g_gain = df_Meas[df_Meas["Test Conditions"].str.contains("CH_RxCalPower -60.00Bm").to_list()]
    df_2g_gain_Value = df_2g_gain.iloc[:, 2:]
    df_2g_gain_Item = df_2g_gain["Test Conditions"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    df_2g_gain_Item.drop(columns=[1, 2, 3, 4], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_2g_gain_Item.columns = ["Band"]
    df_2g_gain_Item = df_2g_gain_Item.replace(
        {"Band": {"GSM850": "G085", "GSM900": "G09", "DCS1800": "G18", "PCS1900": "G19"}}
    )
    df_2g_gain = pd.merge(df_2g_gain_Item, df_2g_gain_Value, left_index=True, right_index=True)
    df_2g_gain_Mean = round(df_2g_gain.groupby(["Band"]).mean(), 1)
    df_2g_gain_Mean["Average"] = round(df_2g_gain_Mean.mean(axis=1), 1)

    df_2g_ripple = df_Meas[df_Meas["Test Conditions"].str.contains("_RX_Ripple").to_list()]
    df_2g_ripple_Value = df_2g_ripple.iloc[:, 2:]
    df_2g_ripple_Item = df_2g_ripple["Test Conditions"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    df_2g_ripple_Item.drop(columns=[1, 2, 3], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_2g_ripple_Item.columns = ["Band"]
    df_2g_ripple_Item = df_2g_ripple_Item.replace(
        {"Band": {"GSM850": "G085", "GSM900": "G09", "DCS1800": "G18", "PCS1900": "G19"}}
    )
    df_2g_ripple = pd.merge(df_2g_ripple_Item, df_2g_ripple_Value, left_index=True, right_index=True)
    df_2g_ripple_Mean = round(df_2g_ripple.groupby(["Band"]).mean(), 1)
    df_2g_ripple_Mean["Average"] = round(df_2g_ripple_Mean.mean(axis=1), 1)

    return df_2g_gain_Mean["Average"], df_2g_ripple_Mean["Average"]


def daseul_3G_rx_average(df_Meas):
    df_PRX_Gain_3G = df_Meas[df_Meas["Test Conditions"].str.contains("_Main_PRX").to_list()]
    df_PRX_Gain_3G_Value = df_PRX_Gain_3G.iloc[:, 2:]
    df_PRX_Gain_3G_Item = df_PRX_Gain_3G["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_PRX_Gain_3G_Item.drop(columns=[0, 2, 3, 4, 5], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_PRX_Gain_3G_Item.columns = ["Band"]
    df_PRX_Gain_3G = pd.merge(df_PRX_Gain_3G_Item, df_PRX_Gain_3G_Value, left_index=True, right_index=True)
    df_PRX_Gain_3G_mean = round(df_PRX_Gain_3G.groupby(["Band"]).mean(), 1)
    df_PRX_Gain_3G_data = round(df_PRX_Gain_3G.groupby(["Band"]).agg(["mean", "max", "min"]), 1)
    df_PRX_Gain_3G_mean["Average"] = round(df_PRX_Gain_3G_mean.mean(axis=1), 1)

    df_PRX_Comp_3G = df_Meas[df_Meas["Test Conditions"].str.contains("_MAIN_PRX_Comp").to_list()]
    df_PRX_Comp_3G_Value = df_PRX_Comp_3G.iloc[:, 2:]
    df_PRX_Comp_3G_Item = df_PRX_Comp_3G["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_PRX_Comp_3G_Item.drop(columns=[0, 2, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_PRX_Comp_3G_Item.columns = ["Band", "CH"]
    df_PRX_Comp_3G = pd.merge(df_PRX_Comp_3G_Item, df_PRX_Comp_3G_Value, left_index=True, right_index=True)
    df_PRX_Comp_3G_mean = round(df_PRX_Comp_3G.groupby(["Band", "CH"]).mean(), 1)
    df_PRX_Comp_3G_data = round(df_PRX_Comp_3G.groupby(["Band", "CH"]).agg(["mean", "max", "min"]), 1)
    df_PRX_Comp_3G_mean["Average"] = round(df_PRX_Comp_3G_mean.mean(axis=1), 1)

    return (
        df_PRX_Gain_3G_mean["Average"],
        df_PRX_Gain_3G_mean,
        df_PRX_Gain_3G_data,
        df_PRX_Comp_3G_mean["Average"],
        df_PRX_Comp_3G_mean,
        df_PRX_Comp_3G_data,
    )


def daseul_sub6_rx_average(df_Meas):
    df_PRX_Gain_sub6 = df_Meas[df_Meas["Test Conditions"].str.contains("_MAIN_PRX_GAIN_STAGE").to_list()]
    df_PRX_Gain_sub6_Value = df_PRX_Gain_sub6.iloc[:, 2:]
    df_PRX_Gain_sub6_Item = df_PRX_Gain_sub6["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_PRX_Gain_sub6_Item.drop(columns=[0, 2, 3, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_PRX_Gain_sub6_Item.columns = ["Band", "Stage"]
    df_PRX_Gain_sub6 = pd.merge(df_PRX_Gain_sub6_Item, df_PRX_Gain_sub6_Value, left_index=True, right_index=True)
    df_PRX_Gain_sub6_mean = round(df_PRX_Gain_sub6.groupby(["Band", "Stage"]).mean(), 1)
    df_PRX_Gain_sub6_data = round(df_PRX_Gain_sub6.groupby(["Band", "Stage"]).agg(["mean", "max", "min"]), 1)
    df_PRX_Gain_sub6_mean["Average"] = round(df_PRX_Gain_sub6_mean.mean(axis=1))

    df_PRX_RSRP_sub6 = df_Meas[df_Meas["Test Conditions"].str.contains("_RSRP_OFFSET_MAIN_").to_list()]
    df_PRX_RSRP_sub6_Value = df_PRX_RSRP_sub6.iloc[:, 2:]
    df_PRX_RSRP_sub6_Item = df_PRX_RSRP_sub6["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_PRX_RSRP_sub6_Item.drop(columns=[0, 2, 3, 4, 5, 6, 7], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_PRX_RSRP_sub6_Item.columns = ["Band"]
    df_PRX_RSRP_sub6 = pd.merge(df_PRX_RSRP_sub6_Item, df_PRX_RSRP_sub6_Value, left_index=True, right_index=True)
    df_PRX_RSRP_sub6_mean = round(df_PRX_RSRP_sub6.groupby(["Band"]).mean(), 1)
    df_PRX_RSRP_sub6_data = round(df_PRX_RSRP_sub6.groupby(["Band"]).agg(["mean", "max", "min"]), 1)
    df_PRX_RSRP_sub6_mean["Average"] = round(df_PRX_RSRP_sub6_mean.mean(axis=1), 1)

    df_PRX_Comp_sub6 = df_Meas[df_Meas["Test Conditions"].str.contains("_Freq_MAIN_PRX_Offset").to_list()]
    df_PRX_Comp_sub6_Value = df_PRX_Comp_sub6.iloc[:, 2:]
    df_PRX_Comp_sub6_Item = df_PRX_Comp_sub6["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_PRX_Comp_sub6_Item.drop(columns=[0, 2, 3, 4, 5, 6, 7], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_PRX_Comp_sub6_Item.columns = ["Band"]
    df_PRX_Comp_sub6 = pd.merge(df_PRX_Comp_sub6_Item, df_PRX_Comp_sub6_Value, left_index=True, right_index=True)
    df_PRX_Comp_sub6_mean = round(df_PRX_Comp_sub6.groupby(["Band"]).mean(), 1)
    df_PRX_Comp_sub6_data = round(df_PRX_Comp_sub6.groupby(["Band"]).agg(["mean", "max", "min"]), 1)
    df_PRX_Comp_sub6_mean["Average"] = round(df_PRX_Comp_sub6_mean.mean(axis=1), 1)

    return (
        df_PRX_Gain_sub6_mean["Average"],
        df_PRX_Gain_sub6_mean,
        df_PRX_Gain_sub6_data,
        df_PRX_RSRP_sub6_mean["Average"],
        df_PRX_RSRP_sub6_mean,
        df_PRX_RSRP_sub6_data,
        df_PRX_Comp_sub6_mean["Average"],
        df_PRX_Comp_sub6_mean,
        df_PRX_Comp_sub6_data,
    )


def fbrx_average(df_Meas, df_Code, Save_data_var):
    (
        Gain_Meas_3G,
        Gain_Meas_3G_Mean,
        Gain_Meas_3G_Data,
        Gain_Meas_NR,
        Gain_Meas_NR_Mean,
        Gain_Meas_NR_Data,
    ) = fbrx_gain_meas_average(df_Meas)
    (
        Gain_Code_3G,
        Gain_Code_3G_Mean,
        Gain_Code_3G_Data,
        Gain_Code_NR,
        Gain_Code_NR_Mean,
        Gain_Code_NR_Data,
    ) = fbrx_gain_code_average(df_Code)
    # FBRX Gain은 센터채널만 하기 때문에 편차가 적으나, FBRX Freq는 Min, Max 편차 발생함 -> Min, Max 구해서 스펙에 반영
    (
        Freq_Meas_3G,
        Freq_Meas_3G_Max,
        Freq_Meas_3G_Min,
        Freq_Meas_3G_Mean,
        Freq_Meas_3G_Data,
    ) = fbrx_3g_freq_meas_average(df_Meas)
    (
        Freq_Meas_NR,
        Freq_Meas_NR_Max,
        Freq_Meas_NR_Min,
        Freq_Meas_NR_Mean,
        Freq_Meas_NR_Data,
    ) = fbrx_nr_freq_meas_average(df_Meas)
    (
        Freq_Code_NR,
        Freq_Code_NR_Max,
        Freq_Code_NR_Min,
        Freq_Code_NR_Mean,
        Freq_Code_NR_Data,
    ) = fbrx_nr_freq_code_average(df_Code)

    if Save_data_var.get():
        filename = "Excel_FBRX_Gain.xlsx"
        with pd.ExcelWriter(filename) as writer:
            Gain_Meas_3G_Mean.to_excel(writer, sheet_name="Gain_Meas_3G_Mean")
            Gain_Meas_3G_Data.to_excel(writer, sheet_name="Gain_Meas_3G_Data")
            Gain_Meas_NR_Mean.to_excel(writer, sheet_name="Gain_Meas_NR_Mean")
            Gain_Meas_NR_Data.to_excel(writer, sheet_name="Gain_Meas_NR_Data")
            Gain_Code_3G_Mean.to_excel(writer, sheet_name="Gain_Code_3G_Mean")
            Gain_Code_3G_Data.to_excel(writer, sheet_name="Gain_Code_3G_Data")
            Gain_Code_NR_Mean.to_excel(writer, sheet_name="Gain_Code_NR_Mean")
            Gain_Code_NR_Data.to_excel(writer, sheet_name="Gain_Code_NR_Data")
        func.WB_Format(filename, 2, 5, 0)

        filename = "Excel_FBRX_Freq.xlsx"
        with pd.ExcelWriter(filename) as writer:
            Freq_Meas_3G_Mean.to_excel(writer, sheet_name="Freq_Meas_3G_Mean")
            Freq_Meas_3G_Data.to_excel(writer, sheet_name="Freq_Meas_3G_Data")
            Freq_Meas_NR_Mean.to_excel(writer, sheet_name="Freq_Meas_NR_Mean")
            Freq_Meas_NR_Data.to_excel(writer, sheet_name="Freq_Meas_NR_Data")
            Freq_Code_NR_Mean.to_excel(writer, sheet_name="Freq_Code_NR_Mean")
            Freq_Code_NR_Data.to_excel(writer, sheet_name="Freq_Code_NR_Data")
        func.WB_Format(filename, 2, 5, 0)

    return (
        Gain_Meas_3G,
        Gain_Meas_NR,
        Gain_Code_3G,
        Gain_Code_NR,
        Freq_Meas_3G,
        Freq_Meas_3G_Max,
        Freq_Meas_3G_Min,
        Freq_Meas_NR,
        Freq_Meas_NR_Max,
        Freq_Meas_NR_Min,
        Freq_Code_NR,
        Freq_Code_NR_Max,
        Freq_Code_NR_Min,
    )


def fbrx_gain_meas_average(df_Meas):
    df_3g_fbrx_gain = df_Meas[df_Meas["Test Conditions"].str.contains("_FBRX_Gain_").to_list()]
    df_3g_fbrx_gain_Value = df_3g_fbrx_gain.iloc[:, 2:]
    df_3g_fbrx_gain_Item = df_3g_fbrx_gain["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_3g_fbrx_gain_Item.drop(columns=[2, 3, 4, 5], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_3g_fbrx_gain_Item.columns = ["RAT", "Band", "Index"]
    df_3g_fbrx_gain = pd.merge(df_3g_fbrx_gain_Item, df_3g_fbrx_gain_Value, left_index=True, right_index=True)
    df_3g_fbrx_gain_Mean = round(df_3g_fbrx_gain.groupby(["RAT", "Band", "Index"]).mean(), 1)
    df_3g_fbrx_gain_Data = round(
        df_3g_fbrx_gain.groupby(["RAT", "Band", "Index"]).agg(["mean", "max", "min"]),
        2,
    )
    df_3g_fbrx_gain_Mean["Average"] = round(df_3g_fbrx_gain_Mean.mean(axis=1), 2)

    df_nr_fbrx_gain = df_Meas[df_Meas["Test Conditions"].str.contains("_FBRX_Index").to_list()]
    df_nr_fbrx_gain_Value = df_nr_fbrx_gain.iloc[:, 2:]
    df_nr_fbrx_gain_Item = df_nr_fbrx_gain["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_nr_fbrx_gain_Item.drop(columns=[3, 4], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_nr_fbrx_gain_Item.columns = ["RAT", "Path", "Band", "Index"]
    df_nr_fbrx_gain = pd.merge(df_nr_fbrx_gain_Item, df_nr_fbrx_gain_Value, left_index=True, right_index=True)
    df_nr_fbrx_gain_Mean = round(df_nr_fbrx_gain.groupby(["RAT", "Path", "Band", "Index"]).mean(), 1)
    df_nr_fbrx_gain_Data = round(
        df_nr_fbrx_gain.groupby(["RAT", "Path", "Band", "Index"]).agg(["mean", "max", "min"]),
        2,
    )
    df_nr_fbrx_gain_Mean["Average"] = round(df_nr_fbrx_gain_Mean.mean(axis=1), 2)

    return (
        df_3g_fbrx_gain_Mean["Average"],
        df_3g_fbrx_gain_Mean,
        df_3g_fbrx_gain_Data,
        df_nr_fbrx_gain_Mean["Average"],
        df_nr_fbrx_gain_Mean,
        df_nr_fbrx_gain_Data,
    )


def fbrx_gain_code_average(df_Code):
    df_3g_fbrx_code = df_Code[df_Code["Test Conditions"].str.contains("_Modulation_FBRX_Result").to_list()]
    df_3g_fbrx_code_Value = df_3g_fbrx_code.iloc[:, 2:]
    df_3g_fbrx_code_Item = df_3g_fbrx_code["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_3g_fbrx_code_Item.drop(columns=[2, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_3g_fbrx_code_Item.columns = ["RAT", "Band", "CH"]
    df_3g_fbrx_code = pd.merge(df_3g_fbrx_code_Item, df_3g_fbrx_code_Value, left_index=True, right_index=True)
    df_3g_fbrx_code_mean = round(df_3g_fbrx_code.groupby(["RAT", "Band", "CH"]).mean())
    df_3g_fbrx_code_data = round(df_3g_fbrx_code.groupby(["RAT", "Band", "CH"]).agg(["mean", "max", "min"]))
    df_3g_fbrx_code_mean["Average"] = round(df_3g_fbrx_code_mean.mean(axis=1))

    df_nr_fbrx_code = df_Code[df_Code["Test Conditions"].str.contains("_FBRX_Index").to_list()]
    df_nr_fbrx_code_Value = df_nr_fbrx_code.iloc[:, 2:]
    df_nr_fbrx_code_Item = df_nr_fbrx_code["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_nr_fbrx_code_Item.drop(columns=[3, 4], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_nr_fbrx_code_Item.columns = ["RAT", "Path", "Band", "Index"]
    df_nr_fbrx_code = pd.merge(df_nr_fbrx_code_Item, df_nr_fbrx_code_Value, left_index=True, right_index=True)
    df_nr_fbrx_code_mean = round(df_nr_fbrx_code.groupby(["RAT", "Path", "Band", "Index"]).mean())
    df_nr_fbrx_code_data = round(df_nr_fbrx_code.groupby(["RAT", "Path", "Band", "Index"]).agg(["mean", "max", "min"]))
    df_nr_fbrx_code_mean["Average"] = round(df_nr_fbrx_code_mean.mean(axis=1))

    return (
        df_3g_fbrx_code_mean["Average"],
        df_3g_fbrx_code_mean,
        df_3g_fbrx_code_data,
        df_nr_fbrx_code_mean["Average"],
        df_nr_fbrx_code_mean,
        df_nr_fbrx_code_data,
    )


def fbrx_3g_freq_meas_average(df_Meas):
    df_3g_drop = df_Meas[df_Meas["Test Conditions"].str.contains("_FBRX_Gain_Index")].index
    df_Meas.drop(df_3g_drop, inplace=True)
    df_3g = df_Meas[df_Meas["Test Conditions"].str.contains("WCDMA").to_list()]
    df_3g_fbrx_freq = df_3g[df_3g["Test Conditions"].str.contains("CH_FBRX_").to_list()]

    df_3g_fbrx_freq_Value = df_3g_fbrx_freq.iloc[:, 2:]
    df_3g_fbrx_freq_Item = df_3g_fbrx_freq["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_3g_fbrx_freq_Item.drop(columns=[2, 3, 4, 5], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_3g_fbrx_freq_Item.columns = ["RAT", "Band"]
    df_3g_fbrx_freq = pd.merge(df_3g_fbrx_freq_Item, df_3g_fbrx_freq_Value, left_index=True, right_index=True)
    df_3g_fbrx_freq_mean = round(df_3g_fbrx_freq.groupby(["RAT", "Band"]).mean())
    df_3g_fbrx_freq_max = round(df_3g_fbrx_freq.groupby(["RAT", "Band"]).max())
    df_3g_fbrx_freq_min = round(df_3g_fbrx_freq.groupby(["RAT", "Band"]).min())
    df_3g_fbrx_freq_data = round(df_3g_fbrx_freq.groupby(["RAT", "Band"]).agg(["mean", "max", "min"]))
    df_3g_fbrx_freq_mean["Average"] = round(df_3g_fbrx_freq_mean.mean(axis=1), 2)
    df_3g_fbrx_freq_mean["Max"] = round(df_3g_fbrx_freq_max.max(axis=1), 2)
    df_3g_fbrx_freq_mean["Min"] = round(df_3g_fbrx_freq_min.min(axis=1), 2)

    return (
        df_3g_fbrx_freq_mean["Average"],
        df_3g_fbrx_freq_mean["Max"],
        df_3g_fbrx_freq_mean["Min"],
        df_3g_fbrx_freq_mean,
        df_3g_fbrx_freq_data,
    )


def fbrx_nr_freq_meas_average(df_Meas):
    df_nr_drop = df_Meas[df_Meas["Test Conditions"].str.contains("_FBRX_Index")].index
    df_Meas.drop(df_nr_drop, inplace=True)
    df_nr = df_Meas[df_Meas["Test Conditions"].str.contains("NR").to_list()]
    df_nr_fbrx_freq = df_nr[df_nr["Test Conditions"].str.contains("_FBRX_").to_list()]

    df_nr_fbrx_freq_Value = df_nr_fbrx_freq.iloc[:, 2:]
    df_nr_fbrx_freq_Item = df_nr_fbrx_freq["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_nr_fbrx_freq_Item.drop(columns=[3, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_nr_fbrx_freq_Item.columns = ["RAT", "Band", "Path"]
    df_nr_fbrx_freq = pd.merge(df_nr_fbrx_freq_Item, df_nr_fbrx_freq_Value, left_index=True, right_index=True)
    df_nr_fbrx_freq_mean = round(df_nr_fbrx_freq.groupby(["RAT", "Band", "Path"]).mean())
    df_nr_fbrx_freq_data = round(df_nr_fbrx_freq.groupby(["RAT", "Band", "Path"]).agg(["mean", "max", "min"]))
    df_nr_fbrx_freq_mean["Average"] = round(df_nr_fbrx_freq_mean.mean(axis=1), 1)
    df_nr_fbrx_freq_mean["Max"] = round(df_nr_fbrx_freq_mean.max(axis=1), 1)
    df_nr_fbrx_freq_mean["Min"] = round(df_nr_fbrx_freq_mean.min(axis=1), 1)

    return (
        df_nr_fbrx_freq_mean["Average"],
        df_nr_fbrx_freq_mean["Max"],
        df_nr_fbrx_freq_mean["Min"],
        df_nr_fbrx_freq_mean,
        df_nr_fbrx_freq_data,
    )


def fbrx_nr_freq_code_average(df_Code):
    df_nr_drop = df_Code[df_Code["Test Conditions"].str.contains("_FBRX_Index")].index
    df_Code.drop(df_nr_drop, inplace=True)
    df_nr = df_Code[df_Code["Test Conditions"].str.contains("NR").to_list()]
    df_nr_fbrx_freq = df_nr[df_nr["Test Conditions"].str.contains("_FBRX_").to_list()]

    df_nr_fbrx_freq_Value = df_nr_fbrx_freq.iloc[:, 2:]
    df_nr_fbrx_freq_Item = df_nr_fbrx_freq["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_nr_fbrx_freq_Item.drop(columns=[3, 4, 5, 6], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_nr_fbrx_freq_Item.columns = ["RAT", "Band", "Path"]
    df_nr_fbrx_freq = pd.merge(df_nr_fbrx_freq_Item, df_nr_fbrx_freq_Value, left_index=True, right_index=True)
    df_nr_fbrx_freq_mean = round(df_nr_fbrx_freq.groupby(["RAT", "Band", "Path"]).mean())
    df_nr_fbrx_freq_data = round(df_nr_fbrx_freq.groupby(["RAT", "Band", "Path"]).agg(["mean", "max", "min"]))
    df_nr_fbrx_freq_mean["Average"] = round(df_nr_fbrx_freq_mean.mean(axis=1))
    df_nr_fbrx_freq_mean["Max"] = round(df_nr_fbrx_freq_mean.max(axis=1))
    df_nr_fbrx_freq_mean["Min"] = round(df_nr_fbrx_freq_mean.min(axis=1))

    return (
        df_nr_fbrx_freq_mean["Average"],
        df_nr_fbrx_freq_mean["Max"],
        df_nr_fbrx_freq_mean["Min"],
        df_nr_fbrx_freq_mean,
        df_nr_fbrx_freq_data,
    )


def apt_average(df_Meas, Save_data_var):
    # APT_Meas_3G_Ave, df_APT_Meas_3G_mean, df_APT_Meas_3G_data = Apt_3g_meas_average(df_Meas)
    APT_Meas_3G_Ave, df_APT_Meas_3G_mean = Apt_3g_meas_average(df_Meas)
    (
        APT_Meas_sub6_Ave,
        APT_Meas_sub6_Max,
        APT_Meas_sub6_Min,
        df_APT_Meas_sub6_Mean,
        # df_APT_Meas_sub6_data,
    ) = Apt_sub6_meas_average(df_Meas)

    if Save_data_var.get():
        filename = "Excel_APT.xlsx"
        with pd.ExcelWriter(filename) as writer:
            df_APT_Meas_3G_mean.to_excel(writer, sheet_name="APT_Meas_3G_mean")
            # df_APT_Meas_3G_data.to_excel(writer, sheet_name="APT_Meas_3G_data")
            df_APT_Meas_sub6_Mean.to_excel(writer, sheet_name="APT_Meas_sub6_Mean")
            # df_APT_Meas_sub6_data.to_excel(writer, sheet_name="APT_Meas_sub6_data")
        func.WB_Format(filename, 2, 5, 0)

    return APT_Meas_3G_Ave, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min


def Apt_3g_meas_average(df_Meas):
    df_APT_Meas_3G = df_Meas[df_Meas["Test Conditions"].str.contains("_APT_PA_").to_list()]
    df_APT_Meas_3G_Value = df_APT_Meas_3G.iloc[:, 2:]
    df_APT_Meas_3G_Item = df_APT_Meas_3G["Test Conditions"].str.split("_|\\(|\\)", expand=True)
    # 의미없는 컬럼 삭제
    df_APT_Meas_3G_Item.drop(columns=[0, 2, 3, 4, 5, 7, 9, 10], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_APT_Meas_3G_Item.columns = ["Band", "PA Stage", "Index"]
    df_APT_Meas_3G = pd.merge(df_APT_Meas_3G_Item, df_APT_Meas_3G_Value, left_index=True, right_index=True)
    df_APT_Meas_3G_mean = round(df_APT_Meas_3G.groupby(["Band", "PA Stage", "Index"], sort=False).mean(), 2)
    # df_APT_Meas_3G_data = round(
    #     df_APT_Meas_3G.groupby(["Band", "PA Stage", "Index"], sort=False).agg(["mean", "max", "min"]),
    #     2,
    # )
    df_APT_Meas_3G_mean["Average"] = round(df_APT_Meas_3G_mean.mean(axis=1), 2)

    return (
        df_APT_Meas_3G_mean["Average"],
        df_APT_Meas_3G_mean,
    )  # df_APT_Meas_3G_data


def Apt_sub6_meas_average(df_Meas):
    df_3G = df_Meas[df_Meas["Test Conditions"].str.contains("WCDMA")].index
    df_Meas.drop(df_3G, inplace=True)
    df_MCH = df_Meas[df_Meas["Test Conditions"].str.contains("_MCH_APT_")].index
    df_Meas.drop(df_MCH, inplace=True)
    df_APT_Meas_sub6 = df_Meas[df_Meas["Test Conditions"].str.contains("CH_APT_").to_list()]
    df_APT_Meas_sub6_Value = df_APT_Meas_sub6.iloc[:, 2:]
    df_APT_Meas_sub6_Item = df_APT_Meas_sub6["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_APT_Meas_sub6_Item.drop(columns=[0, 3, 4, 5, 7], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_APT_Meas_sub6_Item.columns = ["Band", "Path", "PA Stage", "Index"]
    df_APT_Meas_sub6 = pd.merge(df_APT_Meas_sub6_Item, df_APT_Meas_sub6_Value, left_index=True, right_index=True)
    df_APT_Meas_sub6_Mean = round(
        df_APT_Meas_sub6.groupby(["Band", "Path", "PA Stage", "Index"], sort=False).mean(),
        2,
    )
    df_APT_Meas_sub6_Max = round(
        df_APT_Meas_sub6.groupby(["Band", "Path", "PA Stage", "Index"], sort=False).max(),
        2,
    )
    df_APT_Meas_sub6_Min = round(
        df_APT_Meas_sub6.groupby(["Band", "Path", "PA Stage", "Index"], sort=False).min(),
        2,
    )
    # df_APT_Meas_sub6_data = round(
    #     df_APT_Meas_sub6.groupby(["Band", "Path", "PA Stage", "Index"], sort=False).agg(
    #         ["mean", "max", "min"]
    #     ),
    #     2,
    # )
    df_APT_Meas_sub6_Mean["Average"] = round(df_APT_Meas_sub6_Mean.mean(axis=1), 2)
    df_APT_Meas_sub6_Mean["Max"] = round(df_APT_Meas_sub6_Max.max(axis=1), 2)
    df_APT_Meas_sub6_Mean["Min"] = round(df_APT_Meas_sub6_Min.min(axis=1), 2)

    return (
        df_APT_Meas_sub6_Mean["Average"],
        df_APT_Meas_sub6_Mean["Max"],
        df_APT_Meas_sub6_Mean["Min"],
        df_APT_Meas_sub6_Mean,
        # df_APT_Meas_sub6_data,
    )


def sub6_et_average(df_Meas, Save_data_var):
    (
        ETSAPT_sub6_Psat_Ave,
        ETSAPT_sub6_Psat_Max,
        ETSAPT_sub6_Psat_Min,
        df_et_sub6_psat_mean,
        df_et_sub6_psat_data,
    ) = sub6_et_psat_ave(df_Meas)
    (
        ETSAPT_sub6_Freq_Ave,
        ETSAPT_sub6_Freq_Max,
        ETSAPT_sub6_Freq_Min,
        df_et_sub6_pgain_mean,
        df_et_sub6_pgain_data,
    ) = sub6_et_freq_ave(df_Meas)
    (
        ETSAPT_sub6_Pgain_Ave,
        ETSAPT_sub6_Pgain_Max,
        ETSAPT_sub6_Pgain_Min,
        df_et_sub6_freqp_mean,
        df_et_sub6_freqp_data,
    ) = sub6_et_pgain_ave(df_Meas)
    (
        ETSAPT_sub6_Power_Ave,
        ETSAPT_sub6_Power_Max,
        ETSAPT_sub6_Power_Min,
        df_et_sub6_power_mean,
        df_et_sub6_power_data,
    ) = sub6_et_power_ave(df_Meas)

    if Save_data_var.get():
        filename = "Excel_ETSAPT_sub6.xlsx"
        with pd.ExcelWriter(filename) as writer:
            df_et_sub6_psat_mean.to_excel(writer, sheet_name="ETSAPT_sub6_Psat_mean")
            df_et_sub6_psat_data.to_excel(writer, sheet_name="ETSAPT_sub6_Psat_data")
            df_et_sub6_pgain_mean.to_excel(writer, sheet_name="ETSAPT_sub6_Pgain_Mean")
            df_et_sub6_pgain_data.to_excel(writer, sheet_name="ETSAPT_sub6_Pgain_data")
            df_et_sub6_freqp_mean.to_excel(writer, sheet_name="ETSAPT_sub6_Freq_Mean")
            df_et_sub6_freqp_data.to_excel(writer, sheet_name="ETSAPT_sub6_Freq_data")
            df_et_sub6_power_mean.to_excel(writer, sheet_name="ETSAPT_sub6_Power_Mean")
            df_et_sub6_power_data.to_excel(writer, sheet_name="ETSAPT_sub6_Power_data")
        func.WB_Format(filename, 2, 5, 0)

    return (
        ETSAPT_sub6_Psat_Ave,
        ETSAPT_sub6_Psat_Max,
        ETSAPT_sub6_Psat_Min,
        ETSAPT_sub6_Freq_Ave,
        ETSAPT_sub6_Freq_Max,
        ETSAPT_sub6_Freq_Min,
        ETSAPT_sub6_Pgain_Ave,
        ETSAPT_sub6_Pgain_Max,
        ETSAPT_sub6_Pgain_Min,
        ETSAPT_sub6_Power_Ave,
        ETSAPT_sub6_Power_Max,
        ETSAPT_sub6_Power_Min,
    )


def sub6_et_psat_ave(df_Meas):
    df_et_psat = df_Meas[df_Meas["Test Conditions"].str.contains("_ET_S-APT_Psat").to_list()]
    df_et_psat_Value = df_et_psat.iloc[:, 2:]
    df_et_psat_Item = df_et_psat["Test Conditions"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    df_et_psat_Item.drop(columns=[0, 3, 4, 5, 6, 7, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_et_psat_Item.columns = ["Band", "Path"]
    df_et_psat = pd.merge(df_et_psat_Item, df_et_psat_Value, left_index=True, right_index=True)
    df_et_psat_mean = round(df_et_psat.groupby(["Band", "Path"], sort=False).mean(), 1)
    df_et_psat_data = round(df_et_psat.groupby(["Band", "Path"], sort=False).agg(["mean", "max", "min"]), 1)
    df_et_psat_mean["Average"] = round(df_et_psat_mean.mean(axis=1), 1)
    df_et_psat_mean["Max"] = round(df_et_psat_mean.max(axis=1), 1)
    df_et_psat_mean["Min"] = round(df_et_psat_mean.min(axis=1), 1)

    return (
        df_et_psat_mean["Average"],
        df_et_psat_mean["Max"],
        df_et_psat_mean["Min"],
        df_et_psat_mean,
        df_et_psat_data,
    )


def sub6_et_pgain_ave(df_Meas):
    df_et_pgain = df_Meas[df_Meas["Test Conditions"].str.contains("_ET_S-APT_Pgain").to_list()]
    df_et_pgain_Value = df_et_pgain.iloc[:, 2:]
    df_et_pgain_Item = df_et_pgain["Test Conditions"].str.split("_| ", expand=True)
    # 의미없는 컬럼 삭제
    df_et_pgain_Item.drop(columns=[0, 3, 4, 5, 6, 7, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_et_pgain_Item.columns = ["Band", "Path"]
    df_et_pgain = pd.merge(df_et_pgain_Item, df_et_pgain_Value, left_index=True, right_index=True)
    df_et_pgain_mean = round(df_et_pgain.groupby(["Band", "Path"], sort=False).mean(), 1)
    df_et_pgain_data = round(df_et_pgain.groupby(["Band", "Path"], sort=False).agg(["mean", "max", "min"]), 1)
    df_et_pgain_mean["Average"] = round(df_et_pgain_mean.mean(axis=1), 1)
    df_et_pgain_mean["Max"] = round(df_et_pgain_mean.max(axis=1), 1)
    df_et_pgain_mean["Min"] = round(df_et_pgain_mean.min(axis=1), 1)

    return (
        df_et_pgain_mean["Average"],
        df_et_pgain_mean["Max"],
        df_et_pgain_mean["Min"],
        df_et_pgain_mean,
        df_et_pgain_data,
    )


def sub6_et_freq_ave(df_Meas):
    df_et_freqp = df_Meas[df_Meas["Test Conditions"].str.contains("_ET_S-APT_Freq_Power").to_list()]
    df_et_freqp_Value = df_et_freqp.iloc[:, 2:]
    df_et_freqp_Item = df_et_freqp["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_et_freqp_Item.drop(columns=[0, 3, 4, 5, 6, 7, 8, 10], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_et_freqp_Item.columns = ["Band", "Path", "BW"]
    df_et_freqp = pd.merge(df_et_freqp_Item, df_et_freqp_Value, left_index=True, right_index=True)
    df_et_freqp_mean = round(df_et_freqp.groupby(["Band", "Path", "BW"], sort=False).mean(), 1)
    df_et_freqp_data = round(
        df_et_freqp.groupby(["Band", "Path", "BW"], sort=False).agg(["mean", "max", "min"]),
        1,
    )
    df_et_freqp_mean["Average"] = round(df_et_freqp_mean.mean(axis=1), 1)
    df_et_freqp_mean["Max"] = round(df_et_freqp_mean.max(axis=1), 1)
    df_et_freqp_mean["Min"] = round(df_et_freqp_mean.min(axis=1), 1)

    return (
        df_et_freqp_mean["Average"],
        df_et_freqp_mean["Max"],
        df_et_freqp_mean["Min"],
        df_et_freqp_mean,
        df_et_freqp_data,
    )


def sub6_et_power_ave(df_Meas):
    df_et_power = df_Meas[df_Meas["Test Conditions"].str.contains("_ET_S-APT_Power_VBand").to_list()]
    df_et_power_Value = df_et_power.iloc[:, 2:]
    df_et_power_Item = df_et_power["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_et_power_Item.drop(columns=[0, 3, 4, 5, 6, 7, 8], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_et_power_Item.columns = ["Band", "Path", "Target"]
    df_et_power = pd.merge(df_et_power_Item, df_et_power_Value, left_index=True, right_index=True)
    df_et_power_mean = round(df_et_power.groupby(["Band", "Path", "Target"], sort=False).mean(), 2)
    df_et_power_data = round(
        df_et_power.groupby(["Band", "Path", "Target"], sort=False).agg(["mean", "max", "min"]),
        2,
    )
    df_et_power_mean["Average"] = round(df_et_power_mean.mean(axis=1), 1)
    df_et_power_mean["Max"] = round(df_et_power_mean.max(axis=1), 1)
    df_et_power_mean["Min"] = round(df_et_power_mean.min(axis=1), 1)

    return (
        df_et_power_mean["Average"],
        df_et_power_mean["Max"],
        df_et_power_mean["Min"],
        df_et_power_mean,
        df_et_power_data,
    )


def Et_3g_average(df_Meas, Save_data_var):
    (
        ETSAPT_3G_Psat_Ave,
        ETSAPT_3G_Psat_Max,
        ETSAPT_3G_Psat_Min,
        df_et_3g_psat_mean,
        df_et_3g_psat_data,
    ) = Et_3g_psat_ave(df_Meas)

    (
        ETSAPT_3G_Power_Ave,
        ETSAPT_3G_Power_Max,
        ETSAPT_3G_Power_Min,
        df_et_3g_power_mean,
        df_et_3g_power_data,
    ) = Et_3g_power_ave(df_Meas)

    if Save_data_var.get():
        filename = "Excel_ETSAPT_3G.xlsx"
        with pd.ExcelWriter(filename) as writer:
            ETSAPT_3G_Psat_Ave.to_excel(writer, sheet_name="ETSAPT_3G_Psat_Ave")
            df_et_3g_psat_mean.to_excel(writer, sheet_name="ETSAPT_3G_Psat_Mean")
            df_et_3g_psat_data.to_excel(writer, sheet_name="ETSAPT_3G_Psat_Data")
            ETSAPT_3G_Power_Ave.to_excel(writer, sheet_name="ETSAPT_3G_Power_Ave")
            df_et_3g_power_mean.to_excel(writer, sheet_name="ETSAPT_3G_Power_Mean")
            df_et_3g_power_data.to_excel(writer, sheet_name="ETSAPT_3G_Power_Data")
        func.WB_Format(filename, 2, 5, 0)

    return (
        ETSAPT_3G_Psat_Ave,
        ETSAPT_3G_Psat_Max,
        ETSAPT_3G_Psat_Min,
        ETSAPT_3G_Power_Ave,
        ETSAPT_3G_Power_Max,
        ETSAPT_3G_Power_Min,
    )


def Et_3g_psat_ave(df_Meas):
    df_hspa = df_Meas[df_Meas["Test Conditions"].str.contains("WCDMA_").to_list()]
    df_et_psat = df_hspa[df_hspa["Test Conditions"].str.contains("_ET_S-APT_PSat").to_list()]
    df_et_psat_Value = df_et_psat.iloc[:, 2:]
    df_et_psat_Item = df_et_psat["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_et_psat_Item.drop(columns=[0, 2, 3, 5, 6, 7], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_et_psat_Item.columns = ["Band", "R99"]
    df_et_psat = pd.merge(df_et_psat_Item, df_et_psat_Value, left_index=True, right_index=True)
    df_et_psat_mean = round(df_et_psat.groupby(["Band", "R99"], sort=False).mean(), 2)
    df_et_psat_data = round(
        df_et_psat.groupby(["Band", "R99"], sort=False).agg(["mean", "max", "min"]),
        2,
    )
    df_et_psat_mean["Average"] = round(df_et_psat_mean.mean(axis=1), 1)
    df_et_psat_mean["Max"] = round(df_et_psat_mean.max(axis=1), 1)
    df_et_psat_mean["Min"] = round(df_et_psat_mean.min(axis=1), 1)

    return (
        df_et_psat_mean["Average"],
        df_et_psat_mean["Max"],
        df_et_psat_mean["Min"],
        df_et_psat_mean,
        df_et_psat_data,
    )


def Et_3g_power_ave(df_Meas):
    df_hspa = df_Meas[df_Meas["Test Conditions"].str.contains("WCDMA_").to_list()]
    df_et_power = df_hspa[df_hspa["Test Conditions"].str.contains("_ET_S-APT_Power").to_list()]
    df_et_power_Value = df_et_power.iloc[:, 2:]
    df_et_power_Item = df_et_power["Test Conditions"].str.split("_", expand=True)
    # 의미없는 컬럼 삭제
    df_et_power_Item.drop(columns=[0, 2, 3, 5, 6, 7], inplace=True)
    # groupby 실행을 위한 컬럼명 변경
    df_et_power_Item.columns = ["Band", "R99"]
    df_et_power = pd.merge(df_et_power_Item, df_et_power_Value, left_index=True, right_index=True)
    df_et_power_mean = round(df_et_power.groupby(["Band", "R99"], sort=False).mean(), 2)
    df_et_power_data = round(
        df_et_power.groupby(["Band", "R99"], sort=False).agg(["mean", "max", "min"]),
        2,
    )
    df_et_power_mean["Average"] = round(df_et_power_mean.mean(axis=1), 1)
    df_et_power_mean["Max"] = round(df_et_power_mean.max(axis=1), 1)
    df_et_power_mean["Min"] = round(df_et_power_mean.min(axis=1), 1)

    return (
        df_et_power_mean["Average"],
        df_et_power_mean["Max"],
        df_et_power_mean["Min"],
        df_et_power_mean,
        df_et_power_data,
    )


def get_data(list_file, Select_op, text_area):
    text_area.insert(tk.END, "=" * 100)
    text_area.insert(tk.END, "\n")
    Result_Meas = pd.DataFrame()
    Result_Code = pd.DataFrame()

    if Select_op == "Daseul":
        Total_count = 0
        for file in list_file:
            Print_fname = os.path.basename(file)
            Print_Word = "Collecting Data"
            text_area.insert(tk.END, f"{Print_Word:<25}\t|\t{Print_fname}\t|\t")
            text_area.see(tk.END)
            # Import Data
            # my_cols = [str(i) for i in range(30)]  # create some col names
            my_cols = [
                "Test Conditions",
                "Meas",
                "Lower Limits",
                "Upper Limits",
                "P_F",
                "Sec",
                "Code",
                "Code LSL",
                "Code USL",
                "Meas Fine",
                "Code Fine",
            ]
            df_Data = pd.read_csv(
                file,
                sep="\t|,",
                names=my_cols,
                header=None,
                engine="python",
                encoding="utf-8",
            )
            text_area.insert(tk.END, f"Done\n")
            text_area.see(tk.END)
            # df_null = df_Data[df_Data["Test Conditions"].isnull()].index
            # df_Data.drop(df_null, inplace=True)
            # EPT가 Auto Sweep 이라서 캘로그마다 실행갯수가 다르다 -> 추출 후 Drop
            Print_Word = "Drop RFIC Gain Cal Data"
            text_area.insert(tk.END, f"{Print_Word:<25}\t|\t{Print_fname}\t|\t")
            text_area.see(tk.END)
            df_RFIC = df_Data[df_Data["Test Conditions"].str.contains("_RFIC_")].index
            df_Data.drop(df_RFIC, inplace=True)
            df_Data.reset_index(drop=True)
            text_area.insert(tk.END, f"Done\n")
            text_area.see(tk.END)

            count = df_Data[df_Data["Test Conditions"].str.contains("// << UartSwitchToCP >>")].shape[0]

            df_Meas = df_Data[["Test Conditions", "Meas"]].reset_index(drop=True)
            df_Code = df_Data[["Test Conditions", "Code"]].reset_index(drop=True)

            Start_Meas = df_Meas.index[
                df_Meas["Test Conditions"].str.contains("// << WCDMA Tx DC Calibration >>")
            ].tolist()
            Stop_Meas = df_Meas.index[df_Meas["Test Conditions"].str.contains("// << H/W Version Write >>")].tolist()
            Start_Code = df_Code.index[
                df_Code["Test Conditions"].str.contains("// << WCDMA Tx DC Calibration >>")
            ].tolist()
            Stop_Code = df_Code.index[
                df_Code["Test Conditions"].str.contains("// << SLSI_CAL_HSPA_POST_V3 >>")
            ].tolist()

            size_missmatch = False if (len(Start_Meas) == len(Stop_Meas)) else True

            Re_test_Count = 0
            for i in range(1, count, 1):
                Re_test = False
                if size_missmatch:
                    Subset_Meas = df_Meas[Start_Meas[i] : Stop_Meas[i - Re_test_Count]]
                    Subset_Code = df_Code[Start_Code[i] : Stop_Code[i - Re_test_Count]]
                else:
                    Subset_Meas = df_Meas[Start_Meas[i] : Stop_Meas[i]]
                    Subset_Code = df_Code[Start_Code[i] : Stop_Code[i]]

                Re_test = any(Subset_Meas["Test Conditions"].str.contains("// Retry"))
                if Re_test:
                    Re_test_Count += 1
                    continue

                Subset_Meas = Subset_Meas.dropna().reset_index(drop=True)
                Subset_Code = Subset_Code.dropna().reset_index(drop=True)

                if i == 1:
                    Result_Meas = Subset_Meas
                    Result_Code = Subset_Code
                    # groupby 실행 시 숫자가 아닌 열은 자동 생략 (ommiting nuisance) 처리됨, Pandas 차기버전부터 오류로 처리
                    # -> astype으로 Object를 float으로 변경
                    Result_Meas["Meas_1"] = Subset_Meas["Meas"].astype(float)
                    Result_Code["Code_1"] = Subset_Code["Code"].astype(float)
                else:
                    # groupby 실행 시 숫자가 아닌 열은 자동 생략 (ommiting nuisance) 처리됨, Pandas 차기버전부터 오류로 처리
                    # -> astype으로 Object를 float으로 변경
                    Result_Meas[f"Meas_{i}"] = Subset_Meas["Meas"].astype(float)
                    Result_Code[f"Code_{i}"] = Subset_Code["Code"].astype(float)
                text_area.insert(tk.END, f"Data Count = {i + Total_count}\n")
                text_area.see(tk.END)

            Total_count += i

    else:  # MTM
        for count, file in enumerate(list_file, start=1):
            Print_fname = os.path.basename(file)
            Print_Word = "Collecting Data"
            text_area.insert(tk.END, f"{Print_Word:<25}\t|\t{Print_fname}\t|\t")

            my_cols = [str(i) for i in range(20)]  # create some col names
            df_Data = pd.read_csv(file, sep="\t|,|=", names=my_cols, header=None, engine="python")
            text_area.insert(tk.END, f"Done\n")

            Print_Word = "Drop Null Data"
            text_area.insert(tk.END, f"{Print_Word:<25}\t|\t{Print_fname}\t|\t")
            df_Data = df_Data.iloc[2:, :3]
            df_null = df_Data[df_Data["0"].isnull()].index
            df_Data.drop(df_null, inplace=True)
            text_area.insert(tk.END, f"Done\n")

            Print_Word = "RFIC Gain Cal Data"
            text_area.insert(tk.END, f"{Print_Word:<25}\t|\t{Print_fname}\t|\t")
            text_area.see(tk.END)
            RFIC_Gain_index = df_Data[df_Data["1"].str.contains("RFIC Gain")].index.tolist()
            HSPA_Modul_index = df_Data[df_Data["1"].str.contains(" Modulation FBRx ")].index.tolist()
            RFIC_Gain_index.extend(HSPA_Modul_index)

            Subset_Meas = df_Data.drop(RFIC_Gain_index).reset_index(drop=True)
            Subset_Code = df_Data[df_Data["1"].str.contains(" value")].dropna().reset_index(drop=True)
            text_area.insert(tk.END, f"Done\n")

            Subset_Meas.columns = ["Band", "Item", "Meas"]
            Subset_Code.columns = ["Band", "Item", "Code"]
            # groupby 실행 시 숫자가 아닌 열은 자동 생략 (ommiting nuisance) 처리됨, Pandas 차기버전부터 오류로 처리
            # -> astype으로 Object를 float으로 변경
            if count == 1:
                Result_Meas = Subset_Meas
                Result_Code = Subset_Code
                Result_Meas["Meas_1"] = Subset_Meas["Meas"].astype(float)
                Result_Code["Code_1"] = Subset_Code["Code"].astype(float)
            else:
                Result_Meas[f"Meas_{count}"] = Subset_Meas["Meas"].astype(float)
                Result_Code[f"Code_{count}"] = Subset_Code["Code"].astype(float)

    text_area.insert(tk.END, "=" * 100)
    text_area.insert(tk.END, "\n")
    text_area.see(tk.END)

    return Result_Meas, Result_Code


def start(
    list_file,
    Option_var,
    txt_spc_path,
    Select_op,
    Cable_Spec_var,
    RX_Gain_Spec_var,
    FBRX_Spec_var,
    APT_Spec_var,
    ET_Psat_var,
    ET_Pgain_var,
    ET_Freq_var,
    ET_Power_var,
    RX_Gain_3G_Spec_var,
    FBRX_3G_Spec_var,
    RX_Gain_2G_Spec_var,
    GMSK_Spec_var,
    EPSK_Spec_var,
    Save_data_var,
    text_area,
):
    text_area.delete("1.0", "end")
    Selected_Option = Option_var.get()
    Selected_spc = txt_spc_path.get()

    try:
        if Select_op == "Daseul":
            if Selected_spc == "":
                msgbox.showwarning("경고", "SPC 파일(*.dec)을 선택하세요")
                return
            elif Selected_Option == 3:
                msgbox.showwarning("경고", "Daseul Option을 선택하세요")
                return
        elif Select_op == "MTM":
            if Selected_Option != 3:
                msgbox.showwarning("경고", "MTM Default Cal Data 옵션을 선택하세요")
                return

        # Test_List 생성
        Check_Sub6 = False
        Check_HSPA = False
        Check_2G = False

        Test_List = {}
        Search_SUB6 = "[SUB6_CALIBRATION_COMMON]\n"
        Search_HSPA = "[HSPA_COMMON]\n"
        Search_2G = "[Common_Parameter]\n"

        with open(Selected_spc, "r", encoding="utf-8") as file:
            data_lines = file.readlines()
        file.close()

        for index, line in enumerate(data_lines):
            if Search_SUB6 == line:
                Check_Sub6 = True
            elif Check_Sub6 and line.startswith("Cal_Band="):
                item_SUB6 = line.strip().replace("=", ",").split(",")
                key = dict.fromkeys(["SUB6"])
                list_a = item_SUB6[1 : len(item_SUB6)]
                list_a = [v for v in list_a if v]  # 리스트 값 공백 제거
                Test_List.update({"SUB6": list_a})
                break
            else:
                continue

        for index, line in enumerate(data_lines):
            if Search_HSPA == line:
                Check_HSPA = True
            elif Check_HSPA and line.startswith("Cal_Band="):
                item_HSPA = line.strip().replace("=", ",").split(",")
                key = dict.fromkeys(["HSPA"])
                list_a = item_HSPA[1 : len(item_HSPA)]
                list_a = [v for v in list_a if v]  # 리스트 값 공백 제거
                # 인덱스가 필요하기 때문에 int로 변환
                list_a = map(int, list_a)
                # 인덱스 값과 일치시키고 list_a를 list_b로 변환
                list_b = ["1", "2", "5", "4", "8"]
                ent = {i: k for i, k in enumerate(list_b)}
                result = list(map(ent.get, list_a))
                Test_List.update({"HSPA": result})
                break
            else:
                continue

        for index, line in enumerate(data_lines):
            if Search_2G == line:
                Check_2G = True
            elif Check_2G and line.startswith("Cal_Band="):
                item_2G = line.strip().replace("=", "").split(",")
                key = dict.fromkeys(["GSM"])
                Test_List.update({"GSM": ["G085", "G09", "G18", "G19"]})
                break
            else:
                continue

        if Selected_Option == 1:
            L_cable.chng_cable_spec_only(Selected_spc, Cable_Spec_var, text_area)

            # for rat in Test_List:
            #     for band in Test_List[rat]:
            #         if (rat == "LTE") and (band in ["32"]):
            #             Lsi_chng_rx_gain_spec_only(Selected_spc, rat, band)
            #         elif (rat == "NR") and (band in ["75"]):
            #             Lsi_chng_rx_gain_spec_only(Selected_spc, rat, band)
            #         elif rat == "GSM":
            #             Lsi_chng_2g_tx_spec_only(Selected_spc, rat, band)
            #             Lsi_chng_2g_rx_gain_spec_only(Selected_spc, rat, band)
            #         else:
            #             Lsi_chng_fbrx_meas_spec_only(Selected_spc, rat, band)
            #             Lsi_chng_rx_gain_spec_only(Selected_spc, rat, band)

        elif Selected_Option == 2:

            if list_file.size() == 0:
                msgbox.showwarning("경고", "Cal log 파일(*.csv)을 추가하세요")
                return

            df_Meas, df_Code = get_data(list_file.get(0, tk.END), Select_op, text_area)

            CableCheck = daseul_cable_average(df_Meas, Save_data_var)

            (
                FBRX_Gain_Meas_3G,
                FBRX_Gain_Meas_sub6,
                FBRX_Gain_Code_3G,
                FBRX_Gain_Code_sub6,
                FBRX_Freq_Meas_3G,
                FBRX_Freq_Meas_3G_Max,
                FBRX_Freq_Meas_3G_Min,
                FBRX_Freq_Meas_sub6,
                FBRX_Freq_Meas_sub6_Max,
                FBRX_Freq_Meas_sub6_Min,
                FBRX_Freq_Code_sub6,
                FBRX_Freq_Code_sub6_Max,
                FBRX_Freq_Code_sub6_Min,
            ) = fbrx_average(df_Meas, df_Code, Save_data_var)

            (
                PRX_Gain_2G,
                Ripple_2G,
                RXGain_3G,
                RXComp_3G,
                RXGain_sub6,
                RXRSRP_sub6,
                RXComp_sub6,
            ) = daseul_rx_average(df_Meas, Save_data_var)

            GMSK_Mean, GMSK_TXL_Mean, EPSK_Mean, EPSK_TXL_Mean = gsm_average(df_Meas, Save_data_var)

            (
                ETSAPT_3G_Psat_Ave,
                ETSAPT_3G_Psat_Max,
                ETSAPT_3G_Psat_Min,
                ETSAPT_3G_Power_Ave,
                ETSAPT_3G_Power_Max,
                ETSAPT_3G_Power_Min,
            ) = Et_3g_average(df_Meas, Save_data_var)

            APT_Meas_3G_Ave, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min = apt_average(
                df_Meas, Save_data_var
            )

            (
                ETSAPT_sub6_Psat_Ave,
                ETSAPT_sub6_Psat_Max,
                ETSAPT_sub6_Psat_Min,
                ETSAPT_sub6_Freq_Ave,
                ETSAPT_sub6_Freq_Max,
                ETSAPT_sub6_Freq_Min,
                ETSAPT_sub6_Pgain_Ave,
                ETSAPT_sub6_Pgain_Max,
                ETSAPT_sub6_Pgain_Min,
                ETSAPT_sub6_Power_Ave,
                ETSAPT_sub6_Power_Max,
                ETSAPT_sub6_Power_Min,
            ) = sub6_et_average(df_Meas, Save_data_var)

            L_cable.chng_cable_spec(Selected_spc, CableCheck, Cable_Spec_var, text_area)

            for rat in Test_List:
                for band in Test_List[rat]:
                    text_area.insert(tk.END, "=" * 65)
                    text_area.insert(tk.END, "\n\n")
                    text_area.insert(tk.END, f"{rat}, BAND = {band}\n\n")
                    text_area.see(tk.END)
                    if (rat == "SUB6") and (band in ["75"]):
                        L_sub6.chng_sub6_rx_gain(
                            Selected_spc,
                            rat,
                            band,
                            RX_Gain_Spec_var,
                            RXGain_sub6,
                            RXRSRP_sub6,
                            RXComp_sub6,
                            text_area,
                        )
                    elif rat == "GSM":
                        L_2g.chng_2g_rx_gain(
                            Selected_spc, band, RX_Gain_2G_Spec_var, PRX_Gain_2G, Ripple_2G, text_area
                        )
                        L_2g.chng_2g_tx(
                            Selected_spc,
                            band,
                            GMSK_Spec_var,
                            GMSK_Mean,
                            GMSK_TXL_Mean,
                            EPSK_Spec_var,
                            EPSK_Mean,
                            EPSK_TXL_Mean,
                            text_area,
                        )
                    elif rat == "HSPA":

                        L_3g.chng_3g_rx_gain(
                            Selected_spc, rat, band, RX_Gain_3G_Spec_var, RXGain_3G, RXComp_3G, text_area
                        )
                        L_3g.chng_3g_fbrx_gain_meas(
                            Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Meas_3G, text_area
                        )
                        L_3g.chng_3g_fbrx_gain_code(
                            Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Code_3G, text_area
                        )
                        L_3g.chng_3g_fbrx_freq_meas(
                            Selected_spc,
                            rat,
                            band,
                            FBRX_3G_Spec_var,
                            FBRX_Freq_Meas_3G,
                            FBRX_Freq_Meas_3G_Max,
                            FBRX_Freq_Meas_3G_Min,
                            text_area,
                        )
                        L_3g.chng_3g_apt(Selected_spc, rat, band, APT_Spec_var, APT_Meas_3G_Ave)
                        L_et.chng_3g_et_psat_pgain(
                            Selected_spc,
                            rat,
                            band,
                            ET_Psat_var,
                            ETSAPT_3G_Psat_Ave,
                            ETSAPT_3G_Psat_Max,
                            ETSAPT_3G_Psat_Min,
                            ET_Pgain_var,
                            ETSAPT_3G_Power_Ave,
                            ETSAPT_3G_Power_Max,
                            ETSAPT_3G_Power_Min,
                            text_area,
                        )

                    else:
                        text_area.insert(tk.END, f"RX GAIN Calibration\n")
                        text_area.see(tk.END)
                        L_sub6.chng_sub6_rx_gain(
                            Selected_spc,
                            rat,
                            band,
                            RX_Gain_Spec_var,
                            RXGain_sub6,
                            RXRSRP_sub6,
                            RXComp_sub6,
                            text_area,
                        )

                        text_area.insert(tk.END, f"FBRX GAIN Calibration\n")
                        text_area.see(tk.END)
                        L_sub6.chng_sub6_fbrx_gain_meas(
                            Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Meas_sub6, text_area
                        )
                        L_sub6.chng_sub6_fbrx_gain_code(
                            Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Code_sub6, text_area
                        )

                        text_area.insert(tk.END, f"FBRX FREQ Calibration\n")
                        text_area.see(tk.END)

                        L_sub6.chng_sub6_fbrx_freq_meas(
                            Selected_spc,
                            rat,
                            band,
                            FBRX_Spec_var,
                            FBRX_Freq_Meas_sub6,
                            FBRX_Freq_Meas_sub6_Max,
                            FBRX_Freq_Meas_sub6_Min,
                            text_area,
                        )
                        L_sub6.chng_sub6_fbrx_freq_code(
                            Selected_spc,
                            rat,
                            band,
                            FBRX_Spec_var,
                            FBRX_Freq_Code_sub6,
                            FBRX_Freq_Code_sub6_Max,
                            FBRX_Freq_Code_sub6_Min,
                            text_area,
                        )
                        L_sub6.chng_sub6_apt(
                            Selected_spc,
                            rat,
                            band,
                            APT_Spec_var,
                            APT_Meas_sub6_Ave,
                            APT_Meas_sub6_Max,
                            APT_Meas_sub6_Min,
                        )

                        text_area.insert(tk.END, f"ET-SAPT Calibration\n")
                        text_area.see(tk.END)

                        L_et.chng_sub6_et_psat_pgain(
                            Selected_spc,
                            rat,
                            band,
                            ET_Psat_var,
                            ETSAPT_sub6_Psat_Ave,
                            ETSAPT_sub6_Psat_Max,
                            ETSAPT_sub6_Psat_Min,
                            ET_Pgain_var,
                            ETSAPT_sub6_Pgain_Ave,
                            ETSAPT_sub6_Pgain_Max,
                            ETSAPT_sub6_Pgain_Min,
                            text_area,
                        )
                        L_et.chng_sub6_et_freq(
                            Selected_spc,
                            rat,
                            band,
                            ET_Freq_var,
                            ETSAPT_sub6_Freq_Ave,
                            ETSAPT_sub6_Freq_Max,
                            ETSAPT_sub6_Freq_Min,
                            text_area,
                        )
                        L_et.chng_sub6_et_power(
                            Selected_spc,
                            rat,
                            band,
                            ET_Power_var,
                            ETSAPT_sub6_Power_Ave,
                            ETSAPT_sub6_Power_Max,
                            ETSAPT_sub6_Power_Min,
                            text_area,
                        )

        elif Selected_Option == 3:

            if list_file.size() == 0:
                msgbox.showwarning("경고", "MTM log 파일(*.csv)을 추가하세요")
                return

            df_Meas, df_Code = get_data(list_file.get(0, tk.END), Select_op, text_area)
            (
                HSPA_RX_Gain_default,
                Sub6_RX_Gain_default,
                Sub6_RSRP_Offset_default,
            ) = mtm.Rx_gain_average_mtm(df_Meas, Save_data_var)
            GSM_RX_Gain_Default = mtm.Rx_2G_gain_average_mtm(df_Meas, Save_data_var)
            HSPA_RX_Freq_default, Sub6_RX_Freq_default = mtm.Rx_freq_average_mtm(df_Meas, Save_data_var)
            Sub6_RX_Mixer_default = mtm.Rx_mixer_average_mtm(df_Meas, Save_data_var)

            for rat in Test_List:
                for band in Test_List[rat]:
                    if rat == "HSPA":
                        L_3g.chng_3g_rx_gain_default(Selected_spc, rat, band, HSPA_RX_Gain_default, text_area)
                        L_3g.chng_3g_rx_freq_default(Selected_spc, rat, band, HSPA_RX_Freq_default, text_area)
                    elif rat == "GSM":
                        pass
                        # Chng_2G_TX(Selected_spc, band, FBRX_Meas_2G, TX_MaxP_2G)
                        # Chng_2G_RX_Gain(Selected_spc, band, RxGAIN_2G)
                    else:
                        L_sub6.chng_sub6_rx_gain_default(Selected_spc, rat, band, Sub6_RX_Gain_default, text_area)
                        L_sub6.chng_sub6_rsrp_offset_default(
                            Selected_spc, rat, band, Sub6_RSRP_Offset_default, text_area
                        )
                        L_sub6.chng_sub6_rx_freq_default(Selected_spc, rat, band, Sub6_RX_Freq_default, text_area)
                        L_sub6.chng_sub6_rx_mixer_default(Selected_spc, rat, band, Sub6_RX_Mixer_default, text_area)

        else:
            msgbox.showwarning("ERROR", "옵션을 선택하세요")
            return
    except FileNotFoundError as e:
        msgbox.showwarning("ERROR", e)

    msgbox.showwarning("Message", "작업 완료")
