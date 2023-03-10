'''
  _____                                               
_/ ____\____ _______  _____             ____    ____  
\   __\\__  \\_  __ \/     \   ______  /    \  / ___\ 
 |  |   / __ \|  | \/  Y Y  \ /_____/ |   |  \/ /_/  >
 |__|  (____  /__|  |__|_|  /         |___|  /\___  / 
            \/            \/               \//_____/  

Quote Calculator v2023.02
Creator: Ryan Dinubilo
Created On: 3/4/23
Revised: 3/9/23+

Changelog:
v1.0
- Created calculator

v1.1 
- Added support for crops and spraying sessions
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

cropType = st.sidebar.selectbox("What type of crop?", ["Apples", "Blueberries", "Cane Berries", "Cannabis", "Cherries", "Citrus", "Hops", "Pollen Application", "Row Crops (Strawberries)", "Table Grapes", "Tree Nuts", "Wine Grapes"])

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


calculateButton = st.sidebar.button("Calculate")

if calculateButton:

    #calculations
    orchardMiles = acres*milesOfRowPerAcre

    #hours to travers full orchard
    ttcOrchard = orchardMiles/operationSpeed
    print(ttcOrchard)

    #drivers required to complete operation
    driversRequired = ttcOrchard/humanWorkingHours
    print(driversRequired)

    #Human cost to complete operation
    humanTotalCost = (ttcOrchard/acres)*(humanOperatorCostPerHour)
    print(humanTotalCost)

    #Driver cost per operation
    driverTotalCost = acres*humanTotalCost

    #input display
    col1, col2 = st.columns(2)
    col1.metric("Acres covered", acres)
    col2.metric("Crop Type", cropType)

    #Line break
    st.write("##")

    #First row of columns for miles to traverse full orchard
    col1, col2 = st.columns(2)
    col1.metric("Miles to traverse full orchard", millify(orchardMiles))
    col2.metric("Hours to traverse full orchard", millify(ttcOrchard))

    #Second row of columns for cost 
    col1, col2 = st.columns(2)
    humanCost = round(humanTotalCost, 2)
    col1.metric("Human Operating Cost Per Acre", f'$ {humanCost}')