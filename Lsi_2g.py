import re
import tkinter as tk


def chng_2g_tx(
    Selected_spc,
    band,
    GMSK_Spec_var,
    GMSK_Mean,
    GMSK_TXL_Mean,
    EPSK_Spec_var,
    EPSK_Mean,
    EPSK_TXL_Mean,
    text_area,
):
    GMSK_Spec = int(GMSK_Spec_var.get())
    EPSK_Spec = int(EPSK_Spec_var.get())
    target_word = f"[{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False
    Param = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    (
        HPM_Index,
        MPM_Index,
        LPM_Index,
        ULPM_Index,
        EPSK_HPM_Index,
        EPSK_MPM_Index,
        EPSK_LPM_Index,
        EPSK_ULPM_Index,
        MPM,
        LPM,
        ULPM,
        EPSK_MPM,
        EPSK_LPM,
        EPSK_ULPM,
    ) = GSM_Params(band, data_lines)

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("GMSK_Ref_Power"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("Power", New_String[0])
            Word = [v for v in Word if v]
            Index_N = int(Word[1])
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            if Index_N in [0, 1, 2, 3]:
                gain = "HPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][HPM_Index[Index_N]])
            elif Index_N in [4]:
                gain = "HPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            elif MPM & (Index_N in [5, 6]):
                gain = "MPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][MPM_Index[Index_N - 5]])
            elif MPM & (Index_N in [7]):
                gain = "MPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            elif LPM & (Index_N in [8, 9]):
                gain = "LPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][LPM_Index[Index_N - 8]])
            elif LPM & (Index_N in [10]):
                gain = "LPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            elif ULPM & (Index_N in [11, 12]):
                gain = "ULPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain][ULPM_Index[Index_N - 11]])
            elif ULPM & (Index_N in [13]):
                gain = "ULPM"
                New_String[2] = round(GMSK_Mean[band, "GMSK", gain]["Index"])
            else:
                New_String[2] = 0
            New_String[3] = New_String[2] - GMSK_Spec
            New_String[4] = New_String[2] + GMSK_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            Word = "Power".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("GMSK_Power_TxL"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = str(round(GMSK_TXL_Mean[band, Word[2]]) - 2)
            New_String[3] = str(round(GMSK_TXL_Mean[band, Word[2]]) + 2)
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("EPSK_Ref_Power"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("Power", New_String[0])
            Word = [v for v in Word if v]
            Index_N = int(Word[1])
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            if Index_N in [0, 1, 2, 3]:
                gain = "HPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_HPM_Index[Index_N]])
            elif (EPSK_MPM == True or EPSK_LPM == True or EPSK_ULPM == True) & (Index_N in [4]):
                gain = "HPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            elif EPSK_MPM & (Index_N in [5, 6]):
                gain = "MPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_MPM_Index[Index_N - 5]])
            elif EPSK_MPM & (Index_N in [7]):
                gain = "MPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            elif EPSK_LPM & (Index_N in [8, 9]):
                gain = "LPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_LPM_Index[Index_N - 8]])
            elif EPSK_LPM & (Index_N in [10]):
                gain = "LPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            elif EPSK_ULPM & (Index_N in [11, 12]):
                gain = "ULPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain][EPSK_ULPM_Index[Index_N - 11]])
            elif EPSK_ULPM & (Index_N in [13]):
                gain = "ULPM"
                New_String[2] = round(EPSK_Mean[band, "EPSK", gain]["Index"])
            else:
                New_String[2] = 0
            New_String[3] = New_String[2] - EPSK_Spec
            New_String[4] = New_String[2] + EPSK_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            Word = "Power".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("EPSK_Power_TxL"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = str(round(EPSK_TXL_Mean[band, Word[2]]) - 2)
            New_String[3] = str(round(EPSK_TXL_Mean[band, Word[2]]) + 2)
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def GSM_Params(band, data_lines):
    target_word = f"[{band}_Calibration_Parameter]"
    Param = False
    MPM = LPM = ULPM = True
    for index, line in enumerate(data_lines):
        if target_word in line:
            Param = True
        elif Param & line.startswith("Tx_PAMAPTGainMode_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            Gainmode = New_String[1:]
            if Gainmode[1] == "0":
                MPM = False
            if Gainmode[2] == "0":
                LPM = False
            if Gainmode[3] == "0":
                ULPM = False
        elif Param & line.startswith("Tx_APT_HPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            HPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_MPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            MPM_Index = New_String[1:3]
        elif Param & line.startswith("Tx_APT_LPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            LPM_Index = New_String[1:3]
        elif Param & line.startswith("Tx_APT_ULPM_CalIndex_GMSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            ULPM_Index = New_String[1:3]
        elif Param & line.startswith("Tx_PAMAPTGainMode_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            Gainmode = New_String[1:]
            if Gainmode[1] == "0":
                EPSK_MPM = False
            if Gainmode[2] == "0":
                EPSK_LPM = False
            if Gainmode[3] == "0":
                EPSK_ULPM = False
        elif Param & line.startswith("Tx_APT_HPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_HPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_MPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_MPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_LPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_LPM_Index = New_String[1:5]
        elif Param & line.startswith("Tx_APT_ULPM_CalIndex_EPSK="):
            New_String = re.split("=|,| |//|\n", line)
            New_String = [v for v in New_String if v]
            EPSK_ULPM_Index = New_String[1:5]
        elif line.startswith("EPSK_FineTxCal="):
            Param = False

    return (
        HPM_Index,
        MPM_Index,
        LPM_Index,
        ULPM_Index,
        EPSK_HPM_Index,
        EPSK_MPM_Index,
        EPSK_LPM_Index,
        EPSK_ULPM_Index,
        MPM,
        LPM,
        ULPM,
        EPSK_MPM,
        EPSK_LPM,
        EPSK_ULPM,
    )


def chng_2g_rx_gain(Selected_spc, band, RX_Gain_2G_Spec_var, PRX_Gain_2G, Ripple_2G, text_area):
    RX_Gain_Spec = int(RX_Gain_2G_Spec_var.get())  # 1dB = 100
    target_word = f"[{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("Rx_AGCOffset_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = round(PRX_Gain_2G[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("Rx_Ripple"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[2]:>5}\t{New_String[3]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[3] = round(Ripple_2G[band]) + 2
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("GMSK_Ref_Power0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()
