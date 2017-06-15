# DEC-API-IATI
A Python script to pull documents from the Developers Experience Clearinghouse (https://dec.usaid.gov/) in order to populate USAID's IATI document data.

The DEC API uses a base64 encoded search string in order to pull Evaluations and Summaries for USAID activities.
The results are all of the data for the input years combined into a CSV formatted file.

# Running the File
Open and run the csv-script-iati.py in your preferred Python console.
The script will request a starting year and ending year for the year range to download the data from.
The script will ask if the user wants to combine pre-existing files into one. If so, it will combine files and end the program.
If the user did not combine pre-existing files, then the user will be prompted if they want to combine downloaded files.
The script will then download the appropriate files from the DEC website using the (currently) hardcoded search query. Files are saved as "DEC_Data_From_(year).csv".
If the user chose to combine downloaded files, the files will now be combined into a file with the name "DEC_Data_From_(first_year)-(last_year).csv".
