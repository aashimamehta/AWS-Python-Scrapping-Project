'''
Author: Aashima Mehta
Data of Last Moification : 9/4/2020
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
import boto3

page = requests.get('https://forecast.weather.gov/MapClick.php?lat=47.60357000000005&lon=-122.32944999999995#.X1GtyXlKhPY') #website link that I parsed in this project
soup = BeautifulSoup(page.content, 'html.parser')
#print(soup) to print the html code of that website                 //a good check
week = soup.find(id ='seven-day-forecast-body')
#print(week)

# the days will be the item #
items = (week.find_all(class_='tombstone-container'))
#tombstone container is a list of all days and weather that are
#now stored in items list
#print(items[0])

#now extract the info required                                  #good checks
#print(items[0].find(class_='period-name').get_text())
#print(items[0].find(class_='short-desc').get_text())
#print(items[0].find(class_='temp').get_text())

period_names =[item.find(class_='period-name').get_text() for item in items]
short_desc =[item.find(class_='short-desc').get_text() for item in items]
temperature =[item.find(class_='temp').get_text() for item in items]
#print(period_names)                                                    #good checks
#print(short_desc)
#print(temperature)

def printReport(period_names, short_desc, temperature):
#converting the information above into a table to make it look better
    msg = ("Weather in Seattle for the next " + (str(len(temperature) - 1)) + " days is as follows: \n")
    for i in range(len(period_names)):
        msg += ("Day " + (str(i)) + ": " + period_names[i] + ", "+ short_desc[i]+", " +temperature[i] + "\n")
    return msg

print(printReport(period_names, short_desc, temperature))


# to send the message using AWS SNS Serives to the topic 
def main(message):
    topicArn = 'arn:aws:sns:XX-XXX-X:XXXXXXXXXXXX:XXXXXXXX'             #unique link for the topic arn goes here
    snsClient = boto3.client('sns','us-west-2')
    response = snsClient.publish(TopicArn=topicArn, Message=message,
                   Subject='Publish to group test' )


main(message)
