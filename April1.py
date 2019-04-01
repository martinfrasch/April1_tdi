
# coding: utf-8

# In[60]:


#quandl-based capstone project
import quandl
import numpy as np
import datetime
import pandas as pd
from bokeh.io import output_file, show
from bokeh.plotting import figure
from bokeh.layouts import widgetbox,gridplot
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import Button, RadioButtonGroup, Select, RangeSlider,Tabs,Panel
from bokeh.models.tools import HoverTool
from bokeh.models import NumeralTickFormatter


output_file("king_tdi.html") 

quandl.ApiConfig.api_key = "YayxSPq-oifg3s46Bm5y"

median_listing_price_singlehome = quandl.get('ZILLOW/M15_MLPSF',returns=np)
median_listing_price_condo = quandl.get('ZILLOW/M15_MLPCC',returns=np)
median_rental_price_singlehome = quandl.get('ZILLOW/M15_MRPSF',returns=np)
median_rental_price_condo = quandl.get('ZILLOW/M15_MRPCC',returns=np)

df_listing_single = pd.DataFrame(median_listing_price_singlehome)
df_listing_condo = pd.DataFrame(median_listing_price_condo)
df_rental_single = pd.DataFrame(median_rental_price_singlehome)
df_rental_condo = pd.DataFrame(median_rental_price_condo)

source1=ColumnDataSource(df_listing_single)
source2=ColumnDataSource(df_listing_condo)
source3=ColumnDataSource(df_rental_single)
source4=ColumnDataSource(df_rental_condo)


# In[61]:


#print(df_listing_single)
#print(df_listing_condo)
#print(df_rental_single)
#print(df_rental_condo)

thirty_years_fixed_mortgage_rate=quandl.get('FMAC/FIX30YR',start_date='2010-01-01', end_date='2019-03-28', column_index='1', returns=np)
df_30y=pd.DataFrame(thirty_years_fixed_mortgage_rate)

#print(df_30y)

#compute rough monthly payments from a listed price single family home based on this date's mortgage
#match the date of mortgage, take that date's interest rate - 30 years and compute the payments - for future
#since now only looking at last year, will assume 4.5% average rate for 30 years and 

#L = input("How much will you be borrowing? ") Assume 20%
L_single = 0.2*df_listing_single

#N = input("How many years will you be paying this loan off? ") Assume 30 years
N_single = 30 *12

#I = input("What is the interest in percents that you will be paying? Ex, 10% = 10, 5% = 5, etc. ") Assume 5% (estimated visually from https://www.quandl.com/data/FMAC/FIX30YR-30-Year-Fix-Rate for the 2010 till now period) 
I_single = 5/100

#print("Your monthly payment will be: ") accounting for 10% tax spread over 12 months
M_single = (L/N) + I*(L/N)+(0.1*df_listing_single)/12

delta_single=M_single-df_rental_single

## condo

#L = input("How much will you be borrowing? ") Assume 20%
L_condo = 0.2*df_listing_condo

#N = input("How many years will you be paying this loan off? ") Assume 30 years
N_condo = 30 *12

#I = input("What is the interest in percents that you will be paying? Ex, 10% = 10, 5% = 5, etc. ") Assume 5% (estimated visually from https://www.quandl.com/data/FMAC/FIX30YR-30-Year-Fix-Rate for the 2010 till now period) 
I_condo = 5/100

#print("Your monthly payment will be: ") accounting for 10% tax spread over 12 months
M_condo = (L/N) + I*(L/N)+(0.1*df_listing_condo)/12


#print(delta_single)

delta_condo=M_condo-df_rental_condo

source5=ColumnDataSource(delta_single)
source6=ColumnDataSource(delta_condo)
source7=ColumnDataSource(df_30y)


# In[62]:


p_listing_single = figure(x_axis_type="datetime", title="King Country Median Listing Price - Single Family Residence", plot_height=350, plot_width=800)
p_listing_single.xgrid.grid_line_color=None
p_listing_single.ygrid.grid_line_alpha=0.5
p_listing_single.xaxis.axis_label = 'Time'
p_listing_single.yaxis.axis_label = 'Price'
p_listing_single.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")

hover=HoverTool()
hover.tooltips=[
    ('Median Listing Price of a Single Family Residence','@Value')
]
p_listing_single.add_tools(hover)


p_listing_condo = figure(x_axis_type="datetime", title="King Country Median Listing Price - Condo", plot_height=350, plot_width=800)
p_listing_condo.xgrid.grid_line_color=None
p_listing_condo.ygrid.grid_line_alpha=0.5
p_listing_condo.xaxis.axis_label = 'Time'
p_listing_condo.yaxis.axis_label = 'Price'
p_listing_condo.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")

hover=HoverTool()
hover.tooltips=[
    ('Median Listing Price of a Condo','@Value')
]
p_listing_condo.add_tools(hover)

p_rental_single = figure(x_axis_type="datetime", title="King Country Median Rental Price - Single Family Residence", plot_height=350, plot_width=800)
p_rental_single.xgrid.grid_line_color=None
p_rental_single.ygrid.grid_line_alpha=0.5
p_rental_single.xaxis.axis_label = 'Time'
p_rental_single.yaxis.axis_label = 'Price'
p_rental_single.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")

hover=HoverTool()
hover.tooltips=[
    ('Median Rental Price of a Single Family Residence','@Value')
]
p_rental_single.add_tools(hover)


p_rental_condo = figure(x_axis_type="datetime", title="King Country Median Rental Price - Condo", plot_height=350, plot_width=800)
p_rental_condo.xgrid.grid_line_color=None
p_rental_condo.ygrid.grid_line_alpha=0.5
p_rental_condo.xaxis.axis_label = 'Time'
p_rental_condo.yaxis.axis_label = 'Price'
p_rental_condo.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")

hover=HoverTool()
hover.tooltips=[
    ('Median Rental Price of a Condo','@Value')
]
p_rental_condo.add_tools(hover)


p_delta_single = figure(x_axis_type="datetime", title="Difference in Monthly Mortgage Payments between Median Listing and Rental Price of Single Family Residence in King Country", plot_height=350, plot_width=1200)
p_delta_single.xgrid.grid_line_color=None
p_delta_single.ygrid.grid_line_alpha=0.5
p_delta_single.xaxis.axis_label = 'Time'
p_delta_single.yaxis.axis_label = 'Price'
p_delta_single.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")

hover=HoverTool()
hover.tooltips=[
    ('Difference in Monthly Mortgage Payments between Median Listing and Rental Price of a Single Family Residence','@Value')
]
p_delta_single.add_tools(hover)

p_delta_condo = figure(x_axis_type="datetime", title="Difference in Monthly Mortgage Payments between Median Listing and Rental Price of a Condo in King Country", plot_height=350, plot_width=800)
p_delta_condo.xgrid.grid_line_color=None
p_delta_condo.ygrid.grid_line_alpha=0.5
p_delta_condo.xaxis.axis_label = 'Time'
p_delta_condo.yaxis.axis_label = 'Price'
p_delta_condo.yaxis[0].formatter = NumeralTickFormatter(format="$0,0")

hover=HoverTool()
hover.tooltips=[
    ('Difference in Monthly Mortgage Payments between Median Listing and Rental Price of a Condo in King Country','@Value')
]
p_delta_condo.add_tools(hover)

p_30y_mortg = figure(x_axis_type="datetime", title="30 years fixed mortgage rates from FMAC - national average", plot_height=350, plot_width=800)
p_30y_mortg.xgrid.grid_line_color=None
p_30y_mortg.ygrid.grid_line_alpha=0.5
p_30y_mortg.xaxis.axis_label = 'Time'
p_30y_mortg.yaxis.axis_label = '%'
p_30y_mortg.yaxis[0].formatter = NumeralTickFormatter(format='0')

hover=HoverTool()
hover.tooltips=[
    ('30 years fixed mortgage rates from FMAC','@US Interest Rate')
]
p_30y_mortg.add_tools(hover)


p_listing_single.line(x='Date', y='Value', source=source1, line_width=2)
p_listing_condo.line(x='Date', y='Value', source=source2, line_width=2)
p_rental_single.line(x='Date', y='Value', source=source3, line_width=2)
p_rental_condo.line(x='Date', y='Value', source=source4, line_width=2)
p_delta_single.line(x='Date', y='Value', source=source5, line_width=2)
p_delta_condo.line(x='Date', y='Value', source=source6, line_width=2)
p_30y_mortg.line(x='Week', y='US Interest Rate', source=source7, line_width=2)

tab1=Panel(child=p_listing_single,title="Listing Price Single Family")
tab2=Panel(child=p_listing_condo, title="Listing Price Condo")
tab3=Panel(child=p_rental_single, title="Rental Price Single Family")
tab4=Panel(child=p_rental_condo, title="Rental Price Condo")
tab5=Panel(child=p_delta_single, title="Delta Price Single Family")
tab6=Panel(child=p_delta_condo, title="Delta Price Condo")
tab7=Panel(child=p_30y_mortg, title="30y-fixed mortgage rates")


tabs = Tabs(tabs=[ tab1, tab2, tab3, tab4, tab5, tab6, tab7 ])

show(tabs)

