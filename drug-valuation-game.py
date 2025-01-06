## packages 
from dash import Dash, html, dcc 
from dash.dependencies import Input, Output, State
import dash 
import plotly.express as px 
import numpy as np 

px.defaults.template = "ggplot2" 

## Dropdown style 
## Set the button style
dropdown_style = {
    'background-color': "#d0d2d3",
    'color': '#354a5d',
    'height': '30px',
    'width': '125px',
    'font-size': '20px',
    'font-color': '#fafbfb'
}

## options 
year_options = [x for x in range(17)]
negotiated_drug_prices = [1,10,100,1000,2500,5000,10000,20000,40000,60000]
discount_rate_options = [10]

## IRA predefines 
free_market_price = html.Div(className="quarterC",
                  children=[
                      html.P("Free Market Drug Price ($)"),
                      dcc.Dropdown(
                          options= [50000, 60000, 77568, 80000],
                          value=77568,
                          id="market-drug-price",
                          style = dropdown_style
                    )
                  ])
YoR_market_price = html.Div(className="quarterC",
                  children=[
                      html.P("Years at Market Price"),
                      dcc.Dropdown(
                          options= year_options,
                          value=9,
                          id="yor-market-price",
                          style = dropdown_style
                    )
                  ])

cmc_nego_price = html.Div(className="quarterC",
                  children=[
                      html.P("Negotiated Drug Price ($)"),
                      dcc.Dropdown(
                          options= negotiated_drug_prices,
                          value=100,
                          id="nego-drug-price",
                          style = dropdown_style
                    )
                  ])
YoR_nego_price = html.Div(className="quarterC",
                  children=[
                      html.P("Years at Negotiated Price"),
                      dcc.Dropdown(
                          options= year_options,
                          value=9,
                          id="yor-nego-price",
                          style = dropdown_style
                    )
                  ])

discount_rate = html.Div(className="sixC",
                  children=[
                      html.P("Discount Rate (%)"),
                      dcc.Dropdown(
                          options= [8, 10, 12],
                          value=10,
                          id="discount-rate",
                          style = dropdown_style
                    )
                  ])

phase1_PoS = html.Div(className="sixC",
                  children=[
                      html.P("Ph.1 PoS (%)"),
                      dcc.Dropdown(
                          options= [10*x for x in range(11)],
                          value=20,
                          id="ph1-pos",
                          style = dropdown_style
                    )
                  ])

phase2_PoS = html.Div(className="sixC",
                  children=[
                      html.P("Ph.2 PoS (%)"),
                      dcc.Dropdown(
                          options= [10*x for x in range(11)],
                          value=40,
                          id="ph2-pos",
                          style = dropdown_style
                    )
                  ])

phase3_PoS = html.Div(className="sixC",
                  children=[
                      html.P("Ph.3 PoS (%)"),
                      dcc.Dropdown(
                          options= [10*x for x in range(11)],
                          value=60,
                          id="ph3-pos",
                          style = dropdown_style
                    )
                  ])

fda_PoS = html.Div(className="sixC",
                  children=[
                      html.P("FDA Approval PoS (%)"),
                      dcc.Dropdown(
                          options= [10*x for x in range(11)],
                          value=80,
                          id="fda-pos",
                          style = dropdown_style
                    )
                  ])

r_and_d = html.Div(className="sixC",
                  children=[
                      html.P("R&D Costs ($ Millions)"),
                      dcc.Dropdown(
                          options= [0, 750, 1000, 1500, 2000],
                          value=1000,
                          id="rd-costs",
                          style = dropdown_style
                    )
                  ])





############################# START THE APP ####################################
app = Dash(__name__)
server = app.server



app.layout = html.Div([
    ######## HEADER
    html.Div(children=[
        html.H1("No Patient Left Behind - Drug Valuation Game", className="header"),
        html.Hr(),
        html.H3("Senior Fellow: Zelda Mendelowitz"),
        html.H3("Jr Fellow: Thanaa Makdsi, "),
        html.H2("Drug: KT-474 (small molecule)"),
        html.H3("Indictation: Hidradenitis Suppurativa (HS)")
    ]),
    html.Hr(),
    ###### USER INPUTS 
    html.Div(className="row",
             children=[
                 ## left box
                 html.Div(className="lcolumn",
                          children=[
                              html.Div(className="card",
                                       children=[
                                           html.H2("IRA Adjusted Parameters"),
                                           html.Div(className="row",
                                                    children=[
                                                        free_market_price,
                                                        YoR_market_price,
                                                        cmc_nego_price,
                                                        YoR_nego_price
                                                    ])
                                       ])
                          ]),
                 html.Div(className="rcolumn",
                          children=[
                              html.Div(className="card",
                                       children=[
                                           html.H2("IRA Independent Parameters"),
                                           html.Div(className="row",
                                                    children=[
                                                        discount_rate,
                                                        phase1_PoS,
                                                        phase2_PoS,
                                                        phase3_PoS,
                                                        fda_PoS,
                                                        r_and_d
                                                    ])
                                       ])
                          ])        
             ]),
    #### NPVs
    html.Div(className="row",
             children=[
                 html.Div(className="l2column",
                          children=[
                              html.Div(className="card",
                                       children=[
                                           html.H1("Free Market NPV"),
                                           html.H1(id="free-market-npv")
                                       ])
                          ]),
                 html.Div(className="r2column",
                          children=[
                              html.Div(className="card",
                                       children=[
                                            html.H1("IRA Adjusted NPV"),
                                            html.H1(id="ira-adjusted-npv")
                                       ])
                          ])
             ])
])




#### NET PRESENT VALUE FUNCTION 
## calculate the net present value of a revenue stream with discount rate
def npv(revenue, rate):
    n = len(revenue)
    discount_factor = 1/(1+rate)
    print(discount_factor)
    sum = 0
    for i in range(n):
        sum += revenue[i]*(discount_factor**(i+1))
    return sum

## Format currencies with dollar sign and commas
def format_currency(amount):
    return '${:,.0f}'.format(amount)



################################################################################


###### CALL BACK
### FREE MARKET NPV
@app.callback(
    Output("free-market-npv", "children"),
    Output("ira-adjusted-npv", "children"),
    Input("market-drug-price", "value"),
    Input("yor-market-price", "value"),
    Input("nego-drug-price", "value"),
    Input("yor-nego-price", "value"),
    Input("discount-rate", "value"),
    Input("ph1-pos", "value"),
    Input("ph2-pos", "value"),
    Input("ph3-pos", "value"),
    Input("fda-pos", "value"),
    Input("rd-costs", "value")
)
def calculate_npv(market,
                  yor_market,
                  nego,
                  yor_nego,
                  discount_rate, 
                  ph1,
                  ph2,
                  ph3,
                  fda,
                  rd):
    
    ### Fixed inputs
    years_to_start = 4
    growth = 0.007
    drug_price_growth = 0.01
    prevalence_rate = 0.01
    mod_to_severe_rate = 0.45
    discontinuation_rate = 0.25
    start_pop = 348382799
    pos = (ph1/100)*(ph2/100)*(ph3/100)*(fda/100)
    costs = 1000000*rd

    ## population computation
    populations = [start_pop*(1+growth)**n for n in range(yor_market + yor_nego)]
    hs_pop = np.multiply(populations, prevalence_rate)
    hs_mod_severe = np.multiply(hs_pop, mod_to_severe_rate)
    market_share = [min(0.01 + 0.04*n, 1) for n in range(yor_market + yor_nego)]
    treated_pop = np.multiply(hs_mod_severe, market_share)
    final_pop = np.multiply(treated_pop, (1-discontinuation_rate))

    ## free market and adjusted price lists
    fmp = [market*(1 + drug_price_growth)**n for n in range(yor_market)]
    neg_prices = [nego*(1+drug_price_growth)**n for n in range(yor_nego)]
    prices = fmp + neg_prices
    free_market_prices = [market*(1 + drug_price_growth)**n for n in range(yor_market + yor_nego)]

    ## free market vs adjusted revenues
    unadjusted_revenue_IRA = np.multiply(final_pop, prices)
    adjusted_revenue_IRA = [0]*years_to_start + list(np.multiply(unadjusted_revenue_IRA, pos))
    unadjusted_revenue_FM = np.multiply(final_pop, free_market_prices)
    adjusted_revenue_FM = [0]*years_to_start + list(np.multiply(unadjusted_revenue_FM, pos))

    ## collect net present values and format correctly
    npvs = [round(npv(adjusted_revenue_FM, discount_rate/100)) - costs,
            round(npv(adjusted_revenue_IRA, discount_rate/100)) - costs]
    return [format_currency(x) for x in npvs]



################################################################################


if __name__ == '__main__':
    app.run(debug=True, port=8000)
