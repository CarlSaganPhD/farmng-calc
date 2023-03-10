'''
  _____                                               
_/ ____\____ _______  _____             ____    ____  
\   __\\__  \\_  __ \/     \   ______  /    \  / ___\ 
 |  |   / __ \|  | \/  Y Y  \ /_____/ |   |  \/ /_/  >
 |__|  (____  /__|  |__|_|  /         |___|  /\___  / 
            \/            \/               \//_____/  

Quote Calculator v2023.02
Creator: Ryan Dinubilo
Created: 3/4/23
Revised: 3/9/23

Changelog:
v1.0
- Created calculator

v1.1 
- Added support for crops and spraying sessions

v1.2
- Added savings algorthm, graph support, more metric displays
'''


#Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import time
from millify import millify

#Load sidebar logo and disclaimer
logo = st.sidebar.image("https://i.imgur.com/MYHvLk7.png")
title = st.sidebar.header("farm-ng Quote Calculator")
body = st.sidebar.write("This calculator will provide you with a comprehensive analysis of the benefits of using our robotics products.")
links = st.sidebar.write("To learn more, visit our [website](https://farm-ng.com)")

#Calculation Variables and User Input
acres = st.sidebar.slider("Acres covered", 1, 2000)
acresInt = int(acres)

cropType = st.sidebar.selectbox("What type of crop?", ["🍎 Apples", "Blueberries", "Cane Berries", "Cannabis", "Cherries", "Citrus", "Hops", "Pollen Application", "Row Crops (Strawberries)", "Table Grapes", "Tree Nuts", "Wine Grapes"])

advancedSettings = st.sidebar.checkbox("Advanced Settings")


#Miles of standard size 12ft width rows per acre
milesOfRowPerAcre = 0.79

#Current estimate for number of acres covered by a single Amiga?
acresPerAmiga = 20

#Operation speed in miles per hour
operationSpeed = 2

#Human operator cost per hour
humanOperatorCostPerHour = 24.5

#85 HP Tractor Overhead per hour
tractorOverheadPerHour = 34.9

#85 HP Tractor Overhead per year
tractorOverheadPerYear = 10470

#human working hours
humanWorkingHours = 8

#Autonomy working hours
autonomyWorkingHours = 20

#tractors requi
tractorsRequiredPerEvent = 1


if advancedSettings:
  milesofRowPerAcreUser = st.sidebar.number_input("Miles of Row per Acre (default=0.79 mi/acre)", value=0.79)
  operationSpeedUser = st.sidebar.number_input("Operation Speed (default=2 mph)", value=2)

  humanCostPerHourUser = st.sidebar.number_input("Human Operating Cost Per Hour (default=$24.50)", value=24.5)


calculateButton = st.sidebar.button("Calculate")

if calculateButton:

    #Savings algorithm
    N = acres
    
    df = pd.DataFrame({ 'Acres covered (acres)' : range(1, N + 1, 1), 
                        'Original Cost ($)' : np.linspace(13.79, N*13.79 +1, N),
                        'Amiga Cost ($)' : np.linspace(2.63, N*2.63+1, N)})

    #calculations
    orchardMiles = acres*milesOfRowPerAcre

    #hours to travers full orchard
    ttcOrchard = orchardMiles/operationSpeed

    #drivers required to complete operation
    driversRequired = ttcOrchard/humanWorkingHours

    #Human cost to complete operation
    humanTotalCost = (ttcOrchard/acres)*(humanOperatorCostPerHour)

    #Driver cost per operation
    driverTotalCost = acres*humanTotalCost

    #Number of drivers needed to complete operation
    driversNeeded = acres/8

    #Calculations
    amigaCostPerAcre = (ttcOrchard/acres)*6.67
    amigaCostPerHourRounded = round(amigaCostPerAcre, 2)
    amigaTotal = amigaCostPerAcre*acres
    amigaTotalRounded = round(amigaTotal)

    tractorCostPerHour = (ttcOrchard/acres)*tractorOverheadPerHour
    tractorCostPerHourRounded = round(tractorCostPerHour, 2)

    tractorTotal = tractorOverheadPerHour*acres
    tractorTotalRoudned =round(tractorTotal)

    #Difference savings
    savings = tractorTotal - amigaTotal
    savingsRounded = round(savings)

    st.header(f"You save: :green[${savingsRounded}] by switching to the Amiga platform")

    #input display
    col1, col2 = st.columns(2)
    col1.metric("Acres covered", acres)
    col2.metric("Crop Type", cropType)

    #First row of columns for miles to traverse full orchard
    col1, col2 = st.columns(2)
    col1.metric("Miles to traverse full orchard", millify(orchardMiles), help=f"Covering {acres} acres at 0.79 miles of standard 12ft row per acre")
    col2.metric("Hours to traverse full orchard", millify(ttcOrchard), help=f'At an operation speed of 2 mph')

    st.write('##')

    #Amiga Calculation
    #Third row of columns for cost 
    col1, col2 = st.columns(2)
    col1.metric("🦾 Amiga Cost Per Acre", f'$ {amigaCostPerHourRounded}', help=f'Total amiga cost, divided by a 10 year lifetime with 300 work-hours per year')
    col2.metric("🦾 Total Amiga Operating Cost", f'$ {amigaTotalRounded}', help=f'Covering {acres} acres at $2.63 per acre')
    
    # #Second row of columns for cost 
    # col1, col2 = st.columns(2)
    # humanCost = round(humanTotalCost, 2)
    # col1.metric(label="👤 Driver Operating Cost Per Acre", value=f'$ {humanCost}', help=f'Hours to traverse orchard divided by orchard size, times the driver pay per hour')

    # driverTotal = humanCost*acres
    # driverTotalRoudned =round(driverTotal,2)
    # col2.metric("Total Driver Operating Cost", f'$ {driverTotalRoudned}')

    st.write('##')
    #Third row of columns for cost 
    col1, col2 = st.columns(2)
    col1.metric("🚜 Tractor Operating Cost Per Acre", f'$ {tractorCostPerHourRounded}', help=f'Hours to traverse orchard divided by orchard size, times the tractor cost per hour')
    col2.metric("Total Tractor Operating Cost", f'$ {tractorTotalRoudned}', help=f'Covering {acres} acres at $13.79 per acre')

    #Area graph of cost
    st.area_chart(data=df, x="Acres covered (acres)")
