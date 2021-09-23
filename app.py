import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from dash import dash_table
import plotly.express as px
import yfinance as yf
import dash_bootstrap_components as dbc


cols = ['Ticker', 'Number']
Energy = '석유, 천연가스, 석탄과 같은 화석연료의 탐사, 생산, 정제, 마케팅을 하는 대부분의 회사들과 지구에서 에너지원을 추출할 수 있는 서비스와 장비를 제공하는 기업을 Energy로 분류합니다. 유전 서비스 회사로서 대기업의 유전탐사나 Fracturing에 필요한 장비, 유체 및 재료를 판매하는 경우에도 Energy Sector로 분류됩니다.'
Energy_example = 'Exxon Mobil Corp.(XOM), Schlumberger(SLB), Kinder Morgan(KMI), Halliburton Co.(HAL)'
Energy_etf = 'Energy Select Sector SPDR ETF(XLE)'

Material = '원자재나 천연자원을 핵심사업으로 하는 회사. 원자재나 천연자원을 통해 더 유용한 것으로 바꾸는 회사를 Materials로 분류됩니다. 많은 화학 회사들, 광산 회사들, 금속 회사들, 벌목 회사들, 그리고 몇몇 석유와 천연가스 회사를 Materials로 분류합니다.'
Material_example = 'Rio Tinto(RIO), Vale S.A.(VALE), Ecolab(ECL)'
Material_etf = 'Materials Select Sector SPDR Fund(XLB)'

Industrial = 'Industrials 부문은 항공기, 전기 장비, 방위 산업, 건설 산업, 산업 기계 등과 같은 자본재 생산이나 운송 서비스 및 기반 시설의 제공에 직접 관여합니다. 미국의 가장 상징적인 우량 기업들 중 다수는 Industrials 부문이며, 많은 기업들이 미국 사회와 미국 군사력에 역사적인 역할을 하고 있습니다.'
Industrial_example = 'Boeing Co.(BA), Lockheed Martin Corp.(LMT), General Electric Co.(GE), Caterpillar(CAT).'
Industrial_etf = 'Industrial Select Sector SPDR ETF(XLI)'

Financial = 'Financials은 주로 돈을 취급하는 사업과 관련됩니다. 은행은 이 분야의 핵심 산업이지만, 보험 회사, 중개업소, 소비자 금융 제공업체, 주택 담보 관련 부동산 투자 신탁도 Financials에 포함됩니다.'
Financial_example = 'Bank of America Corp.(BAC), Visa(V), PayPal Holdings(PYPL), Berkshire Hathaway(BRK.A, BRK.B).'
Financial_etf = 'Financial Select Sector SPDR ETF(XLF)'

ConsumerCyclical = 'Consumer Cyclical은 상품과 서비스를 소비자들에게 판매합니다. 일반적으로 필수 소비재가 아닌 품목을 판매하는 기업이 포함되며, 자동차, 의류, 호텔, 레스토랑, 레저 관련 사업과 사치품, 소매업체와 전자 상거래 기반 소매업체 등이 포함됩니다.'
ConsumerCyclical_example = 'Carnival Corp.(CCL), Grubhub(GRUB), Lululemon Athletica(LULU), Party City(PRTY).'
ConsumerCyclical_etf = 'Consumer Discretionary Select Sector SPDR ETF(XLY)'

InformationTechnology = '인터넷과 기기 중심의 세계에 필요한 거의 모든 산업을 포함하고 있습니다. 소프트웨어 개발이나 기술 솔루션 구현과 관련된 서비스 제공에 초점을 맞추거나 기술을 가능하게 하는 장비, 구성요소 및 하드웨어를 구축하는 기업도 포함합니다. 소프트웨어, 하드웨어, 반도체 및 반도체 장비 업체도 포함됩니다.'
InformationTechnology_example = 'Apple(AAPL), Cisco Systems(CSCO), Intel Corp.(INTC), Oracle(ORCL)'
InformationTechnology_etf = 'Technology Select Sector SPDR ETF(XLK)'

CommunicationService = 'Communication services는 무선 통신망과 구식 유선 서비스 제공업체를 포함한 통신 서비스 제공업체들로 구성됩니다. TV나 라디오와 같은 구형 미디어와 인터넷을 통한 대화형 미디어와 새로운 형태의 통신을 포함한 미디어와 엔터테인먼트 회사들이 포함됩니다.'
CommunicationService_example = 'Verizon Communications(VZ), Facebook(FB), Walt Disney Co.(DIS), Comcast Corp.(CMCSA)'
CommunicationService_etf = 'Communication Services Select Sector SPDR ETF(XLC)'

RealEstate = '새로운 부동산 프로젝트를 개발하고 프로젝트 부동산 내의 다양한 공간에 대한 세입자를 얻음으로써 그것을 관리하는 기업을 포함한다. 또한 부동산투자신탁(LEIT)는 부동산 소유에 따른 현금 흐름에 쉽게 투자할 수 있는 편리한 방법을 개인 투자자들에게 제공하며, Mortgage LEIT를 제외한 모든 LEIT는 Real Estate에 포함된다.'
RealEstate_example = 'Redfin Corp.(RDFN), American Tower Corp.(AMT), Simon Property Group(SPG), Public Storage(PSA)'
RealEstate_etf = 'Vanguard Real Estate ETF(VNQ)'

HealthCare = 'Health Care는 두가지 주 요소로 구성되는데, 생명공학 기술을 기반으로 의약품 및 치료제를 개발하는 회사뿐만 아니라 이러한 치료제를 테스트하는 임상 실험에 필요한 분석 도구 및 공급품이 포함됩니다. 다른 하나는 수술용품, 의료 진단 도구 및 의료 보험을 포함한 의료 장비 및 서비스를 제공합니다.'
HealthCare_example = 'Johnson & Johnson(JNJ), Pfizer(PFE), McKesson Corp.(MCK), Abbott Laboratories(ABT)'
HealthCare_etf =  'Health Care Select Sector SPDR ETF(XLV)'

ConsumerStaple = '식품제조업자와 유통업자, 비내구적 생활용품, 개인 관리용품과 음료수 등 경제에 상관없이 사람들이 계속 필요로 하는 생활 필수품을 의미합니다. 가장 방어적인 부문중 하나이며, 불황에도 유지하거나 심지어 성장하지만, 경제성장 기간동안 시장에 뒤쳐지는 종목입니다. 이 범주에는 가정 및 개인 관리 제품, 음식, 음료, 담배 및 슈퍼마켓과 같은 판매를 전문으로 하는 소매 회사도 포함합니다.'
ConsumerStaple_example = 'Coca-Cola Co.(KO), Colgate-Palmolive(CL), Procter & Gamble Co.(PG), Walmart(WMT)'
ConsumerStaple_etf = 'Consumer Staples Select Sector SPDR ETF(XLP)'

Utility = '모든 유형의 Utility 회사를 포함합니다. 천연가스 송배전 전문기업 뿐만아니라 주택 및 상업용 고객이 전력을 사용할 수 있도록하는 전문 설비업체를 포함합니다. 또한 수도, 가스 등 공익적 사업에 종사하고 있으며 제한된 비즈니스 특성상 진입 장벽이 매우 높기 때문에 자연스럽게 독점되는 성향이 있습니다. 따라서 엄격한 규제를 받고 있으며 그들의 수익성은 정부에 의해 억제되고 있습니다.'
Utility_example = 'NextEra Energy(NEE), Duke Energy(DUK), Exelon Corp.(EXC), Dominion Energy(D)'
Utility_etf = 'Utilities Select Sector SPDR ETF(XLU)'



def data_to_frame(y):
    df = pd.DataFrame(y)
    tickers = df['ticker-data']
    numbers = df['number-data']
    return df, tickers, numbers

def get_data_from_yf(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        close = stock.info['previousClose']
        sector = stock.info['sector']
        industries = stock.info['industry']
        datum = [ticker, close, sector, industries]
        data.append(datum)

    return pd.DataFrame(data)

def cal_volume(final_data):
    cols = ['Ticker', 'Close', 'Sector', 'Industry', 'Number']
    final_data.columns = cols
    final_data['Volume'] = final_data['Close'] * final_data['Number']

    return final_data

def make_final_df(y):
    df, tickers, numbers = data_to_frame(y)
    data = get_data_from_yf(tickers)
    final_data = pd.concat([data, df['number-data'].astype('int64')], axis=1)
    final = cal_volume(final_data)
    final['Ticker'] = final[['Ticker']].applymap(str.upper)

    return final

### ETF ###
def get_data_from_yf_etf(tickers):
    data = []
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        close = stock.info['previousClose']
        cat = stock.info['category']
        datum = [ticker, close, cat]
        data.append(datum)
        
    return pd.DataFrame(data)


def cal_volume_etf(df):
    cols = ['Ticker','Close','Industry','Number','Sector']
    df.columns = cols
    df['Volume'] = df['Close'] * df['Number']

    return df


def make_final_df_etf(etf):
    df, tickers, numbers = data_to_frame(etf)
    data = get_data_from_yf_etf(tickers)
    final_data = pd.concat([data, df['number-data'].astype('int64')], axis=1)
    final_data['Sector'] = 'ETF'
    final = cal_volume_etf(final_data)
    final['Ticker'] = final[['Ticker']].applymap(str.upper)

    return final

def cal_percentage(a):
    df = pd.DataFrame(a)
    df['Percentage'] = round(df['Volume'] / df['Volume'].sum() * 100, 3)
    df.fillna('No Data', inplace=True)
    return df


def make_pie_chart(df):
    fig = px.sunburst(data_frame=df,
                     path = ['Sector','Industry','Ticker'],
                     values = 'Volume',
                     template = 'ggplot2',
                     height = 700)
    return fig

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# tab layout
tabs_styles = {
    'height' : '44px'
}
tab_style = {
    'borderBotton' : '1px solid #d6d6d6',
    'padding' : '6px',
    'fontWeight' : 'bold'
}
tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}


app.layout = dbc.Container([
    dbc.Row([
        html.H1('Stock Pie Chart by Sector and Industry'),
        html.H4('Stock 표를 본인이 보유하신 주식으로 채운뒤, Submit 버튼을 눌러주세요.'),
        html.H4('Ticker는 꼭 소문자로 작성해주세요'),
        html.H4(' Number에는 보유하신 개수를 넣어주세요'),
        html.H4('ETF는 지원하지 않습니다. ETF는 표에서 제거해주세요'),
        html.H4('주식 데이터를 불러오는데 많은 시간이 소요됩니다. 인내심을 갖고 기다려주세요!')
    ]),


    dbc.Row([
        dbc.Col(
        html.Div([
            html.H1('Stock'),
            dash_table.DataTable(
                id='adding-rows-table',
                columns=[
                    {'name' : 'Ticker', 'id' : 'ticker-data'},
                    {'name' : 'Number', 'id' : 'number-data'}
                ],
                data=[{}],
                editable=True,
                row_deletable=True
            ),

            html.Button('Add Row', id='editing-rows-button', n_clicks=0),
            html.Button('Submit', id='submit-button', n_clicks=0)

        ], className='Table'),),


        dbc.Col(
        html.Div([
            html.H1('Description'),
            dcc.Dropdown(
                id = 'drop-down',
                options = [
                    {'label' : 'Energy', 'value' : 'Energy'},
                    {'label' : 'Utility', 'value' : 'Utility'},
                    {'label' : 'Consumer Staples', 'value' : 'ConsumerStaple'},
                    {'label' : 'Health Care', 'value' : 'HealthCare'},
                    {'label' : 'Real Estate', 'value' : 'RealEstate'},
                    {'label' : 'Communication Services', 'value' : 'CommunicationService'},
                    {'label' : 'Information Technology', 'value' : 'InformationTechnology'},
                    {'label' : 'Consumer Cyclical', 'value' : 'ConsumerCyclical'},
                    {'label' : 'Financial', 'value' : 'Financial'},
                    {'label' : 'Industrial', 'value' : 'Industrial'},
                    {'label' : 'Material', 'value' : 'Material'}
                ],
                value='Energy'
            ),
            html.Div(id='drop-down-output'),
            html.H3('Major example of this sector'),
            html.Div(id='example'),
            html.H3('Major ETF of this Sector'),
            html.Div(id='etf_example')

        ], className='Description'),)]),


        html.Div([
            html.Div([], id='graphs-contents')]),


], className='container')



@app.callback(
    Output('adding-rows-table', 'data'),
    Input('editing-rows-button', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'))
def add_row(n_clicks, rows, columns):
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    return rows

@app.callback(
    [Output('graphs-contents', 'children')],
    [Input('submit-button', 'n_clicks'), Input('adding-rows-table', 'data')]
)
def check(n_clicks, y):
    if n_clicks == 0:
        raise PreventUpdate
    a = make_final_df(y)
    df = cal_percentage(a)
    fig = make_pie_chart(df)
    return [dcc.Graph(figure=fig)]


@app.callback(
    [Output('drop-down-output', 'children'), Output('example', 'children'), Output('etf_example', 'children')],
    Input('drop-down', 'value')
)
def update_output(value):
    if value == 'RealEstate':
        discription = RealEstate
        example = RealEstate_example
        etf_example = RealEstate_etf
    elif value == 'Energy':
        discription = Energy
        example = Energy_example
        etf_example = Energy_etf
    elif value == 'Material':
        discription = Material
        example = Material_example
        etf_example = Material_etf
    elif value == 'Industrial':
        discription = Industrial
        example = Industrial_example
        etf_example = Industrial_etf
    elif value == 'Utility':
        discription = Utility
        example = Utility_example
        etf_example = Utility_etf
    elif value == 'HealthCare':
        discription = HealthCare
        example = HealthCare_example
        etf_example = HealthCare_etf
    elif value == 'Financial':
        discription = Financial
        example = Financial_example
        etf_example = Financial_etf
    elif value == 'ConsumerCyclical':
        discription = ConsumerCyclical
        example = ConsumerCyclical_example
        etf_example = ConsumerCyclical_etf
    elif value == 'ConsumerStaple':
        discription = ConsumerStaple
        example = ConsumerStaple_example
        etf_example = ConsumerStaple_etf
    elif value == 'InformationTechnology':
        discription = InformationTechnology
        example = InformationTechnology_example
        etf_example = InformationTechnology_etf
    elif value == 'CommunicationService':
        discription = CommunicationService
        example = CommunicationService_example
        etf_example = CommunicationService_etf
    return discription, example, etf_example


if __name__ == '__main__':
    app.debug = True
    app.run_server()
