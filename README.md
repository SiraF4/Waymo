Waymo Cybersecurity Attack Simulations
ECE 1155 - Information Security 

This project contains two python simulations which demonstrate cyberattacks on the Waymo autonomous platform. Specifically, authentication attack and sensor spoofing attack.

Files included:
1. authenticationtestcode.py - credential stuffing simulation on Waymo One accounts
2. Sensors_vulnerabilitiy.py = LiDAR sensor spoofing simulation on Waymo percention system

##################################################################
Requirements for Running the programs:
Both scripts require Python 3 libraries
1. matplotlib (ploting our simualtion results)
2. numpy

Install them by running this line in your terminal:
pip install matplotlib numpy

!! Both programs must be ran from the terminal or command prompt !!

##################################################################
Simulation 1: Authentication Attack 
File: authenticationtestcode.py
1. open your terminal (command prompt or powershell on windows)
2. Navigate to the folder where you saved the python file:
    cd path\to\your\folder
3. Run the file:
    python authenticationtestcode.py

Expected Outputs:
* A printed summary table in the terminal showing the compromised and locked out accounts across three scenarios (FF, TF, TT)
* A window with 3 side-by-side plots:
    1. Accounts compromised over time
    2. System response time degradation
    3. Legitimate users locked out

##################################################################
Simulation 2: Sensor Spoofing Attack 
File: Sensors_vulnerability.py
1. open your terminal (command prompt or powershell on windows)
2. Navigate to the folder where you saved the python file:
    cd path\to\your\folder
3. Run the file:
    python Sensor_vulnerability.py

Expected Outputs:
* A printed summary in the terminal showing normal vs under-attack LiDAR outcomes
* A window showing Before vs After attack scatter plots of LiDAR detections
* A window showing a bar chart comparing error percentages (normal vs under attack)

##################################################################

Troubleshooting:
- If given these erros, please enter the terminal prompts to execute the libraries correctly:
1. Error: "No module named 'matplotlib'"
terminal:    pip install matplotlib

2. Error: "No module named 'numpy'"
terminal:    pip install numpy

3. Error: 'python' is not recognized
    Try using python3 in terminal instead:
terminal:   python3 authenticationtestcode.py

- If plot windows do not appear, make sure you are running the script from the terminal and not within the VS code's debugger or Run button

