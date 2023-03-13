import re
import tkinter as tk


def chng_sub6_rx_gain(Selected_spc, rat, band, RX_Gain_Spec_var, RXGain_sub6, RXRSRP_sub6, RXComp_sub6, text_area):
    RX_Gain_Spec = int(RX_Gain_Spec_var.get())
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("RX_Gain_main_"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            gainstage = int(re.sub(r"[^0-9]", "", New_String[0])) - 1
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(RXGain_sub6[band, f"STAGE{gainstage}(-50.00dBm) "])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("RX_RsrpOffset_main_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            gainstage = int(re.sub(r"[^0-9]", "", New_String[0])) - 1
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(RXRSRP_sub6[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("RX_FreqOffset_prx_0"):
            New_String = Old_String = line
            New_String = re.split("\t|\n", New_String)
            New_String = [v for v in New_String if v]
            gainstage = int(re.sub(r"[^0-9]", "", New_String[0])) - 1
            text_area.insert(
                tk.END,
                f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
            )
            New_String[2] = round(RXComp_sub6[band])
            New_String[3] = New_String[2] - RX_Gain_Spec
            New_String[4] = New_String[2] + RX_Gain_Spec
            text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
            text_area.insert(tk.END, f"\n")
            text_area.see(tk.END)
            New_String = [str(v) for v in New_String]
            New_String = "\t".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line == "// TX FBRX\n":
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_sub6_fbrx_gain_meas(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Meas_sub6, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get())
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_FBRX_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_meas(line, band, FBRX_Spec, FBRX_Gain_Meas_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_FBRX_Pow_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_meas(line, band, FBRX_Spec, FBRX_Gain_Meas_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_gain_meas(line, band, FBRX_Spec, FBRX_Gain_Meas_sub6, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    gainstage = int(Word[4])
    text_area.insert(
        tk.END,
        f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
    )
    New_String[2] = round(FBRX_Gain_Meas_sub6["NR", band, Path, f"Index{gainstage} "])
    New_String[3] = New_String[2] - FBRX_Spec
    New_String[4] = New_String[2] + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_fbrx_gain_code(Selected_spc, rat, band, FBRX_Spec_var, FBRX_Gain_Code_sub6, text_area):
    FBRX_Spec = int(FBRX_Spec_var.get()) * 100  # 1dB = 100
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_FBRX_Code_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_code(line, band, FBRX_Spec, FBRX_Gain_Code_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_FBRX_Code_Index_"):
            New_String = Old_String = line
            New_String = sub6_fbrx_gain_code(line, band, FBRX_Spec, FBRX_Gain_Code_sub6, text_area)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_gain_code(line, band, FBRX_Spec, FBRX_Gain_Code_sub6, text_area):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    gainstage = int(Word[4])
    text_area.insert(
        tk.END,
        f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
    )
    New_String[2] = round(FBRX_Gain_Code_sub6["NR", band, Path, f"Index{gainstage} "])
    New_String[3] = New_String[2] - FBRX_Spec
    New_String[4] = New_String[2] + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_fbrx_freq_meas(
    Selected_spc,
    rat,
    band,
    FBRX_Spec_var,
    FBRX_Freq_Meas_sub6,
    FBRX_Freq_Meas_sub6_Max,
    FBRX_Freq_Meas_sub6_Min,
    text_area,
):
    FBRX_Spec = int(FBRX_Spec_var.get())
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Cable = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Cable = True
            new_text_content += line
        elif Cable & line.startswith("TX_FBRX_Channel_Pow"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_meas(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Meas_sub6,
                FBRX_Freq_Meas_sub6_Max,
                FBRX_Freq_Meas_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Cable & line.startswith("TX2_FBRX_Channel_Pow"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_meas(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Meas_sub6,
                FBRX_Freq_Meas_sub6_Max,
                FBRX_Freq_Meas_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Cable = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_freq_meas(
    line, band, FBRX_Spec, FBRX_Freq_Meas_sub6, FBRX_Freq_Meas_sub6_Max, FBRX_Freq_Meas_sub6_Min, text_area
):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    text_area.insert(
        tk.END,
        f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
    )
    New_String[2] = round(FBRX_Freq_Meas_sub6["NR", band, Path])
    New_String[3] = round(FBRX_Freq_Meas_sub6_Min["NR", band, Path]) - FBRX_Spec
    New_String[4] = round(FBRX_Freq_Meas_sub6_Max["NR", band, Path]) + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_fbrx_freq_code(
    Selected_spc,
    rat,
    band,
    FBRX_Spec_var,
    FBRX_Freq_Code_sub6,
    FBRX_Freq_Code_sub6_Max,
    FBRX_Freq_Code_sub6_Min,
    text_area,
):
    FBRX_Spec = int(FBRX_Spec_var.get()) * 100  # 1dB = 100
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_FBRX_Channel_Code"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_code(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Code_sub6,
                FBRX_Freq_Code_sub6_Max,
                FBRX_Freq_Code_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_FBRX_Channel_Code"):
            New_String = Old_String = line
            New_String = sub6_fbrx_freq_code(
                line,
                band,
                FBRX_Spec,
                FBRX_Freq_Code_sub6,
                FBRX_Freq_Code_sub6_Max,
                FBRX_Freq_Code_sub6_Min,
                text_area,
            )
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_APT_High_Gain_Index_0"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_fbrx_freq_code(
    line, band, FBRX_Spec, FBRX_Freq_Code_sub6, FBRX_Freq_Code_sub6_Max, FBRX_Freq_Code_sub6_Min, text_area
):
    New_String = re.split("\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    text_area.insert(
        tk.END,
        f"{New_String[0]:<30}       | {New_String[3]:>5}\t{New_String[4]:>5}\t\t\u2192\t",
    )
    New_String[2] = round(FBRX_Freq_Code_sub6["NR", band, Path])
    New_String[3] = round(FBRX_Freq_Code_sub6_Min["NR", band, Path]) - FBRX_Spec
    New_String[4] = round(FBRX_Freq_Code_sub6_Max["NR", band, Path]) + FBRX_Spec
    text_area.insert(tk.END, f"{New_String[3]:>5}\t{New_String[4]:>5}\n")
    text_area.see(tk.END)
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_apt(Selected_spc, rat, band, APT_Spec_var, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min):
    APT_Spec = float(APT_Spec_var.get())  # 1dB = 100
    band = f"n{band}"
    target_word = f"[{rat}_{band}_Calibration_Spec]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            new_text_content += line
        elif Check & line.startswith("TX_APT_"):
            New_String = Old_String = line
            New_String = sub6_apt(line, band, APT_Spec, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif Check & line.startswith("TX2_APT_"):
            New_String = Old_String = line
            New_String = sub6_apt(line, band, APT_Spec, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min)
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
        elif line.startswith("TX_DC_I"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_apt(line, band, APT_Spec, APT_Meas_sub6_Ave, APT_Meas_sub6_Max, APT_Meas_sub6_Min):
    New_String = re.split("=|\t|\n", line)
    New_String = [v for v in New_String if v]
    Word = re.split("_", New_String[0])
    Word = [v for v in Word if v]
    if Word[0] == "TX":
        Path = "Tx"
    elif Word[0] == "TX2":
        Path = "Tx2"
    Pa_stage = Word[2]
    values = [
        APT_Meas_sub6_Ave[band, Path, Pa_stage, f"Index{Word[5]} "],
        APT_Meas_sub6_Max[band, Path, Pa_stage, f"Index{Word[5]} "],
        APT_Meas_sub6_Min[band, Path, Pa_stage, f"Index{Word[5]} "],
    ]
    if all(v == -10.0 for v in values):
        New_String[2] = -10.1
        New_String[3] = -9.9
    else:
        New_String[1] = round(APT_Meas_sub6_Ave[band, Path, Pa_stage, f"Index{Word[5]} "])
        New_String[2] = New_String[1] - APT_Spec
        New_String[3] = New_String[1] + APT_Spec
    Word = "_".join(Word) + "\t" + "="
    New_String[0] = Word
    New_String = [str(v) for v in New_String]
    New_String = "\t".join(New_String) + "\n"

    return New_String


def chng_sub6_rx_gain_default(Selected_spc, rat, band, Sub6_RX_Gain_default, text_area):

    band = f"n{band}"
    target_word = f"[{rat}_{band}_CAL_PARAM]"
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
        elif Check & Not_Duplicated & line.startswith("Rx_4RX_CAL_EN=1"):
            enable_4RX = True
            Not_Duplicated = False
            new_text_content += line
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & enable_4RX & line.startswith(f"PRX_RxGAIN_4RX_Default_Value="):
            ant = "4RX"
            path = "PRX"
            New_String = sub6_rxgain_cal(line, band, ant, path, Sub6_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RxGAIN_MAIN_Default_Value="):
            ant = "MAIN"
            path = "DRX"
            New_String = sub6_rxgain_cal(line, band, ant, path, Sub6_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & enable_4RX & line.startswith(f"DRX_RxGAIN_4RX_Default_Value="):
            ant = "4RX"
            path = "DRX"
            New_String = sub6_rxgain_cal(line, band, ant, path, Sub6_RX_Gain_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
            enable_4RX = False
        elif Check & (line.startswith("// TX Cal Parameters")):
            new_text_content += line
            Check = False
        else:
            new_text_content += line
    text_area.see(tk.END)
    # text_area.insert(tk.END, f"Tech= {rat}  \t| Band= {band:<7}\t| Ant= {Antenna}\t| Path= {Path}\n")
    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rxgain_cal(line, band, ant, path, Sub6_RX_Gain_default, text_area):

    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{ant:<4} {path} GAIN  | ")
    for i in range(6):
        if i == 5:
            text_area.insert(tk.END, f"{New_String[5+i]:>5}")
        else:
            text_area.insert(tk.END, f"{New_String[5+i]:>5},")
    for i in range(6):
        New_String[5 + i] = round(Sub6_RX_Gain_default[band][ant][path][f"Stage{i}"] * 100)

    text_area.insert(tk.END, f" \u2192 ")
    for i in range(6):
        if i == 5:
            text_area.insert(tk.END, f"{New_String[5+i]:>5}")
        else:
            text_area.insert(tk.END, f"{New_String[5+i]:>5},")

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, New_String[:5]))
    New_String2 = ",".join(map(str, New_String[5:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_sub6_rsrp_offset_default(Selected_spc, rat, band, Sub6_RSRP_Offset_default, text_area):

    band = f"n{band}"
    target_word = f"[{rat}_{band}_CAL_PARAM]"
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
        elif Check & Not_Duplicated & line.startswith("Rx_4RX_CAL_EN=1"):
            enable_4RX = True
            Not_Duplicated = False
            new_text_content += line
        # Gainstate를 for로 할 경우 너무 많은 반복 -> if 문으로 처리
        elif Check & enable_4RX & line.startswith(f"PRX_RSRP_Offset_4RX_Default_Value="):
            ant = "4RX"
            path = "PRX"
            New_String = sub6_rsrp_offset(index, line, rat, band, ant, path, Sub6_RSRP_Offset_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RSRP_Offset_MAIN_Default_Value="):
            ant = "MAIN"
            path = "DRX"
            New_String = sub6_rsrp_offset(index, line, rat, band, ant, path, Sub6_RSRP_Offset_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & enable_4RX & line.startswith(f"DRX_RSRP_Offset_4RX_Default_Value="):
            ant = "4RX"
            path = "DRX"
            New_String = sub6_rsrp_offset(index, line, rat, band, ant, path, Sub6_RSRP_Offset_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
            enable_4RX = False
        elif Check & (line.startswith("// TX Cal Parameters")):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rsrp_offset(index, line, rat, band, ant, path, Sub6_RSRP_Offset_default, text_area):

    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{ant:<4} {path} RSRP  | ")
    text_area.insert(tk.END, f"{New_String[6]:>5}")
    New_String[6] = round(Sub6_RSRP_Offset_default[band][ant][path] * 100)
    text_area.insert(tk.END, f" \u2192 ")
    text_area.insert(tk.END, f"{New_String[6]:>5}")

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, New_String[:6]))
    New_String2 = ",".join(map(str, New_String[6:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_sub6_rx_freq_default(Selected_spc, rat, band, Sub6_RX_Freq_default, text_area):

    band = f"n{band}"
    target_word = f"[{rat}_{band}_CAL_PARAM]"

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
        elif Check & line.startswith("RX_FREQ_CAL_EN=1"):
            Freq_List = re.split("[=,\n]", data_lines[index + 2])[1:]
            Freq_List = [v for v in Freq_List if v]
            new_text_content += line
        elif Check & line.startswith("Rx_4RX_CAL_EN=1"):
            Enable_4RX = True
            new_text_content += line
        elif Check & line.startswith(f"PRX_RXFREQ_MAIN_Default="):
            ant = "MAIN"
            path = "PRX"
            New_String = sub6_rxfreq_cal(Freq_List, index, line, rat, band, ant, path, Sub6_RX_Freq_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_RXFREQ_MAIN_DEFAULT="):
            ant = "MAIN"
            path = "DRX"
            New_String = sub6_rxfreq_cal(Freq_List, index, line, rat, band, ant, path, Sub6_RX_Freq_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"PRX_RXFREQ_4RX_DEFAULT="):
            ant = "4RX"
            path = "PRX"
            New_String = sub6_rxfreq_cal(Freq_List, index, line, rat, band, ant, path, Sub6_RX_Freq_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"DRX_RXFREQ_4RX_DEFAULT="):
            ant = "4RX"
            path = "DRX"
            New_String = sub6_rxfreq_cal(Freq_List, index, line, rat, band, ant, path, Sub6_RX_Freq_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"// TX Cal Parameters"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rxfreq_cal(Freq_List, index, line, rat, band, ant, path, Sub6_RX_Freq_default, text_area):

    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    text_area.insert(tk.END, f"{ant:<4} {path} FREQ  | ")

    for i in range(len(New_String[4:])):
        if i == range(len(New_String[4:]))[-1]:
            text_area.insert(tk.END, f"{New_String[4+i]:>5}")
        else:
            text_area.insert(tk.END, f"{New_String[4+i]:>5},")

    del New_String[4:]
    # Freq_List 길이만큼 0 으로 채워넣기 하고 값을 변경
    for i in range(len(Freq_List)):
        New_String.append(0)
        New_String[4 + i] = round(Sub6_RX_Freq_default[band][ant][path][Freq_List[i]] * 100)

    text_area.insert(tk.END, f" \u2192 ")
    for i in range(len(Freq_List)):
        if i == range(len(Freq_List))[-1]:
            text_area.insert(tk.END, f"{New_String[4+i]:>5}")
        else:
            text_area.insert(tk.END, f"{New_String[4+i]:>5},")

    text_area.insert(tk.END, f"\n")
    text_area.see(tk.END)
    New_String1 = "_".join(map(str, New_String[:4]))
    New_String2 = ",".join(map(str, New_String[4:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String


def chng_sub6_rx_mixer_default(Selected_spc, rat, band, Sub6_RX_Mixer_default, text_area):
    band = f"n{band}"
    target_word = f"[{rat}_{band}_CAL_PARAM]"

    new_text_content = ""
    Check = False
    Enable_4RX = False

    with open(Selected_spc, "r", encoding="utf-8") as file:
        data_lines = file.readlines()
    file.close()
    # band별 Mixer 갯수 구하기
    # Mixer = Sub6_RX_Mixer_default.reset_index().groupby("Band")['Mixer'].nunique().loc[band]
    Mixer_list = Sub6_RX_Mixer_default[band].index.get_level_values("Mixer").tolist()
    Mixer = list(dict.fromkeys(Mixer_list))  # list 중복 제거

    for index, line in enumerate(data_lines):
        New_String = Old_String = line
        if line.startswith(target_word):
            new_text_content += line
            Check = True
        elif Check & line.startswith("RX_Mixer_Cal_mode="):
            Mixer_Cal_mode = int(re.sub(r"[^0-9]", "", line)[0])
            new_text_content += line
            if Mixer_Cal_mode == 3:
                Enable_4RX = True
            elif Mixer_Cal_mode == 1:
                Enable_4RX = False
            elif Mixer_Cal_mode == 0:
                Check = False
        elif Check & line.startswith(f"PRX_MIXER_RSRP_Offset_MAIN_Default_Value="):
            ant = "MAIN"
            path = "PRX"
            New_String = sub6_rx_mixer_cal(index, line, rat, ant, band, Mixer, path, Sub6_RX_Mixer_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & line.startswith(f"DRX_MIXER_RSRP_Offset_MAIN_Default_Value="):
            ant = "MAIN"
            path = "DRX"
            New_String = sub6_rx_mixer_cal(index, line, rat, ant, band, Mixer, path, Sub6_RX_Mixer_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"PRX_MIXER_RSRP_Offset_4RX_Default_Value="):
            ant = "4RX"
            path = "PRX"
            New_String = sub6_rx_mixer_cal(index, line, rat, ant, band, Mixer, path, Sub6_RX_Mixer_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif Check & Enable_4RX & line.startswith(f"DRX_MIXER_RSRP_Offset_4RX_Default_Value="):
            ant = "4RX"
            path = "DRX"
            New_String = sub6_rx_mixer_cal(index, line, rat, ant, band, Mixer, path, Sub6_RX_Mixer_default, text_area)
            Change_Str = line.replace(Old_String, New_String)
            new_text_content += Change_Str
        elif line.startswith(f"// TX Cal Parameters"):
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def sub6_rx_mixer_cal(index, line, rat, ant, band, Mixer, path, Sub6_RX_Mixer_default, text_area):

    New_String = re.split("[_=,\n]", line)
    New_String = [v for v in New_String if v]
    Mixer_no = []
    Old_Mixer_no = New_String[7::2]
    Old_Value = New_String[8::2]

    if ant == "MAIN":
        count = 0
        # spc 파일의 default cal mixer 갯수와 실제 캘된 mixer 갯수가 다를 수 있기 때문에 mixer 데이터를 삭제하고
        del New_String[7:]
        # Main ant의 mixer 넘버를 Mixer_no에 저장하고
        for i in Mixer:
            if len(i) == 2:
                Mixer_no.append(i)
        # Mixer_no의 길이만큼 0 으로 채워넣기 한다.
        for i in range(len(Mixer_no)):
            New_String.append(0)
            New_String.append(0)

        New_Mixer_no = New_String[7::2]
        New_Value = New_String[8::2]
        text_area.insert(tk.END, f"{ant:<4} {path} MIXER")
        for i in Mixer_no:
            if count > (len(Old_Mixer_no) - 1):
                Old_Mixer_no.append(0)
                Old_Value.append(0)
            text_area.insert(tk.END, f" | {Old_Mixer_no[count]:>3} {Old_Value[count]:>4}")
            New_Mixer_no[count] = str(i)
            New_Value[count] = str(round(Sub6_RX_Mixer_default[band, i, path] * 100))
            text_area.insert(tk.END, f" \u2192 ")
            text_area.insert(tk.END, f"{New_Mixer_no[count]:>3} {New_Value[count]:>4}\n")
            if i == Mixer_no[-1]:
                pass
            else:
                text_area.insert(tk.END, f"              ")
            count += 1
        text_area.see(tk.END)

    elif ant == "4RX":
        count = 0
        # spc 파일의 default cal mixer 갯수와 실제 캘된 mixer 갯수가 다를 수 있기 때문에 mixer 데이터를 삭제하고
        del New_String[7:]
        # Main ant의 mixer 넘버를 Mixer_no에 저장하고
        for i in Mixer:
            if len(i) == 3:
                Mixer_no.append(i)
        # Mixer_no의 길이만큼 0 으로 채워넣기 한다.
        for i in range(len(Mixer_no)):
            New_String.append(0)
            New_String.append(0)

        New_Mixer_no = New_String[7::2]
        New_Value = New_String[8::2]
        text_area.insert(tk.END, f"{ant:<4} {path} MIXER")
        for i in Mixer_no:
            if count > (len(Old_Mixer_no) - 1):
                Old_Mixer_no.append(0)
                Old_Value.append(0)
            text_area.insert(tk.END, f" | {Old_Mixer_no[count]:>3} {Old_Value[count]:>4}")
            New_Mixer_no[count] = str(i)
            New_Value[count] = str(round(Sub6_RX_Mixer_default[band, i, path] * 100))
            text_area.insert(tk.END, f" \u2192 ")
            text_area.insert(tk.END, f"{New_Mixer_no[count]:>3} {New_Value[count]:>4}\n")
            if i == Mixer_no[-1]:
                pass
            else:
                text_area.insert(tk.END, f"              ")
            count += 1
        text_area.see(tk.END)
    New_String[7::2] = New_Mixer_no
    New_String[8::2] = New_Value
    New_String1 = "_".join(map(str, New_String[:7]))
    New_String2 = ",".join(map(str, New_String[7:]))
    New_String = New_String1 + "=" + New_String2 + "\n"

    return New_String
