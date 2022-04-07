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


def add_valuation_measures(embed, data):
    embed.add_field(name=f"Market Cap (intraday)", value=f"{data['summaryDetail']['marketCap']['fmt']}", inline=True)
    embed.add_field(name=f"Enterprise Value", value=f"{data['defaultKeyStatistics']['enterpriseValue']['fmt']}",
                    inline=True)
    embed.add_field(name=f"Trailing P/E", value=f"{data['summaryDetail']['trailingPE']['fmt']}", inline=True)
    embed.add_field(name=f"Forward P/E", value=f"{data['summaryDetail']['forwardPE']['fmt']}", inline=True)
    embed.add_field(name=f"PEG Ratio", value=f"{data['defaultKeyStatistics']['pegRatio']['fmt']}", inline=True)
    embed.add_field(name=f"Price/Sales (ttm)", value=f"{data['summaryDetail']['priceToSalesTrailing12Months']['fmt']}",
                    inline=True)
    embed.add_field(name=f"Price/Book (mrq)", value=f"{data['defaultKeyStatistics']['priceToBook']['fmt']}",
                    inline=True)
    embed.add_field(name=f"Enterprise Value/Revenue",
                    value=f"{data['defaultKeyStatistics']['enterpriseToRevenue']['fmt']}", inline=True)
    embed.add_field(name=f"Enterprise Value/EBITDA",
                    value=f"{data['defaultKeyStatistics']['enterpriseToEbitda']['fmt']}", inline=True)


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
    embed.add_field(name='EBITDA', value=data['financialData']['ebitda']['fmt'], inline=True)


@bot.command()
async def summary(ctx, ticker):
    ticker = ticker.upper()
    url = f'{BASE_URL}/v11/finance/quoteSummary/{ticker}?lang=en&region=US&modules=summaryDetail,quoteType,defaultKeyStatistics,financialData'
    headers = {'X-API-KEY': API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        ctx.message.reply('The stock name couldn\'t be found')

    data = response.json()['quoteSummary']['result'][0]
    title = f'{data["quoteType"]["longName"]} ({data["quoteType"]["symbol"]})'
    embed = discord.Embed(title=title)
    embed.url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics?p={ticker}'

    embed.add_field(name='Financial Highlights', value='\0', inline=False)

    add_financial_highlights(embed, data)
    await ctx.channel.send(embed=embed)


bot.run(TOKEN)
