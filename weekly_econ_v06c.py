import pandas as pd
import pandas_datareader as pdr
import datetime
import os
import econ_helper_functions_v6c as ehf
import matplotlib

# Global variables:
print('hi_1a')
cwd = os.getcwd()
now = datetime.datetime.now()
dtime_string = now.strftime("%Y-%m-%d-%H-%M-%S")

# Retrieve econ artifacts that interest us:
df_usa_inf, plot_usa_inf, most_recent_usa_inf, \
df_usa_inf_yoy, df_usa_inf_mom, df_usa_inf_mom_ann, \
dir_to_send \
    = ehf.get_usa_inflation_objects()
df_uk_inf, plot_uk_inf, most_recent_uk_inf = ehf.get_uk_inflation_objects()
df_eq_sup, plot_eq_sup, most_recent_eq_sup, \
us_equities_billions, us_debt_billions = ehf.get_equity_supply_objects()
df_usa_unemp, plot_usa_unemp, most_recent_usa_unemp = ehf.get_usa_unemployment_objects()
df_gdp, plot_gdp, most_recent_gdp, \
    df_usa_mkt_cap_to_gdp, df_gdp_trillions = ehf.get_gdp_objects()


# This string "most_recent_data_points" will be a concatenation
# of the data sets we care about:
most_recent_data_points = []

# Load email credentials from separate directory:
cred_dir = cwd + str('\\Credentials\\gmail_credentials.csv')
csv_credentials = pd.read_csv(cred_dir, header=None)
gmail_username = csv_credentials.iloc[0, 0]
gmail_pw = csv_credentials.iloc[1, 0]
to_address_list = []  # fill this in from txt/csv to be loaded

stats_text_B = str('----- TOP LINE STATS: -----') + \
               str('<br>') + str('<br>') + \
               str('Equity Allocation: ') + str(round(df_eq_sup.iloc[-1], 4)) + \
               str('<br>') + \
               str('US Equities, $Billions: ') + str(round(us_equities_billions.iloc[-1], 4)) + \
               str('<br>') + \
               str('US Cash+Bonds, $Billions: ') + str(round(us_debt_billions.iloc[-1], 4)) + \
               str('<br>') + \
               str('Timestamp: ') + str(df_eq_sup.index[-1]) + \
               str('<br>') + str('<br>') + \
               str('CPI [All NSA, All SA, LFE NSA, LFE SA] : ') + \
               str('<br>') + \
               str('YoY: ') + str(round(df_usa_inf_yoy.iloc[-1, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-1, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-1, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-1, 3], 4)) + \
               str('<br>') + \
               str('MoM: ') + str(round(df_usa_inf_mom.iloc[-1, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-1, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-1, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-1, 3], 4)) + \
               str('<br>') + \
               str('MoM Ann: ') + str(round(df_usa_inf_mom_ann.iloc[-1, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-1, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-1, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-1, 3], 4)) + \
               str('<br>') + \
               str('CPI Timestamp: ') + str(df_usa_inf.index[-1]) + \
               str('<br>') + str('<br>') + \
               str('USA Unemployment. [U3, U6] : ') +\
               str(round(df_usa_unemp.iloc[-1, 0], 4)) + str(" ; ") + \
               str(round(df_usa_unemp.iloc[-1, 1], 4)) + \
               str('<br>') + \
               str('U3/U6 Timestamp: ') + str(df_usa_unemp.index[-1]) + \
               str('<br>') + str('<br>') + \
               str('GDP Trillions of Local Currency: ') + \
               str('<br>') + \
               str('[USA, CHN, JPN, GERM, UK] : ') + \
               str('<br>') + \
               str(round(df_gdp_trillions.iloc[-1, 0], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-1, 1], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-1, 2], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-1, 3], 3)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-1, 4], 3)) + str("") + \
               str('<br>') + \
               str('GDP Timestamp: ') + str(df_gdp_trillions.index[-1]) + \
               str('<br>') + str('<br>') + \
               str('') + \
               str('') + \
               str('----- PREVIOUS MONTH STATS: -----') + \
               str('') + \
               str('') + \
               str('<br>') + str('<br>') + \
               str('CPI [All NSA, All SA, LFE NSA, LFE SA] : ') + \
               str('<br>') + \
               str('YoY: ') + str(round(df_usa_inf_yoy.iloc[-2, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-2, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-2, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-2, 3], 4)) + \
               str('<br>') + \
               str('MoM: ') + str(round(df_usa_inf_mom.iloc[-1, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-2, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-2, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-2, 3], 4)) + \
               str('<br>') + \
               str('MoM Ann: ') + str(round(df_usa_inf_mom_ann.iloc[-1, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-2, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-2, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-2, 3], 4)) + \
               str('<br>') + \
               str('CPI Timestamp: ') + str(df_usa_inf.index[-2]) + \
               str('<br>') + str('<br>') + \
               str('USA Unemployment. [U3, U6] : ') + \
               str(round(df_usa_unemp.iloc[-2, 0], 4)) + str(" ; ") + \
               str(round(df_usa_unemp.iloc[-2, 1], 4)) + \
               str('<br>') + \
               str('U3/U6 Timestamp: ') + str(df_usa_unemp.index[-2]) + \
               str('<br>') + str('<br>') + \
               str('') + \
               str('') + \
               str('') + \
               str('') + \
               str('----- PREVIOUS QUARTER STATS: -----') + \
               str('') + \
               str('') + \
               str('<br>') + str('<br>') + \
               str('Equity Allocation: ') + str(round(df_eq_sup.iloc[-2], 4)) + \
               str('<br>') + \
               str('US Equities, $Billions: ') + str(round(us_equities_billions.iloc[-2], 4)) + \
               str('<br>') + \
               str('US Cash+Bonds, $Billions: ') + str(round(us_debt_billions.iloc[-2], 4)) + \
               str('<br>') + \
               str('Timestamp: ') + str(df_eq_sup.index[-2]) + \
               str('<br>') + str('<br>') + \
               str('CPI [All NSA, All SA, LFE NSA, LFE SA] : ') + \
               str('<br>') + \
               str('YoY: ') + str(round(df_usa_inf_yoy.iloc[-4, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-4, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-4, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-4, 3], 4)) + \
               str('<br>') + \
               str('MoM: ') + str(round(df_usa_inf_mom.iloc[-4, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-4, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-4, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-4, 3], 4)) + \
               str('<br>') + \
               str('MoM Ann: ') + str(round(df_usa_inf_mom_ann.iloc[-4, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-4, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-4, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-4, 3], 4)) + \
               str('<br>') + \
               str('CPI Timestamp: ') + str(df_usa_inf.index[-4]) + \
               str('<br>') + str('<br>') + \
               str('USA Unemployment. [U3, U6] : ') + \
               str(round(df_usa_unemp.iloc[-4, 0], 4)) + str(" ; ") + \
               str(round(df_usa_unemp.iloc[-4, 1], 4)) + \
               str('<br>') + \
               str('U3/U6 Timestamp: ') + str(df_usa_unemp.index[-4]) + \
               str('<br>') + str('<br>') + \
               str('GDP Trillions of Local Currency: ') + \
               str('<br>') + \
               str('[USA, CHN, JPN, GERM, UK] : ') + \
               str('<br>') + \
               str(round(df_gdp_trillions.iloc[-2, 0], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-2, 1], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-2, 2], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-2, 3], 3)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-2, 4], 3)) + str("") + \
               str('<br>') + \
               str('GDP Timestamp: ') + str(df_gdp_trillions.index[-2]) + \
               str('<br>') + str('<br>') + \
               str('') + \
               str('') + \
               str('----- PREVIOUS YEAR STATS: -----') + \
               str('') + \
               str('') + \
               str('<br>') + str('<br>') + \
               str('Equity Allocation: ') + str(round(df_eq_sup.iloc[-5], 4)) + \
               str('<br>') + \
               str('US Equities, $Billions: ') + str(round(us_equities_billions.iloc[-5], 4)) + \
               str('<br>') + \
               str('US Cash+Bonds, $Billions: ') + str(round(us_debt_billions.iloc[-5], 4)) + \
               str('<br>') + \
               str('Timestamp: ') + str(df_eq_sup.index[-5]) + \
               str('<br>') + str('<br>') + \
               str('CPI [All NSA, All SA, LFE NSA, LFE SA] : ') + \
               str('<br>') + \
               str('YoY: ') + str(round(df_usa_inf_yoy.iloc[-13, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-13, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-13, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_yoy.iloc[-13, 3], 4)) + \
               str('<br>') + \
               str('MoM: ') + str(round(df_usa_inf_mom.iloc[-13, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-13, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-13, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom.iloc[-13, 3], 4)) + \
               str('<br>') + \
               str('MoM Ann: ') + str(round(df_usa_inf_mom_ann.iloc[-13, 0], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-13, 1], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-13, 2], 4)) + str(" ; ") + \
               str(round(df_usa_inf_mom_ann.iloc[-13, 3], 4)) + \
               str('<br>') + \
               str('CPI Timestamp: ') + str(df_usa_inf.index[-13]) + \
               str('<br>') + str('<br>') + \
               str('USA Unemployment. [U3, U6] : ') + \
               str(round(df_usa_unemp.iloc[-13, 0], 4)) + str(" ; ") + \
               str(round(df_usa_unemp.iloc[-13, 1], 4)) + \
               str('<br>') + \
               str('U3/U6 Timestamp: ') + str(df_usa_unemp.index[-13]) + \
               str('<br>') + str('<br>') + \
               str('GDP Trillions of Local Currency: ') + \
               str('<br>') + \
               str('[USA, CHN, JPN, GERM, UK] : ') + \
               str('<br>') + \
               str(round(df_gdp_trillions.iloc[-5, 0], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-5, 1], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-5, 2], 1)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-5, 3], 3)) + str(" ; ") + \
               str(round(df_gdp_trillions.iloc[-5, 4], 3)) + str("") + \
               str('<br>') + \
               str('GDP Timestamp: ') + str(df_gdp_trillions.index[-5]) + \
               str('<br>') + str('<br>')

    # Send as email:
subj_string = str('Weekly Econ Update: [') + str(dtime_string) + str(']')
msg_text_01 = str('Weekly Market Update:') + \
              str('<br>') + str('<br>') + \
              stats_text_B
ehf.send_mail_gmail(username=gmail_username, password=gmail_pw, \
                    toaddrs_list=['kylebinder14@gmail.com', 'tothereadinglist102@gmail.com'], \
                    msg_text=msg_text_01, fromaddr='Hoey McHoeFace', \
                    subject=subj_string,
                    attachment_path_list=dir_to_send)
print('hi_4a')
