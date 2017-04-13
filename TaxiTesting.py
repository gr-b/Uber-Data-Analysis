import json
import csv
import googlemaps
import datetime
from array import array
import urllib2


#A full event array looks like this
#[0.start_date, 1.end_date, 2.start_long, 3.start_lat, 4.end_long, 5.end_lat, 6.taxi_dist, 7.taxi_start(sec), 8.taxi_duriation(sec), 9.taxi_google_start_coords, 10.taxi_google_end_coords, 11.google_dist, 12.google_dur]

key = 'AIzaSyDVASMakv-4diGu3FRUmh8s3DMtct82ze0' #My google API key, plz don't abuse
max_read = 50 #The max driving events to read from a spreadsheet (So we don't overload my google API quota)

#Reads the important data from the CSV
#Will only take a data set if the the important data in the columns are not 0 or null
def readCSV(fileName):
    dataArray = [] #Stores data from the spreadsheet
    with open(fileName) as csvfile: #Open the CSV File
        reader = csv.DictReader(csvfile)
        for row in reader: #Get data from the csv file
            rowInvalid = False;
            '''rowData = [row['lpep_pickup_datetime'], row['Lpep_dropoff_datetime'],
                       row['Pickup_longitude'], row['Pickup_latitude'],
                       row['Dropoff_longitude'], row['Dropoff_latitude'],
                       row['Trip_distance']]'''
            rowData = [row['pickup_datetime'], row['dropoff_datetime'],
                       row['pickup_longitude'], row['pickup_latitude'],
                       row['dropoff_longitude'], row['dropoff_latitude'],
                       row['trip_distance']]
            for i in rowData:
                if i == '0' :
                    #The row is invalid if one of the attributes are 0
                    rowInvalid = True;
                    break;
            rowData[6] = int(float(rowData[6])*1609.34)
            if  not rowInvalid : #If the row has all the required data
                dataArray.append(rowData) #Add the row to the dataArray
            #Check to see if we've collected enough data
            if len(dataArray) >= max_read:
                break;
    return dataArray #Return the array containing the spreadsheet data

#Gets the JSON data for a google location
def getData(origin, dest, depart_time = ''):
    origin = 'origin=' + origin #start location (name or coords)
    dest = '&destination=' + dest #destination (name or coords)
    APIKey = '&key=' + key #API key
    depart_time = '&departure_time=' + depart_time
    url = 'https://maps.googleapis.com/maps/api/directions/json?' + origin + dest + depart_time + APIKey
    json = urllib2.urlopen(url)
    json = json.read()
    return json

#Gets the Google distance and duriation data and appends it to the data array.
def getDataMany(data):
    for i, event in enumerate(data):
        curEvent = getData(event[9], event[10], str(int(float(event[7]))))
        eventData = getJSONData(curEvent)
        data[i].append(eventData[0])
        data[i].append(eventData[1])
    return data
        
#Gets the distance and duriation data from the JSON
def getJSONData(json_data):
    parsed_json = json.loads(json_data)
    distance = parsed_json['routes'][0]['legs'][0]['distance']['value']
    duriation = parsed_json['routes'][0]['legs'][0]['duration']['value']
    retArray = [distance, duriation]
    return retArray

#Calculate the statistics of the data comparison
#[6] is taxi distance
#[7] is start time (Seconds since epoch)
#[8] is duriation
#[9] is coord start
#[10] is coord end
#[11] is google distance
#[12] is google time
def calcStats(data):
    ratioStats = []
    sumRatioStats = []
    sumDistRatio = 0
    sumTimeRatio = 0
    num = 0
    for i, event in enumerate(data):
        insert = []
        print "Dist, Record:" + str(data[i][6]) + ", Google:" + str(data[i][11])
        print "Time, Record:" + str(data[i][8]) + ", Google:" + str(data[i][12])
        if (data[i][11] != 0 and data[i][12] != 0) :
            distRatio = float(data[i][6])/data[i][11]
            timeRatio = float(data[i][8])/data[i][12]
            insert.append(distRatio)
            insert.append(timeRatio)
            ratioStats.append(insert)
            num = num + 1
    for i, item in enumerate(ratioStats):
        sumDistRatio = sumDistRatio + ratioStats[i][0]
        sumTimeRatio = sumTimeRatio + ratioStats[i][1]
    sumDistRatio = sumDistRatio/(num + 1)
    sumTimeRatio = sumTimeRatio/(num + 1)
    sumRatioStats.append(sumDistRatio)
    sumRatioStats.append(sumTimeRatio)
    return sumRatioStats

#Takes a dataArray and convert dates of the form M/D/Y H:M to datetime format
#Appends to each row, a cell that holds the seconds since epoch
def convertDates(data) :
    #Get time of jan 1st 1970
    epoch = datetime.datetime.utcfromtimestamp(0)
    #strFormat = '%m/%d/%Y %H:%M'
    strFormat = '%Y-%m-%d %H:%M:%S'
    for i, row in enumerate(data):
        for j, cell in enumerate(row[0:2]):
            dateTimeDate = datetime.datetime.strptime(cell, strFormat)
            dateTimeDate = dateTimeDate.replace(year=2017)
            data[i][j] = str(dateTimeDate)
            #If Start time
            if j == 0 :
                secondsSinceEpoch = str((dateTimeDate - epoch).total_seconds())
                data[i].append(secondsSinceEpoch)
            #If end time
            else :
                duriation = str(((dateTimeDate - epoch).total_seconds() - float(secondsSinceEpoch)))
                data[i].append(duriation)
    return data

def convertCoords(data) :
    for i, row in enumerate(data) :
        coordStart = row[3] + ',' + row[2]
        coordEnd = row[5] + ',' + row[4]
        data[i].append(coordStart)
        data[i].append(coordEnd)
    return data

def main():
    #Get the necessary Information
    Input = readCSV('yellow_tripdata_2013-08.csv')
    #Convert the dates in the data to datetime format
    #Also get the start time as the seconds since epoch
    testDate = convertDates(Input)
    #Convert the lattitude and longitude to a format google api can read
    testCoordData = convertCoords(testDate)
    #print testCoordData
    #Input the data into the google API
    GoogleData = getDataMany(testCoordData)
    #print GoogleData
    ratioData = calcStats(GoogleData)
    print ratioData

main();
