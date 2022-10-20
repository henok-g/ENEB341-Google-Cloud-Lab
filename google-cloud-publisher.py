# Copyright 2018 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python
import os
import time
import datetime
import json
from google.cloud import pubsub_v1
from oauth2client.client import GoogleCredentials
from tendo import singleton
import ctypes

me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

# constants - change to fit your project and location
SEND_INTERVAL = 10 #seconds
credentials = GoogleCredentials.get_application_default()
print(credentials)
# change project to your Project ID
project="careful-alloy-366115"
# change topic to your PubSub topic name
topic = "HenokTopic"
# set the following four constants to be indicative of where you are placing your weather sensor
sensorID = "s-Googleplex"
	
def createJSON(id, timestamp, zipcode, latitude, longitude, temperature, humidity, dewpoint, pressure):
    data = {
      'sensorID' : id,
      'timecollected' : timestamp,
      'zipcode' : zipcode, 
      'latitude' : latitude,
      'longitude' : longitude,
      'temperature' : temperature,
      'humidity' : humidity,
      'dewpoint' : dewpoint,
      'pressure' : pressure
    }

    json_str = json.dumps(data)
    return json_str

def main():
  publisher = pubsub_v1.PublisherClient()
  print(publisher)
  topicName = 'projects/' + project + '/topics/' + topic
  print(topicName)
  last_checked = 0
  while True:
    if time.time() - last_checked > SEND_INTERVAL:
      last_checked = time.time()
      
      #Call the c function for reporting data
      fun = ctypes.CDLL(os.path.abspath("libfun.so")).reportData
      fun.restype = ctypes.POINTER(ctypes.c_double * 7)
    
      data = fun().contents
      zipcode = data[0]
      latitude = data[1]
      longitude = data[2]
      temperature = data[3]
      humidity = data[4] 
      dewpoint = data[5]
      pressure = data[6]

      currentTime = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
      s = ", "
      weatherJSON = createJSON(sensorID, currentTime, zipcode, latitude, longitude, temperature, humidity, dewpoint, pressure)
      weatherJSONbytes = weatherJSON.encode('utf-8')
      print(weatherJSON)
      try:
        publisher.publish(topicName, weatherJSONbytes,placeholder='' )
        #publisher.publish(topicName, b'The rain in Wales falls mainly on the snails.')
        print("successfully publishing")
      except:
        print("There was an error publishing weather data.")
    time.sleep(0.5)

if __name__ == '__main__':
	main()
