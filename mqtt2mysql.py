import paho.mqtt.client as mqtt
import pymysql.cursors
import sys
import json

#User variable for database name
dbName = "database"

# User variables for MQTT Broker connection
mqttBrokerPort = 1883
mqttBroker = "xxx.xxx.xxx.xxx"
mqttUser = "user"
mqttPassword = "password"

mysqlHost = "xxx.xxx.xxx.xxx"
mysqlUser = "user"
mysqlPassword = "password"

# This callback function fires when the MQTT Broker conneciton is established.  At this point a connection to MySQL server will be attempted.
def on_connect(client, userdata, flags, rc):
    print("MQTT Client Connected")
    client.subscribe("domoticz/in")
    try:
        db = pymysql.connect(host=mysqlHost, user=mysqlUser, password=mysqlPassword, db=dbName, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        db.close()
        print("MySQL Client Connected")
    except:
        sys.exit("Connection to MySQL failed")

# This function updates the sensor's information in the sensor index table
def sensor_update(db, payload, nbr):
    print(payload)
    cursor = db.cursor()
    insertRequest = "INSERT INTO sensors(idx, nvalue, svalue, nbr) VALUES("+ str(payload['idx'])+","+str(payload['nvalue'])+",\""+str(payload['svalue'])+"\",\""+str(nbr)+"\")"
    cursor.execute(insertRequest)
    db.commit()


# The callback for when a PUBLISH message is received from the MQTT Broker.
def on_message(client, userdata, msg):
    print("Transmission received")
    message = (msg.payload).decode("utf-8")
    message = message.replace("svalue1","svalue")
    print(message)
    nbr = 0
    if message.find('{') != -1 and message.find(';') == -1:
        payload = json.loads(message)
        db = pymysql.connect(host="localhost", user=mysqlUser, password=mysqlPassword, db=dbName,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        sensor_update(db,payload,nbr)
        print('data logged')
        db.close()

    if message.find('{') != -1 and message.find(';') != -1:
        inf = message.find('svalue')
        sup = message.find('Battery')
        submessage = message[inf+9:sup-3]
        newmessage = submessage.split(';')
        print(newmessage)
        payload = json.loads(message)
        for valeur in newmessage:
            payload['svalue'] = str(valeur)
            db = pymysql.connect(host="localhost", user=mysqlUser, password=mysqlPassword, db=dbName,charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
            sensor_update(db,payload,nbr)
            nbr += 1
            print('data logged')
            db.close()

# Connect the MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=mqttUser, password=mqttPassword)
try:
    client.connect(mqttBroker, mqttBrokerPort, 60)
except:
    sys.exit("Connection to MQTT Broker failed")
# Stay connected to the MQTT Broker indefinitely
client.loop_forever()
