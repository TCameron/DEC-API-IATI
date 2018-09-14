import urllib.request
import urllib.parse
import shutil
import base64
import glob
import csv
from datetime import date

__author__ = "Timothy Cameron"
__email__ = "tcameron@devtechsys.com"
__date__ = "09-14-2018"
__version__ = "0.3"


def globit():
    interesting_files = glob.glob("*.csv")

    header_saved = False
    with open('output.csv', 'wb') as fout:
        for filename in interesting_files:
            with open(filename) as fin:
                header = next(fin)
                if not header_saved:
                    fout.write(bytes(header, 'UTF-8'))
                    header_saved = True
                for line in fin:
                    fout.write(bytes(line, 'UTF-8'))


# Method to combine the data downloaded from the DEC website into a single file
def concat(firstyear, lastyear):
    print("Combining files...")
    filename = ""
    for j in range(firstyear, (lastyear+1)):
        filename = "DEC_Data_From_" + str(j) + ".csv"
        with open(filename) as fin:
            conloop(fin, 1)
    print("finished")
    exit(0)


def conloop(infile, line):
    outputfilename = "DEC_Data_From_" + str(first) + "-" + str(last) + ".csv"
    files = glob.glob('*.csv')
    with open(outputfilename, 'w') as fout:
        for file_ in files:
            for entry in open(file_, 'r'):
                try:
                    fout.write(entry)
                    line += 1
                except UnicodeDecodeError:
                    conloop(infile, line+1)


def replace_line(filename, line_num, text):
    lines = open(filename, 'r').readlines()
    lines[line_num] = text
    out = open(filename, 'w')
    out.writelines(lines)
    out.close()


first = int(input("Input the first year to search for: "))
last = int(input("Input the last year to search for: "))
skip = input("Would you like combine preexisting files? [Y/N] ")
if skip.lower() == 'y' or skip.lower() == 'yes':
    # concat(first, last)
    globit()

# If the user answers y or yes, then concat data; Otherwise, end program
if first != last:
    answer = input("Would you like to combine the downloaded files? [Y/N] ")
else:
    answer = 'n'

# Error checking and correction
if last < first:
    temp = first
    first = last
    last = temp

if last < 1953:
    last = 1953
elif last > date.today().year:
    last = date.today().year
    print('Cannot search for dates in the future. Setting last year to: ' + str(last))


# Main loop to download the data
for i in range(first, (last+1)):
    codelist = [11, 12, 13, 14, 15, 16, 21, 22, 24, 25, 26, 27, 31, 32,
                33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 51, 52, 53, 54, 55, 56, 61, 62, 63]
    for j in codelist:
            print("Downloading data for the year " + str(i) + " and type " + str(j) + "...")
            search = 'documents.date_of_publication_freeforrm:(' + str(i) \
                     + ') AND documents.bibliographic_type_code=(' + str(j) + ')'
            byte_string = search.encode('utf-8')
            conv = base64.b64encode(byte_string)
            converted = str(conv).replace('b\'', '')
            converted = converted.replace('\'', '')
            converted = urllib.parse.quote_plus(converted)
            urltoopen = "https://dec.usaid.gov/api/qsearch.ashx?q=" + converted + "&rtype=CSV"
            file_name = "DEC_Data_From_" + str(i) + " " + str(j) + " Group.csv"
            with urllib.request.urlopen(urltoopen) as response, open(file_name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("Data for the year " + str(i) + " has finished downloading.")

# Run the concatenation at this point, after all of the data has been downloaded
if answer.lower() == 'y' or answer.lower() == 'yes':
    # concat(first, last)
    globit()
