#!/usr/bin/python

from flask import request,Flask, jsonify 
from flask_api import FlaskAPI
import RPi.GPIO as GPIO
from flask_cors import CORS
import json
import time

WAIT_TIME = 1  # [s] Time to wait between each refresh
FAN_MIN = 20  # [%] Fan minimum speed.
PWM_FREQ = 100  # [Hz] Change this value if fan has strange behavior
PWM_FREQ_2 = 100

LEDS = {"green": 16, "red": 18, "blue":11, "yellow":15, "white":13}
FAN_PIN = 12
FOCO_PIN = 7

with open('./configurador.json') as f:
        data = json.load(f)
        
commands=[];
pins=[];
value=[];

GPIO.setmode(GPIO.BOARD)
# GPIO.setup(LEDS["green"], GPIO.OUT)
# GPIO.setup(LEDS["red"], GPIO.OUT)
# GPIO.setup(LEDS["blue"], GPIO.OUT)
# GPIO.setup(LEDS["yellow"], GPIO.OUT)
# GPIO.setup(LEDS["white"], GPIO.OUT)
command_number=len(data['allCommands'])
for x in range(0,command_number):# data['GPIO']:
    GPIO.setup(data['allCommands'][x]["pin"], GPIO.OUT)
    commands.append(data['allCommands'][x]["orden"]);
    pins.append(data['allCommands'][x]["pin"]);
    value.append(data['allCommands'][x]["value"]);
    
print(commands, pins, value)

GPIO.setup(FOCO_PIN, GPIO.OUT)
GPIO.setup(FAN_PIN, GPIO.OUT)

speedSteps = [0,50,80,100]  # [%]

vent = GPIO.PWM(FAN_PIN, PWM_FREQ)
vent.start(100)

pwmMotor = GPIO.PWM(FOCO_PIN, PWM_FREQ_2)
pwmMotor.start(100)

i = 0
fanSpeed = 0
fanSpeedOld = 0

app = FlaskAPI(__name__, static_url_path='')
cors = CORS(app, resources={r"/led/*": {"origins": "*"}})
app = Flask(__name__, static_folder="")



@app.route('/json_2',methods=["POST"])
def commands_json_2():

    comando = json.loads(request.data).get("comando_final") 
    with open('./prueba_read_2.json') as f:
        data = json.load(f)
    for x in range(0,command_number):# data['GPIO']:
        GPIO.setup(data['allCommands'][x]["pin"], GPIO.OUT)
    print(comando)
    for x in range (0,len(data['allCommands'])):
        if data['allCommands'][x]["orden"] == comando:
            pos = x;
    #pos = data['commands'].index(comando)
    puerto = data['allCommands'][pos]["pin"]
    Valor = data['allCommands'][pos]["value"]
    print(pos,puerto,Valor)
    GPIO.output(puerto, Valor)
        
    return {"Value": Valor}

@app.route('/json',methods=["POST"])
def commands_json():
    
    comando = json.loads(request.data).get("comando_final") 
    #with open('./prueba_read_2.json') as f:
    #    data = json.load(f)
    #for x in range(0,command_number):# data['GPIO']:
    #    GPIO.setup(data['allCommands'][x]["pin"], GPIO.OUT)
    print(comando)
    print(commands,len(commands))
    Valor =0;
    for x in range (0,len(commands)):
        if commands[x] == comando:
            pos = x;
            #pos = data['commands'].index(comando)
            puerto = pins[pos]
            Valor = value[pos]
            print(pos,puerto,Valor)
            GPIO.output(puerto, Valor)
        
    return {"Value": Valor}

@app.route('/new_commands',methods=["POST"])
def new_comands():
    print("entra")
    data = json.loads(request.data)
    print(data)
    commands.clear();
    pins.clear();
    value.clear();
    command_number=len(data['allCommands'])
    for x in range(0,command_number):# data['GPIO']:
        GPIO.setup(data['allCommands'][x]["pin"], GPIO.OUT)

    for x in range (0,len(data['allCommands'])):
        commands.append(data['allCommands'][x]["orden"]);
        pins.append(data['allCommands'][x]["pin"]);
        value.append(data['allCommands'][x]["value"]);
    print(commands)
    with open('configurador.json', 'w') as outfile:
        json.dump(data,outfile)
    return {"Comandos cambiados":x}
    


@app.route('/', methods=["GET"])
def api_root():
    return {
           "led_url": request.url + "led/(green | red | blue | yellow | white)/",
             "led_url_POST": {"state": "(0 | 1)"}
                 }

@app.route('/led/<color>/', methods=["POST"])
def api_leds_control(color):
    print("LED")
    print("LED") 
    print("LED")
    print(color)
    if request.method == "POST":
        print (json.loads(request.data).get("state"))
        if color in LEDS:
            GPIO.output(LEDS[color], int(json.loads(request.data).get("state")))
    return {color: GPIO.input(LEDS[color])}

@app.route('/foco/<lvl>/', methods=["POST"])
def foco(lvl):
    if request.method == "POST":
        if lvl =="max":
            pwmMotor.ChangeDutyCycle(100)
        if lvl == "med":
            pwmMotor.ChangeDutyCycle(50)
        if lvl == "min":
            pwmMotor.ChangeDutyCycle(10)
        if lvl == "off":
            pwmMotor.ChangeDutyCycle(0)

        #resp = json.loads(request.data).get("percent")
        #print(resp)
        #pwmMotor.ChangeDutyCycle(int(resp))
        return jsonify({'Foco': 'ok'})


@app.route('/fan/<lvl>/', methods=["POST"])
def fan(lvl):
    if request.method == "POST":
        if lvl =="max":
            fanSpeed = speedSteps[3]
        if lvl == "high":
            fanSpeed = speedSteps[2]
        if lvl == "low":
            fanSpeed = speedSteps[1]
        if lvl == "off":
            fanSpeed = speedSteps[0]
        vent.ChangeDutyCycle(fanSpeed)
        #resp = json.loads(request.data).get("percent")
        #print(resp)
        #pwmMotor.ChangeDutyCycle(int(resp))
        return jsonify({'Ventilador': 'ok'})

if __name__ == "__main__":
    app.run()

# while True:
#    for i in range(100,-1,-1):
#        pwmMotor.ChangeDutyCycle(100 - i)
#        time.sleep(0.02)
#
#    print("Ciclo completo")
