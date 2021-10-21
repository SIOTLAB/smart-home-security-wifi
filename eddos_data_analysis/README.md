## data_analysis folder contains files related to E-DDoS data pre-processing and graph plotting.

It has the following three files:
data_analysis.ipynb is a Jupyter notebook and contains the code to analyze the E-DDoS attack data launched against various WiFi-based IoT devices. Overall the analysis is done in the following steps:
1. calculated the mean 10ms power and 10ms attack rate 
2. shift 10 ms rate rows between a range of 0 to 500 (i.e., 0 second to 5 seconds)
3. After dropping, calculate the mean power of 500 ms and rate for 500 ms
3. Calculate correlation for each shift and find maximum correlation and respective shift
4. Shift the data frame by max amount.
5. Repeat for all files
6. Plot graphs 

convert_csv.py: contain the code to convert pcap file to CSV using tshark \
variables.py contains the variable used in the Jupyter notebook 
