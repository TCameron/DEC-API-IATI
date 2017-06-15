import urllib.request
import urllib.parse
import shutil
import base64
import glob
import os
import time
import datetime
from datetime import date


__author__ = "Timothy Cameron"
__email__ = "tcameron@devtechsys.com"
__date__ = "06-15-2017"
__version__ = "0.1"
now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+'Z'


# Method to combine the data downloaded from the DEC website into a single file
def concat(firstyear, lastyear):
    print("Combining files...")
    for j in range(firstyear, (lastyear+1)):
        filename = "export/" + time.strftime("%m-%d-%Y") + "/DEC_Data_From_" + str(j) + ".csv"
        with open(filename) as fin:
            conloop(fin, 1, firstyear, lastyear)
    print("finished")
    exit(0)


# Concats files, row by row, into one CSV file
def conloop(infile, line, f, l):
    outputfilename = "export/" + time.strftime("%m-%d-%Y") + "/DEC_Data_From_" + str(f) + "-" + str(l) + ".csv"
    files = glob.glob('*.csv')
    with open(outputfilename, 'w') as fout:
        for file_ in files:
            for entry in open(file_, 'r'):
                print(entry)
                try:
                    fout.write(entry)
                    line += 1
                except UnicodeDecodeError:
                    conloop(infile, line+1)


# TODO: Find a use for this function? I believe it was to remove header lines from concat'd files
# Replaces a specific line within a file with a given string
def replace_line(filename, line_num, text):
    lines = open(filename, 'r').readlines()
    lines[line_num] = text
    out = open(filename, 'w')
    out.writelines(lines)
    out.close()


# Error checking and correction for the input years
def check_years(first_year, last_year):
    if last_year < first_year:
        temp = first_year
        first_year = last_year
        last_year = temp
    if last_year < 1953:
        last_year = 1953
    elif last_year > date.today().year:
        last_year = date.today().year
        print('Cannot search for dates in the future. Setting last year to: ' + str(last_year))
    return first_year, last_year


# Grab the user's parameters
first = int(input("Input the first year of the range: "))
last = int(input("Input the last year of the range: "))

# Fix the years, in case of an error
first_corrected, last_corrected = check_years(first, last)

# If the user answers y or yes, then concat data and end program; Otherwise, download files
skip = input("Would you like combine pre-existing files? [Y/N] ")
if skip.lower() == 'y' or skip.lower() == 'yes':
    concat(first_corrected, last_corrected)
# Download data; if the user enters y or yes, concat the data after download
answer = ''
if first_corrected != last_corrected:
    answer = input("Would you like to combine the downloaded files? [Y/N] ")

# Make download directory
if not os.path.exists("export/" + time.strftime("%m-%d-%Y") + "/"):
    os.makedirs("export/" + time.strftime("%m-%d-%Y") + "/")

# Main loop to download the data
for i in range(first_corrected, (last_corrected+1)):
    print("Downloading data for the year " + str(i) + "...")
    search = 'documents.date_of_publication_freeforrm:(' + str(i) \
             + ') AND documents.bibliographic_type_code=(21 OR 22 OR 24)'
    byte_string = search.encode('utf-8')
    conv = base64.b64encode(byte_string)
    converted = str(conv).replace('b\'', '')
    converted = converted.replace('\'', '')
    converted = urllib.parse.quote_plus(converted)
    urltoopen = "https://dec.usaid.gov/api/qsearch.ashx?q=" + converted + "&rtype=CSV"
    file_name = "export/" + time.strftime("%m-%d-%Y") + "/DEC_Data_From_" + str(i) + ".csv"
    with urllib.request.urlopen(urltoopen) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print("Data for the year " + str(i) + " has finished downloading.")

# Run the concatenation at this point, after all of the data has been downloaded
if answer.lower() == 'y' or answer.lower() == 'yes':
    concat(first_corrected, last_corrected)
