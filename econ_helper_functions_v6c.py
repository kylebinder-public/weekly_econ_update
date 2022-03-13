import smtplib  # for sending automatic email
from email.mime.text import MIMEText  # for sending automatic email
from email.mime.multipart import MIMEMultipart  # for sending automatic email
from email.mime.application import MIMEApplication  # for sending automatic email
import pandas as pd
import pandas_datareader as pdr
import datetime
import os
import matplotlib


# Global variables:
cwd = os.getcwd()
today_str = datetime.datetime.today().strftime('%Y-%m-%d')
today_dtime = datetime.datetime.today()
now = datetime.datetime.now()
dtime_string = now.strftime("%Y-%m-%d-%H-%M-%S")
dir_to_send = cwd + str('\\_TO_SEND_\\') + dtime_string + str('\\')
os.mkdir(dir_to_send)


def send_mail_gmail(username, password, toaddrs_list,
                    msg_text, fromaddr=None, subject="Test mail",
                    attachment_path_list=None):
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.login(username, password)
    msg = MIMEMultipart()
    sender = fromaddr
    recipients = toaddrs_list
    msg['Subject'] = subject
    if fromaddr is not None:
        msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    if attachment_path_list is not None:
        os.chdir(attachment_path_list)
        files = os.listdir()
        for f in files:  # add files to the message
            try:
                file_path = os.path.join(attachment_path_list, f)
                attachment = MIMEApplication(open(file_path, "rb").read(), _subtype="txt")
                attachment.add_header('Content-Disposition', 'attachment', filename=f)
                msg.attach(attachment)
            except:
                print("could not attach file")
    msg.attach(MIMEText(msg_text, 'html'))
    s.sendmail(sender, recipients, msg.as_string())


def get_usa_inflation_objects():
    df = []
    plot_figure = []
    most_recent_str = []

    # Load the FRED series we care about:
    start_date = datetime.datetime(1913, 1, 1)  # 1913
    end_date = today_dtime
    df_fred = pdr.DataReader(['CPIAUCNS', 'CPIAUCSL', 'CPILFENS', 'CPILFESL'], \
                             'fred', start_date, end_date)

    # Tickers:
    # CPIAUCNS: all items, NSA
    # CPIAUCSL: all items, SA
    # CPILFENS: all items less food+energy, NSA
    # CPILFESL: all items less food+energy, SA

    # Outputs:
    # (1a) df_yoy = year over year inflation
    # (1b) df_mom = month over month inflation, not annualized
    # (1c) df_mom_ann = month over month inflation, annualized by multiplying all "df_mom" by 12.0
    # (2) df_ratios = the "what was 1970 dollars" ratio dataframe

    df_yoy = (df_fred - df_fred.shift(12)) / df_fred
    df_mom = (df_fred - df_fred.shift(1)) / df_fred
    df_mom_ann = df_mom * 12

    # Create plots to be included as email attachments:
    # Semicolon suppresses output to console and greatly speeds this up; all I care about
    # is saving as a ".png" to be emailed:
    plotA = df_yoy.plot(y=['CPIAUCNS', 'CPILFENS'], color=['red', 'green']);
    plotA.set_ylabel("Inflation YoY");
    figA = plotA.get_figure();
    figA_str = dir_to_send + str('CPI_1919_') + str(dtime_string) + str('.png')
    figA.savefig(figA_str);
    matplotlib.pyplot.close(figA);

    plotB1 = df_yoy.iloc[-840:-1, :].plot(y=['CPIAUCNS', 'CPILFENS'], color=['red', 'green']);
    plotB1.set_ylabel("Inflation YoY - Previous 70 Years");
    figB1 = plotB1.get_figure();
    figB1_str = dir_to_send + str('CPI_70Y_') + str(dtime_string) + str('.png')
    figB1.savefig(figB1_str);
    matplotlib.pyplot.close(figB1);

    plotB2 = df_yoy.iloc[-120:-1, :].plot(y=['CPIAUCNS', 'CPILFENS'], color=['red', 'green']);
    plotB2.set_ylabel("Inflation YoY - Previous 10 Years");
    figB2 = plotB2.get_figure();
    figB2_str = dir_to_send + str('CPI_10Y_') + str(dtime_string) + str('.png')
    figB2.savefig(figB2_str);
    matplotlib.pyplot.close(figB2);

    return df_fred, plot_figure, most_recent_str, \
           df_yoy, df_mom, df_mom_ann, \
           dir_to_send


def get_uk_inflation_objects():
    df = []
    plot_figure = []
    most_recent_str = []

    # Load the FRED series we care about:
    start_date = datetime.datetime(1952, 1, 1)  # 1952
    end_date = today_dtime
    df_fred = pdr.DataReader(['GBRCPIALLMINMEI'], \
                             'fred', start_date, end_date)

    # Outputs:
    # (1) df_yoy = year over year inflation
    # (2) df_ratios = the "what was 1970 dollars" ratio dataframe

    return df, plot_figure, most_recent_str


def get_gdp_objects():
    df = []
    plot_figure = []
    most_recent_str = []

    # Load the FRED series we care about:
    start_date = datetime.datetime(1952, 1, 1)  # 1952
    end_date = today_dtime
    df_gdp_quarterly = pdr.DataReader(['GDP', 'CHNGDPNQDSMEI', \
                                        'JPNNGDP', 'CPMNACNSAB1GQDE', 'UKNGDP'],
                                       'fred', start_date, end_date)

    # Actual Outputs:
    # (1) USA GDP - BILLIONS OF USD (Q3 2021 RELEASED DEC 22, 2021)
    # (2) CHINA GDP - YUAN (Not Billions or Millions) - (Q3 2021 RELEASED DEC 14, 2021)
    # (3A) JAPAN GDP - BILLIONS OF YEN (Q3 2021 RELEASED DEC 7, 2021)
    # (3B) GERMANY GDP - *MILLIONS* OF EUROS (Q3 2021 RELEASED DEC 7, 2021)
    # (3C) UK GDP - *MILLIONS* OF POUNDS (Q3 2021 RELEASED DEC 22, 2021)
    df_trillions = df_gdp_quarterly.copy()
    df_trillions.iloc[:, 0] = df_trillions.iloc[:, 0] / 1000
    df_trillions.iloc[:, 1] = df_trillions.iloc[:, 1] / 1000000000000
    df_trillions.iloc[:, 2] = df_trillions.iloc[:, 2] / 1000
    df_trillions.iloc[:, 3] = df_trillions.iloc[:, 3] / 1000000
    df_trillions.iloc[:, 4] = df_trillions.iloc[:, 4] / 1000000

    # df_gdp_trillions = [df_gdp_quarterly.loc[:, 'GDP']  / 1000 , \
    #                     df_gdp_quarterly.loc[:, 'CHNGDPNQDSMEI'] / 1000000000000, \
    #                     df_gdp_quarterly.loc[:, 'JPNNGDP']  / 1000 , \
    #                     df_gdp_quarterly.loc[:, 'CPMNACNSAB1GQDE'] / 1000000,
    #                     df_gdp_quarterly.loc[:, 'UKNGDP'] / 1000000 ]

    # Desired Outputs:
    # (1) USA GDP
    # (2) CHINA GDP
    # (3) JAPAN, GERMANY, UK, INDIA(?)
    # (4A) WORLD GDP
    # (4B) DEVELOPED EX-US GDP
    # (4C) EMERGING EX-CHINA GDP

    # Equity Market Cap ???
    df_fred = pdr.DataReader(['NCBEILQ027S', 'FBCELLQ027S'], \
                             'fred', start_date, end_date)
    df_usa_mkt_cap_to_gdp = []

    # Standardize units:
    us_equities_billions = (df_fred.loc[:, 'NCBEILQ027S'] + df_fred.loc[:, 'FBCELLQ027S']) / 1000

    return df_gdp_quarterly, plot_figure, most_recent_str, \
           df_usa_mkt_cap_to_gdp, df_trillions


def get_usa_unemployment_objects():
    df = []
    plot_figure = []
    most_recent_str = []

    # Load the FRED series we care about:
    start_date = datetime.datetime(1952, 1, 1)  # 1952
    end_date = today_dtime
    df_fred = pdr.DataReader(['UNRATE', 'U6RATE'], \
                             'fred', start_date, end_date)

    plotB1 = df_fred.plot(y=['UNRATE', 'U6RATE'], color=['red', 'green']);
    plotB1.set_ylabel("USA Unemployment");
    figB1 = plotB1.get_figure();
    figB1_str = dir_to_send + str('USA_Unemployment') + str(dtime_string) + str('.png')
    figB1.savefig(figB1_str);
    matplotlib.pyplot.close(figB1);

    plotB2 = df_fred.iloc[-240:-1, :].plot(y=['UNRATE', 'U6RATE'], color=['red', 'green']);
    plotB2.set_ylabel("USA Unemployment - Previous 20 Years");
    figB2 = plotB2.get_figure();
    figB2_str = dir_to_send + str('USA_Unemployment_Prev20') + str(dtime_string) + str('.png')
    figB2.savefig(figB2_str);
    matplotlib.pyplot.close(figB2);

    return df_fred, plot_figure, most_recent_str


def get_equity_supply_objects():
    df = []
    plot_figure = []
    most_recent_str = []

    # Load the FRED series we care about:
    start_date = datetime.datetime(1952, 1, 1)  # 1952
    end_date = today_dtime
    df_fred = pdr.DataReader(['NCBEILQ027S', 'FBCELLQ027S', \
                              'TCMILBSNNCB', 'WCMITCMFODNS', \
                              'SLGTCMDODNS', 'TCMILBSHNO', 'FGTCMDODNS'], \
                             'fred', start_date, end_date)

    # Standardize units:
    us_equities_billions = (df_fred.loc[:, 'NCBEILQ027S'] + df_fred.loc[:, 'FBCELLQ027S']) / 1000
    us_debt_billions = df_fred.loc[:, 'TCMILBSNNCB'] + \
                       df_fred.loc[:, 'WCMITCMFODNS'] + \
                       df_fred.loc[:, 'SLGTCMDODNS'] + \
                       df_fred.loc[:, 'TCMILBSHNO'] + \
                       df_fred.loc[:, 'FGTCMDODNS']
    us_equity_allocation = us_equities_billions / (us_equities_billions + us_debt_billions)

    # Save DFs as CSV:
    now = datetime.datetime.now()
    dtime_string = now.strftime("%Y-%m-%d-%H-%M-%S")
    csv_dir = cwd + str('\\CSVs\\df_fred_') + dtime_string + str('.csv')
    df_fred.to_csv(csv_dir)

    # df = df_fred
    df = us_equity_allocation
    df_eq_sup = us_equity_allocation
    plot_figure = []
    most_recent_str = str(df_fred.index[-1])

    plotC1 = df_eq_sup.plot(y=['Equity Allocation'], color=['red']);
    plotC1.set_ylabel("Equity Alloc");
    figC1 = plotC1.get_figure();
    figC1_str = dir_to_send + str('Equity_Alloc_1955_') + str(dtime_string) + str('.png')
    figC1.savefig(figC1_str);
    matplotlib.pyplot.close(figC1);

    plotC2 = df_eq_sup.iloc[-40:-1].plot(y=['Equity Allocation'], color=['red']);
    plotC2.set_ylabel("Equity Alloc - Previous 10 Years");
    figC2 = plotC2.get_figure();
    figC2_str = dir_to_send + str('Equity_Alloc_10Y_') + str(dtime_string) + str('.png')
    figC2.savefig(figC2_str);
    matplotlib.pyplot.close(figC2);

    return df, plot_figure, most_recent_str, \
        us_equities_billions, us_debt_billions


def get_monetary_aggregates_objects():
    df = []
    plot_figure = []
    most_recent_str = []

    # Load the FRED series we care about:
    start_date = datetime.datetime(1952, 1, 1)  # 1952
    end_date = today_dtime
    df_fred = pdr.DataReader(['GBRCPIALLMINMEI'], \
                             'fred', start_date, end_date)

    # Outputs:
    # (1) df_yoy = year over year inflation
    # (2) df_ratios = the "what was 1970 dollars" ratio dataframe

    return df, plot_figure, most_recent_str


class EconObject:
    """A simple object for keeping track of FRED data"""

    #
    # above docstring can be called via "__doc__"
    #
    # Has these properties, possibly NULL:
    # (1) Most recent data point (String)
    # (2) Dataframe
    # (3) Plot/figure
    # (4) HTML
    #
    # Any methods?
    # (1) Populate most recent date
    # (2) retrieve data - will be specific for particular
    #     class - CPI we'll get from FRED; ETFs we'll get from
    #     Yahoo, VIX term structure we'll get from elsewhere.
    # (3) Create plot
    #
    #####################################
    def __init__(self, df, plot_figure, most_recent_str):
        # self.df = pd.Dataframe()
        self.df = df
        self.plot_figure = plot_figure
        self.most_recent_str = most_recent_str
