# simulation-small-cell-base-station-mobility
Python Application for Real Time Simulation of a Cellular Base Station &amp; a Small Cell for Mobility Management

# Mobility Management Simulation between Base Station and Small Cell

## Overview
This Python application simulates the mobility management of users between a base station and a small cell, focusing on scenarios such as handoffs, call drops, and RSL (Received Signal Level) variations. The simulation is particularly beneficial for understanding the network performance in terms of successful handoffs, call drops, and other relevant metrics.

## Key Features
- Simulates mobility between a base station and a small cell.
- Simulates mobile user movements and dynamically updates their location.
- Takes user input for distance, simulation duration, power of base stations, and number of channels.
- Computes RSL values dynamically for both the base station and the small cell.
- Generates graphs and reports on call drops and handoffs.
- Provides detailed statistics about the network performance.

## Code Structure
- Simulation.py: Main script responsible for running the simulation.
- RSL.py: Computation module for Received Signal Level (RSL).
- Q3.py: Additional module that analyzes transition areas for call drops and handoffs.

## Files in this Project
- simulation.py
This script performs the overall simulation, including invoking functions for Radio Signal Level (RSL) calculations, propagation loss, fading, and shadowing.

- RSL.py
This script contains multiple functions for calculating various components of RSL, such as propagation loss based on the Okamura-Hata model, shadowing, and fading.

- Q3.py
This script contains a different approach for RSL calculations and outputs a plot comparing the RSL values from a Base Station and a Small Cell over different distances.

## Inputs
- Total Simulation Time (in hours)
- Distance between Base Station and Small Cell (in meters)
- Base Station EIRP (in dBm)
- Small Cell EIRP (in dBm)
- Channels at Base Station
- Channels at Small Cell

## Outputs
- Call drop report, which includes the drop location, serving cell, and RSL value.
- Handoff report.
- Detailed network statistics like total active calls, successful completed calls, etc.

## Output File Explanation

The simulation generates an output file that provides detailed statistics for each simulated hour. Here's how the data is structured in the output:

1. **Base Station Metrics**
    - Active Calls
    - Total Call Attempts
    - Successful Call Connections
    - Dropped Calls
    - Blocked Calls due to Capacity
    - Blocked Calls due to Power
    - Handoff Attempts
    - Successful Handoffs
    - Failed Handoffs

2. **Small Cell Metrics**
    - Active Calls
    - Total Call Attempts
    - Successful Call Connections
    - ... (and so on)

3. **Network Summary**
    - Total Call Attempts
    - Total Successful Call Connections
    - ... (and so on)

## RSL.py Explanation

This script computes the Received Signal Level (RSL) for a wireless network simulation, considering various types of signal losses like propagation, fading, shadowing, and penetration.

Here is a breakdown of the functions:

- `create_shadowloss(x)`: Initializes shadow loss.
- `propagation_loss(freq, loc, antenna_height, height_user)`: Computes propagation loss using Okumura-Hata model.
- `fading()`: Calculates Rayleigh fading.
- `shadowing(loc)`: Returns the shadow loss based on location.
- `penetration(loc, node, x)`: Determines the penetration loss.
- `RSL(freq, x, loc, height_bs, height_sc, height_user, EIRP_bs, EIRP_sc)`: Calculates the Received Signal Level for both base station and small cell.


## Q3.py Explanation

The `Q3.py` script is designed to simulate, calculate, and visualize the Received Signal Level (RSL) of both base stations and small cells over varying distances. 

### Functions

- `propagation_loss(...)`: Calculates propagation loss using the Okumura-Hata model.
- `fading()`: Calculates Rayleigh fading.
- `shadowing(distance)`: Computes shadowing loss based on distance.
- `penetration(distance, id)`: Calculates penetration loss.
- `RSL(...)`: Computes the RSL for base station and small cell, saves it to a text file, and plots the results using `matplotlib`.

### Usage

- To use, simply run any script. 
- Ensure that all the required dependencies are installed.
- Run the desired script by executing python <script_name>.py from your command line.


## Software Dependencies

Before running the scripts, make sure you have installed the following Python packages:

- `numpy`: Required for numerical operations.
- `math`: Required for mathematical computations.
- `time`: Required for timing events.
- `random`: Required for generating random numbers.
- `matplotlib`: Required for plotting graphs.






