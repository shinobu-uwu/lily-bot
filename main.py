import os

import discord
import humanize
from discord.ext.commands import Bot
import requests
from datetime import datetime

BASE_URL = 'https://yfapi.net'
TOKEN = os.getenv('DISCORD_TOKEN')
API_KEY = os.getenv('YFINANCE_API_TOKEN')

bot = Bot(command_prefix='$')


@bot.event
async def on_ready():
    print('Bot is ready!')


def add_trading_information(embed, data):
    embed.add_field(name='Beta (5Y Monthly) ', value=data["defaultKeyStatistics"]["beta"]["fmt"], inline=True)
    embed.add_field(name='52-Week Change', value=data["defaultKeyStatistics"]["52WeekChange"]["fmt"], inline=True)
    embed.add_field(name='S&P500 52-Week Change', value=data["defaultKeyStatistics"]["SandP52WeekChange"]["fmt"],
                    inline=True)
    embed.add_field(name='52-Week High', value=data["summaryDetail"]["fiftyTwoWeekHigh"]["fmt"], inline=True)
    embed.add_field(name='52-Week Low', value=data["summaryDetail"]["fiftyTwoWeekLow"]["fmt"], inline=True)
    embed.add_field(name='50-Day Moving Average', value=data["summaryDetail"]["fiftyDayAverage"]["fmt"], inline=True)
    embed.add_field(name='200-Day Moving Average', value=data["summaryDetail"]["twoHundredDayAverage"]["fmt"],
                    inline=True)
    embed.add_field(name='Average Vol (3 month)', value=data["summaryDetail"]["averageVolume"]["fmt"], inline=True)
    embed.add_field(name='Average Vol (10 month)', value=data["summaryDetail"]["averageDailyVolume10Day"]["fmt"],
                    inline=True)
    embed.add_field(name='Shares Outstanding', value=data["defaultKeyStatistics"]["sharesOutstanding"]["fmt"],
                    inline=True)

    raw_statistics = data["defaultKeyStatistics"]["impliedSharesOutstanding"]['fmt']
    implied_shares_outstanding = raw_statistics if raw_statistics is not None else 'N/A'
    embed.add_field(name='Implied Shares Outstanding', value=implied_shares_outstanding, inline=True)
    embed.add_field(name='Float', value=data["defaultKeyStatistics"]["floatShares"]['fmt'], inline=True)
    embed.add_field(name='% Held by Insiders', value=data["defaultKeyStatistics"]["heldPercentInsiders"]['fmt'],
                    inline=True)
    embed.add_field(name='% Held by Institutions', value=data["defaultKeyStatistics"]["heldPercentInstitutions"]['fmt'],
                    inline=True)

    date = humanize.naturaldate(datetime.fromtimestamp(data['defaultKeyStatistics']['dateShortInterest']['raw']))
    embed.add_field(name=f'Shares Short ({date})',
                    value=data["defaultKeyStatistics"]["sharesShort"]['fmt'], inline=True)
    embed.add_field(name=f'Short Ratio ({date})',
                    value=data["defaultKeyStatistics"]["shortRatio"]['fmt'], inline=True)
    embed.add_field(name=f'Short % of Float ({date})',
                    value=data["defaultKeyStatistics"]["shortPercentOfFloat"]['fmt'], inline=True)
    embed.add_field(name=f'Short % of Shares Outstanding ({date})',
                    value=data["defaultKeyStatistics"]["sharesPercentSharesOut"]['fmt'], inline=True)

    date = humanize.naturaldate(
        datetime.fromtimestamp(data['defaultKeyStatistics']['sharesShortPreviousMonthDate']['raw']))
    embed.add_field(name=f'Shares Short (prior to month {date})',
                    value=data["defaultKeyStatistics"]["sharesShortPriorMonth"]['fmt'], inline=True)


def add_dividends_and_splits(embed, data):
    embed.add_field(name='Forward Annual Dividend Rate', value=data["summaryDetail"]["dividendRate"]['fmt'],
                    inline=True)
    embed.add_field(name='Forward Annual Dividend Yield', value=data["summaryDetail"]["dividendYield"]['fmt'],
                    inline=True)
    embed.add_field(name='Tailing Annual Dividend Rate',
                    value=data["summaryDetail"]["trailingAnnualDividendRate"]['fmt'],
                    inline=True)
    embed.add_field(name='Tailing Annual Dividend Yield',
                    value=data["summaryDetail"]["trailingAnnualDividendYield"]['fmt'],
                    inline=True)
    embed.add_field(name='5 Year Average Dividend Yield',
                    value=data["summaryDetail"]["fiveYearAvgDividendYield"]['fmt'],
                    inline=True)
    embed.add_field(name='Payout Ratio', value=data["summaryDetail"]["payoutRatio"]['fmt'], inline=True)

    date = humanize.naturaldate(datetime.fromtimestamp(data["calendarEvents"]["dividendDate"]['raw']))
    embed.add_field(name='Dividend Date', value=date, inline=True)

    date = humanize.naturaldate(datetime.fromtimestamp(data["summaryDetail"]["exDividendDate"]['raw']))
    embed.add_field(name='Ex-Dividend Date', value=date, inline=True)
    embed.add_field(name='Last Split Factor', value=data["defaultKeyStatistics"]["lastSplitFactor"], inline=True)

    date = humanize.naturaldate(datetime.fromtimestamp(data["defaultKeyStatistics"]["lastSplitDate"]['raw']))
    embed.add_field(name='Last Split Date', value=date, inline=True)


def add_financial_highlights(embed, data):
    fiscal_end_year = datetime.fromtimestamp(data["defaultKeyStatistics"]["lastFiscalYearEnd"]['raw'])
    embed.add_field(name='Fiscal Year Ends',
                    value=humanize.naturaldate(fiscal_end_year),
                    inline=True)
    most_recent_quarter = datetime.fromtimestamp(data["defaultKeyStatistics"]["mostRecentQuarter"]['raw'])
    embed.add_field(name='Most Recent Quarter',
                    value=humanize.naturaldate(most_recent_quarter),
                    inline=True)

    embed.add_field(name='Profit Margin', value=data["defaultKeyStatistics"]["profitMargins"]["fmt"], inline=True)
    embed.add_field(name='Operating Margin (ttm)', value=data["financialData"]["operatingMargins"]["fmt"],
                    inline=True)

    embed.add_field(name='Return on Assets (ttm)', value=data['financialData']['returnOnAssets']['fmt'], inline=True)
    embed.add_field(name='Return on Equity (ttm)', value=data['financialData']['returnOnEquity']['fmt'], inline=True)

    embed.add_field(name='Total Revenue (ttm)', value=data['financialData']['totalRevenue']['fmt'], inline=True)
    embed.add_field(name='Revenue per Share (ttm)', value=data['financialData']['revenuePerShare']['fmt'], inline=True)
    embed.add_field(name='Quarterly Revenue Growth (yoy)', value=data['financialData']['revenueGrowth']['fmt'],
                    inline=True)
    embed.add_field(name='Gross Profit (yoy)', value=data['financialData']['grossProfits']['fmt'], inline=True)
    embed.add_field(name='EBITDA', value=data['financialData']['ebitda']['fmt'], inline=True)
    embed.add_field(name='Net Income Avi to Common (ttm)',
                    value=data['defaultKeyStatistics']['netIncomeToCommon']['fmt'], inline=True)
    embed.add_field(name='Diluted EPS (ttm)', value=data['defaultKeyStatistics']['trailingEps']['fmt'], inline=True)
    embed.add_field(name='Quarterly Earnings Growth (yoy)',
                    value=data['defaultKeyStatistics']['earningsQuarterlyGrowth']['fmt'],
                    inline=True)

    embed.add_field(name='Total Cash (mrq)', value=data['financialData']['totalCash']['fmt'], inline=True)
    embed.add_field(name='Total Cash Per Share (mrq)', value=data['financialData']['totalCashPerShare']['fmt'],
                    inline=True)
    embed.add_field(name='Total Debt (mrq)', value=data['financialData']['totalDebt']['fmt'], inline=True)
    embed.add_field(name='Total Debt/Equity (mrq)', value=data['financialData']['debtToEquity']['fmt'], inline=True)
    embed.add_field(name='Current Ratio (mrq)', value=data['financialData']['currentRatio']['fmt'], inline=True)
    embed.add_field(name='Book Value Per Share (mrq)', value=data['defaultKeyStatistics']['bookValue']['fmt'],
                    inline=True)

    embed.add_field(name='Operating Cash Flow (ttm)', value=data['financialData']['operatingCashflow']['fmt'],
                    inline=True)
    embed.add_field(name='Levered Free Cash Flow (ttm)', value=data['financialData']['freeCashflow']['fmt'],
                    inline=True)


@bot.command()
async def summary(ctx, ticker):
    ticker = ticker.upper()
    url = f'{BASE_URL}/v11/finance/quoteSummary/{ticker}?lang=en&region=US&modules=summaryDetail,quoteType,defaultKeyStatistics,financialData,calendarEvents'
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        await ctx.message.reply('The stock name couldn\'t be found')
        return

    data = response.json()['quoteSummary']['result'][0]
    title = f'{data["quoteType"]["longName"]} ({data["quoteType"]["symbol"]})'
    embed = discord.Embed(title=title)
    embed.url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'

    embed.add_field(name='Financial Highlights', value='\0', inline=False)

    add_financial_highlights(embed, data)
    await ctx.channel.send(embed=embed)

    embed = discord.Embed(title='Trading Information')
    add_trading_information(embed, data)
    await ctx.channel.send(embed=embed)

    embed = discord.Embed(title='Dividends & Splits')
    add_dividends_and_splits(embed, data)
    await ctx.channel.send(embed=embed)


bot.run(TOKEN)
