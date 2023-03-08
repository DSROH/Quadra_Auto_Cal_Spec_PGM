import re
import tkinter as tk


def chng_3g_rx_gain_default(Selected_spc, rat, band, HSPA_RX_Gain_default, text_area):
    target_word = f"[{rat}_BAND{band}_CAL_PARAM]"
    text_area.insert(tk.END, f"\n{target_word}\n")
    text_area.see(tk.END)
    new_text_content = ""
    Not_Duplicated = True
    Check = False
    enable_4RX = False

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        New_String = Old_String = line

        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & Not_Duplicated & line.startswith("4RX_Cal_Mode="):
            Diversity = re.split("=| |//", line)
            if Diversity[1] == "3":
                enable_4RX = True
            Not_Duplicated = False
            new_text_content += line
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & line.startswith(f"RX_Gain_DRX_Default_LNAOn="):
            ant = "Main"
            path = "DRX"
            Position = 5
            New_String = Rxgain_3g_cal(index, line, rat, band, ant, path, Position, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"RX_Gain_DRX_Default_LNAOn2="):
            ant = "Main"
            path = "DRX"
            Position = 5
            New_String = Rxgain_3g_cal(index, line, rat, band, ant, path, Position, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"RX_Gain_DRX_Default_BypassLNA="):
            ant = "Main"
            path = "DRX"
            Position = 5
            New_String = Rxgain_3g_cal(index, line, rat, band, ant, path, Position, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & enable_4RX & line.startswith(f"RX_Gain_4RX(PRX)Default="):
            ant = "4RX"
            path = "PRX"
            Position = 3
            New_String = Rxgain_3g_cal(index, line, rat, band, ant, path, Position, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & enable_4RX & line.startswith(f"RX_Gain_4RX(DRX)Default="):
            ant = "4RX"
            path = "DRX"
            Position = 3
            New_String = Rxgain_3g_cal(index, line, rat, band, ant, path, Position, HSPA_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
            enable_4RX = False
        elif Check & (line.startswith("ET_MODE")):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    # text_area.insert(tk.END, f"Tech= {rat}  \t| Band= {band:<7}\t| Ant= {Antenna}\t| Path= {Path}\n")
    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def Rxgain_3g_cal(index, line, rat, band, ant, path, Position, HSPA_RX_Gain_default, text_area):
    band = f"WB{band}"
    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{ant:<4} {path} GAIN  | ")
    text_area.insert(tk.END, f"{New_String[Position]:>5},")
    text_area.see(tk.END)

    New_String[Position] = round(HSPA_RX_Gain_default[band][ant][path]) * 256

    text_area.insert(tk.END, f" \u2192 ")
    text_area.insert(tk.END, f"{New_String[Position]:>5}")
    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, New_String[:Position]))
    New_String = New_String1 + "=" + str(New_String[Position]) + "\n"

    return New_String


def chng_3g_rx_freq_default(Selected_spc, rat, band, HSPA_RX_Freq_default, text_area):
    target_word = f"[{rat}_BAND{band}_CAL_PARAM]"
    new_text_content = ""
    Check = False
    Enable_4RX = False

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()

    for index, line in enumerate(data_lines):
        New_String = Old_String = line

        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & line.startswith("RX_Comp_Ch="):
            Freq_List = re.split("[=,\n]", line)[1:]
            Freq_List = [v for v in Freq_List if v]
            new_text_content += line
        elif Check & line.startswith("4RX_Cal_Mode="):
            Diversity = re.split("=| |//", line)
            if Diversity[1] == "3":
                Enable_4RX = True
            new_text_content += line
        elif Check & line.startswith(f"RX_Comp_DRX_Default="):
            ant = "Main"
            path = "PRX"
            Position = 4
            New_String = Rxfreq_3g_cal(
                Freq_List, index, line, rat, band, ant, path, Position, HSPA_RX_Freq_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RXFREQ_MAIN_DEFAULT="):
            ant = "Main"
            path = "DRX"
            Position = 4
            New_String = Rxfreq_3g_cal(
                Freq_List, index, line, rat, band, ant, path, Position, HSPA_RX_Freq_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"RX_Comp_4RX(PRX)Default="):
            ant = "4RX"
            path = "PRX"
            Position = 3
            New_String = Rxfreq_3g_cal(
                Freq_List, index, line, rat, band, ant, path, Position, HSPA_RX_Freq_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"RX_Comp_4RX(DRX)Default="):
            ant = "4RX"
            path = "DRX"
            Position = 3
            New_String = Rxfreq_3g_cal(
                Freq_List, index, line, rat, band, ant, path, Position, HSPA_RX_Freq_default, text_area
            )
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"ET_MODE"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def Rxfreq_3g_cal(Freq_List, index, line, rat, band, ant, path, Position, HSPA_RX_Freq_default, text_area):
    band = f"WB{band}"
    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{ant:<4} {path} FREQ  | ")
    text_area.see(tk.END)

    for i in range(len(New_String[Position:])):
        if i == range(len(New_String[Position:]))[-1]:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5}")
            text_area.see(tk.END)
        else:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5},")
            text_area.see(tk.END)

    del New_String[Position:]
    text_area.insert(tk.END, f" \u2192 ")
    # Freq_List 길이만큼 0 으로 채워넣기 하고 값을 변경
    for i in range(len(Freq_List)):
        New_String.append(0)
        New_String[Position + i] = round(HSPA_RX_Freq_default[band][ant][path][Freq_List[i]]) * 256

    for i in range(len(Freq_List)):
        if i == range(len(Freq_List))[-1]:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5}")
            text_area.see(tk.END)
        else:
            text_area.insert(tk.END, f"{New_String[Position+i]:>5},")
            text_area.see(tk.END)

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, New_String[:Position]))
    New_String2 = ",".join(map(str, New_String[Position:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_3g_rx_gain(Selected_spc, rat, band, RX_Gain_3G_Spec_var, RXGain_3G, RxComp_3G, text_area):
    RX_Gain_Spec = int(RX_Gain_3G_Spec_var.get())  # 1dB = 100
    target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
    band = f"B{band}"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("AGC_Rx1_LNAON_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", line)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = round(RXGain_3G[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("AGC_Rx1_Ch_LNAON_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            Read_index = int(Word[4])
            Index_count = RxComp_3G.loc[(band)].count()
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            if Read_index < Index_count:
                New_String[2] = round(RxComp_3G[band][Read_index])
                New_String[3] = New_String[2] - RX_Gain_Spec
                New_String[4] = New_String[2] + RX_Gain_Spec
            else:
                New_String[2] = 0
                New_String[3] = New_String[2] - RX_Gain_Spec
                New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            Word = "_".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_PA_LOW_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_fbrx_gain_meas(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Meas_3G, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get())  # 1dB = 100
    target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
    band = f"B{band}"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_FBRX_GAIN_Index_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            Word = re.split("_", New_String[0])
            Word = [v for v in Word if v]
            Read_index = int(Word[4])
            Index_count = FBRX_Gain_Meas_3G.loc[("WCDMA", band)].count()
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            if Read_index < Index_count:
                New_String[2] = round(FBRX_Gain_Meas_3G["WCDMA", band][Read_index])
                New_String[3] = New_String[2] - FBRX_Spec
                New_String[4] = New_String[2] + FBRX_Spec
            else:
                New_String[2] = 0
                New_String[3] = New_String[2] - FBRX_Spec
                New_String[4] = New_String[2] + FBRX_Spec
            text_area.insert(tk.END, f"{New_String[2]:>5}\t{New_String[3]:>5}\n")
            text_area.see(tk.END)
            Word = "_".join(Word)
            New_String[0] = Word
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("AGC_Rx1_LNAON_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_fbrx_gain_code(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Code_3G, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get()) * 100  # 1dB = 100
    target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
    band = f"B{band}"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_Modulation_FBRX_Result"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            text_area.see(tk.END)
            New_String[2] = round(FBRX_Gain_Code_3G["WCDMA", band][0])
            New_String[3] = New_String[2] - FBRX_Spec
            New_String[4] = New_String[2] + FBRX_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("AGC_Rx1_LNAON_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_fbrx_freq_meas(
    Selected_spc,
    rat,
    band,
    FBRX_3G_Spec_var,
    FBRX_Freq_Meas_3G,
    FBRX_Freq_Meas_3G_Max,
    FBRX_Freq_Meas_3G_Min,
    text_area,
):
    FBRX_Spec = int(FBRX_3G_Spec_var.get())  # 1dB = 100
    target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
    band = f"B{band}"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_FBRX_FREQ	="):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(FBRX_Freq_Meas_3G["WCDMA", band])
            New_String[3] = New_String[2] - FBRX_Spec
            New_String[4] = New_String[2] + FBRX_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX_FBRX_FREQ_RIPPLE	="):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(FBRX_Freq_Meas_3G_Max["WCDMA", band]) - round(FBRX_Freq_Meas_3G_Min["WCDMA", band])
            New_String[3] = 0
            New_String[4] = New_String[2] + 3
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("AGC_Rx1_LNAON_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_3g_apt(Selected_spc, rat, band, APT_Spec_var, APT_Meas_3G_Ave):
    APT_Spec = float(APT_Spec_var.get())  # 1dB = 100
    target_word = f"[{rat}_BAND{band}_Calibration_Spec]"
    band = f"B{band}"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_APT_PA_"):
            New_String = Old_String = line
            New_String = apt_3g(line, band, APT_Spec, APT_Meas_3G_Ave)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TxP_Channel_Comp_PA_MID_"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def apt_3g(line, band, APT_Spec, APT_Meas_NR_Ave):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    Pa_stage = Word[3]
    Read_index = int(Word[5])
    Index_count = APT_Meas_NR_Ave.loc[(band, Pa_stage)].count()
    if Read_index < Index_count:
        New_String[1] = round(APT_Meas_NR_Ave[band, Pa_stage][Read_index])
        New_String[2] = round(APT_Meas_NR_Ave[band, Pa_stage][Read_index]) - APT_Spec
        New_String[3] = round(APT_Meas_NR_Ave[band, Pa_stage][Read_index]) + APT_Spec
    else:
        New_String[1] = -10
        New_String[2] = New_String[1] - 0.1
        New_String[3] = New_String[1] + 0.1
    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String
