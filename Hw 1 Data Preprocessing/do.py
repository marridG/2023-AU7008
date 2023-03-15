import pandas as pd
import numpy as np
from prettytable import PrettyTable, MARKDOWN
from scipy.stats import chi2_contingency

IN_DATA_PATH = "./data/data.xlsx"

df = pd.read_excel(IN_DATA_PATH, sheet_name=0)

# print(df.head())
# data_sex = df["性别\n（1 for male；0 for female）"]
# data_sleep = df["平均睡眠时间 \n(>6.5小时）"]
# data_salary = df["薪资\n（元）"]
# print(data_sex, data_sleep, data_salary)

data = df.to_numpy()  # (N, 4)
# print(data.shape)

# independent chi^2 value
print(r"Parsing Data & Calculate Independent \chi^2 Value ...")
_ref_male = np.where(1 == data[:, 1])
_ref_female = np.where(0 == data[:, 1])
_cnt_male, _cnt_female = len(_ref_male[0]), len(_ref_female[0])
_sleep_male = np.sum(data[_ref_male][:, 2])
_sleep_female = np.sum(data[_ref_female][:, 2])
chi_data = [
    [_sleep_male, _cnt_male - _sleep_male, _cnt_male],
    [_sleep_female, _cnt_female - _sleep_female, _cnt_female]
]  # [ [male-sleep-gt, male-sleep-gte, male_total], [female-sleep-gt, female-sleep-gte, female_total],]
# parsed data visualization
tbl = PrettyTable()
tbl.set_style(MARKDOWN)
tbl.field_names = ["性别", "睡眠时间 >6.5h", "睡眠时间 <=6.5h", "总计", ]
tbl.add_row(["男", ] + chi_data[0])
tbl.add_row(["女", ] + chi_data[1])
print("===> Parsed")
print(tbl)
res_chi2 = chi2_contingency(chi_data)
print("===> Result")
tbl.clear()
tbl.field_names = ["卡方值", "p 值", "自由度", "期望频数", ]
tbl.add_row(res_chi2)
# tbl.add_row([res_chi2.statistic, res_chi2.pvalue, res_chi2.dof, res_chi2.expected_freq, ])
print(tbl)
print()

# (0,1) Norm + 0-mean Norm
print(r"Applying (0,1) Norm ...")
salary_data = data[:, 3]
_salary_max, _salary_min = np.max(salary_data), np.min(salary_data)
res_salary_01_norm = (salary_data - _salary_min) * 1. / (_salary_max - _salary_min)
print("Result ===>\n\t%r" % res_salary_01_norm)
print(r"Applying 0-mean Norm ...")
res_salary_0_std_norm = (salary_data - np.mean(salary_data)) * 1. / np.std(salary_data)
print("Result ===>\n\t%r" % res_salary_0_std_norm)
