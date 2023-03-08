import re
import numpy as np
import tkinter as tk
import math


def chng_cable_spec_only(Selected_spc, Cable_Spec_var, text_area):
    Cable_Spec = int(Cable_Spec_var.get())
    target_word = "[INSERT_RF_CABLE_CHECK]"
    new_text_content = ""
    Cable = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Cable = True
            new_text_content += line
        elif Cable & line.startswith("/////////"):
            New_String = Old_String = line
            Numofturn = re.sub(r"[^0-9]", "", New_String)
            Test_Path = re.split(f"Test Band{Numofturn}=|\n", data_lines[index + 1])
            Test_Path = ",".join([v for v in Test_Path if v])  # join으로 list -> to string
            path = "RX" if Test_Path == "SUB6_RX" else "TX"
            Test_Band = re.split(f"Band Number{Numofturn}=|\n", data_lines[index + 2])
            Test_Band = ",".join([v for v in Test_Band if v])
            Test_Freq = re.split(f"Test TxFreq{Numofturn}=|\n", data_lines[index + 3])
            Test_Freq = ",".join([v for v in Test_Freq if v])
            new_text_content += line
            continue

        elif Cable & line.startswith(f"LOWER_LIMIT"):
            New_String = Old_String = line
            New_String = re.split("=", New_String)
            New_String = [v for v in New_String if v]
            LOWER_LIMIT = New_String[1]
            UPPER_LIMIT = re.split(f"UPPER_LIMIT{Numofturn}=|\n", data_lines[index + 1])
            UPPER_LIMIT = ",".join([v for v in UPPER_LIMIT if v])
            Cable_Value = [float(LOWER_LIMIT), float(UPPER_LIMIT)]
            Cable_mean = np.mean(Cable_Value)
            New_String[1] = str(round(Cable_mean - Cable_Spec, 1))
            New_String = "=".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
            continue

        elif Cable & line.startswith(f"UPPER_LIMIT"):
            New_String = Old_String = line
            New_String = re.split("=", New_String)
            New_String = [v for v in New_String if v]
            New_String[1] = str(round(Cable_mean + Cable_Spec, 1))
            New_String = "=".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
            continue

        elif line == "[RF_CAL_VERIFY]\n":
            new_text_content += line
            Cable = False
        else:
            new_text_content += line

    text_area.insert(tk.END, f"[INSERT_RF_CABLE_CHECK]\n")
    text_area.see(tk.END)

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()


def chng_cable_spec(Selected_spc, CableCheck, Cable_Spec_var, text_area):
    Cable_Spec = int(Cable_Spec_var.get())
    target_word = "[INSERT_RF_CABLE_CHECK]"
    new_text_content = ""
    Check = False

    with open(Selected_spc, "r", encoding="utf-8") as f:
        data_lines = f.readlines()
    f.close()

    for index, line in enumerate(data_lines):
        if target_word in line:
            Check = True
            text_area.insert(tk.END, f"[INSERT_RF_CABLE_CHECK]\n")
            text_area.see(tk.END)
            new_text_content += line
        elif Check & line.startswith("/////////"):
            New_String = Old_String = line
            Numofturn = re.sub(r"[^0-9]", "", New_String)
            Test_Path = re.split(f"Test Band{Numofturn}=|\n", data_lines[index + 1])
            Test_Path = ",".join([v for v in Test_Path if v])  # join으로 list -> to string
            path = "RX" if Test_Path == "SUB6_RX" else "TX"
            Test_Band = re.split(f"Band Number{Numofturn}=|\n", data_lines[index + 2])
            Test_Band = ",".join([v for v in Test_Band if v])
            if Test_Band == "28":
                path = "2TX"
            Test_Freq = re.split(f"Test TxFreq{Numofturn}=|\n", data_lines[index + 3])
            Test_Freq = ",".join([v for v in Test_Freq if v])
            new_text_content += line
            continue
        elif Check & line.startswith(f"LOWER_LIMIT"):
            New_String = Old_String = line
            New_String = str(New_String).strip().split("=")
            New_String = [v for v in New_String if v]
            text_area.insert(tk.END, f"n{Test_Band:<2} Path= {path:>3}\n")
            text_area.see(tk.END)
            text_area.insert(tk.END, f"LOWER_LIMIT {Numofturn:<2}\t| {New_String[1]:>5}")
            text_area.see(tk.END)
            if Test_Freq:
                if int(Test_Freq) > 3000000:
                    arfcn = str(math.trunc(600000 + (int(Test_Freq) * 1000 - 3000000000) / 15000))
                    Average = round(CableCheck["NR", f"n{Test_Band}", path, arfcn])
                elif int(Test_Freq) <= 3000000:
                    arfcn = str(math.trunc((int(Test_Freq) * 1000) / 5000))
                    Average = round(CableCheck["NR", f"n{Test_Band}", path, arfcn])
            else:
                Average = round(CableCheck["NR", f"n{Test_Band}", path].iloc[0], 1)
            text_area.insert(tk.END, f"\t\u2192\t")
            New_String[1] = str(round(Average - Cable_Spec, 1))
            text_area.insert(tk.END, f"{New_String[1]:>5}\n")
            text_area.see(tk.END)
            New_String = "=".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
            continue

        elif Check & line.startswith(f"UPPER_LIMIT"):
            New_String = Old_String = line
            New_String = str(New_String).strip().split("=")
            New_String = [v for v in New_String if v]
            text_area.insert(tk.END, f"UPPER_LIMIT {Numofturn:<2}\t| {New_String[1]:>5}")
            text_area.insert(tk.END, f"\t\u2192\t")
            New_String[1] = str(round(Average + Cable_Spec, 1))
            text_area.insert(tk.END, f"{New_String[1]:>5}\n\n")
            text_area.see(tk.END)
            New_String = "=".join(New_String) + "\n"
            new_string = line.replace(Old_String, New_String)
            new_text_content += new_string
            continue

        elif line == "[RF_CAL_VERIFY]\n":
            new_text_content += line
            Check = False
        else:
            new_text_content += line

    with open(Selected_spc, "w", encoding="utf-8") as f:
        f.writelines(new_text_content)
    f.close()
