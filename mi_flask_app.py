from flask import Flask, render_template, Response, session, request, redirect, url_for, flash, jsonify
from ctypes import *
from ControllerClass import *
from StatusClass import *
from Proceso import *
import time
import socket

ctrlEjes=[]
ctrlEjes[1]=FMC4030(1,"192.168.18.105")
ctrlEjes[2]=FMC4030(2,"192.168.18.106")
ctrlEjes[3]=FMC4030(3,"192.168.18.107")
ctrlEjes[4]=FMC4030(4,"192.168.18.108")
time.sleep(1)

app = Flask(__name__)

@app.route("/")
def hello():
    return "<center><h1 style='color:blue'>YA HAY SERVIDOR WEB!!!</h1></center>"

@app.route('/datos_json/status1', methods=['GET'])
def fmc4030_status():
    
    return jsonify({"Inputs": str(ctrlEjes[1].ms.inputStatus[0]), "Outputs": str(ctrlEjes[1].ms.outputStatus[0]), "LimitN": str(ctrlEjes[1].ms.limitNStatus[0]), 
                    "LimitP": str(ctrlEjes[1].ms.limitPStatus[0]), "StatMach": str(ctrlEjes[1].ms.machineRunStatus[0]), "StatHome": str(ctrlEjes[1].ms.homeStatus[0]),
                    "PosX": str(ctrlEjes[1].ms.realPos[0]), "PosY": str(ctrlEjes[1].ms.realPos[1]), "PosZ": str(ctrlEjes[1].ms.realPos[2]), 
                    "StatX": str(ctrlEjes[1].ms.axisStatus[0]), "StatY": str(ctrlEjes[1].ms.axisStatus[1]), "StatZ": str(ctrlEjes[1].ms.axisStatus[2])})

@app.route('/datos_json/status2', methods=['GET'])
def fmc4030_status():
    
    return jsonify({"Inputs": str(ctrlEjes[2].ms.inputStatus[0]), "Outputs": str(ctrlEjes[2].ms.outputStatus[0]), "LimitN": str(ctrlEjes[2].ms.limitNStatus[0]), 
                    "LimitP": str(ctrlEjes[2].ms.limitPStatus[0]), "StatMach": str(ctrlEjes[2].ms.machineRunStatus[0]), "StatHome": str(ctrlEjes[2].ms.homeStatus[0]),
                    "PosX": str(ctrlEjes[2].ms.realPos[0]), "PosY": str(ctrlEjes[2].ms.realPos[1]), "PosZ": str(ctrlEjes[2].ms.realPos[2]), 
                    "StatX": str(ctrlEjes[2].ms.axisStatus[0]), "StatY": str(ctrlEjes[2].ms.axisStatus[1]), "StatZ": str(ctrlEjes[2].ms.axisStatus[2])})

@app.route('/datos_json/status3', methods=['GET'])
def fmc4030_status():
    
    return jsonify({"Inputs": str(ctrlEjes[3].ms.inputStatus[0]), "Outputs": str(ctrlEjes[3].ms.outputStatus[0]), "LimitN": str(ctrlEjes[3].ms.limitNStatus[0]), 
                    "LimitP": str(ctrlEjes[3].ms.limitPStatus[0]), "StatMach": str(ctrlEjes[3].ms.machineRunStatus[0]), "StatHome": str(ctrlEjes[3].ms.homeStatus[0]),
                    "PosX": str(ctrlEjes[3].ms.realPos[0]), "PosY": str(ctrlEjes[3].ms.realPos[1]), "PosZ": str(ctrlEjes[3].ms.realPos[2]), 
                    "StatX": str(ctrlEjes[3].ms.axisStatus[0]), "StatY": str(ctrlEjes[3].ms.axisStatus[1]), "StatZ": str(ctrlEjes[3].ms.axisStatus[2])})

@app.route('/datos_json/status4', methods=['GET'])
def fmc4030_status():
    
    return jsonify({"Inputs": str(ctrlEjes[4].ms.inputStatus[0]), "Outputs": str(ctrlEjes[4].ms.outputStatus[0]), "LimitN": str(ctrlEjes[4].ms.limitNStatus[0]), 
                    "LimitP": str(ctrlEjes[4].ms.limitPStatus[0]), "StatMach": str(ctrlEjes[4].ms.machineRunStatus[0]), "StatHome": str(ctrlEjes[4].ms.homeStatus[0]),
                    "PosX": str(ctrlEjes[4].ms.realPos[0]), "PosY": str(ctrlEjes[4].ms.realPos[1]), "PosZ": str(ctrlEjes[4].ms.realPos[2]), 
                    "StatX": str(ctrlEjes[4].ms.axisStatus[0]), "StatY": str(ctrlEjes[4].ms.axisStatus[1]), "StatZ": str(ctrlEjes[4].ms.axisStatus[2])})

@app.route('/datos_json/connect', methods=['POST'])
def fmc4030_connect():
    CtrlId = int(request.json['Id'])
    
    #Call connection method 
    ctrlEjes[CtrlId].connect_Machine()
    
    return jsonify({"funcion": "Connect", "estado": "OK"})

@app.route('/datos_json/disconnect', methods=['POST'])
def fmc4030_disconnect():
    CtrlId = int(request.json['Id'])
    
    #Call disconnection method 
    ctrlEjes[CtrlId].disconnect_Machine()
   
    time.sleep(0.3)
    
    return jsonify({"funcion": "Home", "estado": "OK"})

@app.route('/datos_json/set_output', methods=['POST'])
def set_output():
    CtrlId = int(request.json['Id'])
    OutId = int(request.json['OutId'])
    OutState = int(request.json['OutState'])
    
    #Call set output method 
    ctrlEjes[CtrlId].set_Output(OutId, OutState)
    
    return jsonify({"funcion": "Set Output", "estado": "OK"})

@app.route('/datos_json/stop_move', methods=['POST'])
def axe_stop():
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    AxeMode = int(request.json['Par1'])
    
    #Call stop axis method 
    ctrlEjes[CtrlId].stop_Axis(AxeId, AxeMode)
    
    return jsonify({"funcion": "Stop", "estado": "OK"})

@app.route('/datos_json/home_move', methods=['POST'])
def axe_home():
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    AxeSpeed = int(request.json['Par1'])
    # AxeAccDec = int(request.json['Acc'])
    # AxeHomeFall = int(request.json['Fall'])
    # AxeDir = int(request.json['Dir'])

    #Call home move method 
    ctrlEjes[CtrlId].home_Move(AxeId, AxeSpeed)
    
    return jsonify({"funcion": "Home", "estado": "OK"})

@app.route('/datos_json/jog_move', methods=['POST'])
def axe_jog():
    #Parametros Json 
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    AxePos = int(request.json['Par1'])
    # AxeSpeed = int(request.json['Speed'])
    # AxeAcc = int(request.json['Acc'])
    # AxeDec = int(request.json['Dec'])
    
    #Call jog move method 
    ctrlEjes[CtrlId].jog_Move(AxeId, AxePos)

    return jsonify({"funcion":"Jog", "estado": "OK"})

@app.route('/datos_json/abs_move', methods=['POST'])
def axe_absmove():
    # Parametros Json
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    AxePos = int(request.json['Par1'])
    AxeSpeed = int(request.json['Par2'])
    # AxeAcc = int(request.json['Acc'])
    # AxeDec = int(request.json['Dec'])
    
    #Call absolute move method 
    ctrlEjes[CtrlId].abs_Move(AxeId, AxePos, AxeSpeed)
    
    time.sleep(0.3)
    
    return jsonify({"funcion":"Abs", "estado": "OK"})

@app.route('/datos_json/rel_move', methods=['POST'])
def axe_relmove():
     # Parametros Json
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    AxePos = int(request.json['Par1'])
    AxeSpeed = int(request.json['Par2'])
    # AxeAcc = int(request.json['Acc'])
    # AxeDec = int(request.json['Dec'])
    
    #Call relative move method 
    ctrlEjes[CtrlId].rel_Move(AxeId, AxePos, AxeSpeed)
    
    return jsonify({"funcion":"Rel", "estado": "OK"})

@app.route('/datos_json/2axis_move', methods=['POST'])
def axe2_move():
     # Parametros Json
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    EndX = int(request.json['Par1'])
    # EndY = int(request.json['EndY'])
    # AxeSpeed = int(request.json['Speed'])
    # AxeAcc = int(request.json['Acc'])
    # AxeDec = int(request.json['Dec'])
    
    #Call 2 Axis move method 
    ctrlEjes[CtrlId].move_2Axis(AxeId, EndX) #, EndY, AxeSpeed, AxeAcc, AxeDec)
    
    return jsonify({"funcion":"2Axe", "estado": "OK"})

@app.route('/datos_json/3axis_move', methods=['POST'])
def axe3_move():
     # Parametros Json
    CtrlId = int(request.json['Id'])
    EndX = int(request.json['EndX'])
    EndY = int(request.json['EndY'])
    EndZ = int(request.json['EndZ'])
    AxeSpeed = int(request.json['Speed'])
    AxeAcc = int(request.json['Acc'])
    AxeDec = int(request.json['Dec'])
    
    #Call 3 Axis move method 
    ctrlEjes[CtrlId].move_3Axis(EndX, EndY, EndZ, AxeSpeed, AxeAcc, AxeDec)
    
    return jsonify({"funcion":"3Axe", "estado": "OK"})

@app.route('/datos_json/2arc_move', methods=['POST'])
def arc2_move():
     # Parametros Json
    CtrlId = int(request.json['Id'])
    AxeId = int(request.json['AxeId'])
    EndX = int(request.json['EndX'])
    EndY = int(request.json['EndY'])
    CenterX = int(request.json['CenterX'])
    CenterY = int(request.json['CenterY'])
    Radius = int(request.json['Radius'])
    AxeSpeed = int(request.json['Speed'])
    AxeAcc = int(request.json['Acc'])
    AxeDec = int(request.json['Dec'])
    AxeDir = int(request.json['Dir'])
    
    #Call Arc 2 Axis move method 
    ctrlEjes[CtrlId].move_Arc2Axis(AxeId, EndX, EndY, CenterX, CenterY, Radius, AxeSpeed, AxeAcc, AxeDec, AxeDir)
    
    return jsonify({"funcion":"2Arc", "estado": "OK"})

@app.route('/datos_json/seq_wirefeed', methods=['POST'])
def eq_wirefeed():
    CtrlId = int(request.json['Id'])
    StepId = int(request.json['Par1'])
    
    step_status = "Idle"

    #Secuencia de Ejes y Actuadores
    if CtrlId == 1:
        if StepId == 0:                                                     #Incializacion de ejes
            ctrlEjes[1].set_Output(DOut0,0)
            ctrlEjes[1].set_Output(DOut1,0)
            if ctrlEjes[1].AxisX_Home==0: ctrlEjes[1].home_Move(axisX,35)
            if ctrlEjes[1].AxisY_Home==0: ctrlEjes[1].home_Move(axisY,35)
            if ctrlEjes[1].AxisZ_Home==0: ctrlEjes[1].home_Move(axisZ,35)
            NroAlambres = 0
            step_status = "Done"
        if StepId == 1:                                                     #Posicion Inicial
            if (ctrlEjes[1].AxisX_Home==1) and (ctrlEjes[1].AxisY_Home==1) and (ctrlEjes[1].AxisZ_Home==1):
                #Posicion Inicial Ejes
                if (ctrlEjes[1].AxisX_Run == 0) and (ctrlEjes[1].AxisX_Home==0): ctrlEjes[1].abs_Move(axisX,1500,65)
                if (ctrlEjes[1].AxisY_Run == 0) and (ctrlEjes[1].AxisY_Home==0): ctrlEjes[1].abs_Move(axisY,1500,65)
                # if (ctrlEjes[1].AxisZ_Run == 0) and (ctrlEjes[1].AxisZ_Home==0): ctrlEjes[1].abs_Move(axisZ,650,45)
                
        if StepId == 2:                                                     #Recoger Alambre                                              
            if (ctrlEjes[1].AxisX_Home==1) and (ctrlEjes[1].AxisY_Home==1) and (ctrlEjes[1].AxisZ_Home==1):                                            #Recoger Alambre
                #Ejes posicion inicial
                if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,0,65)
                if (ctrlEjes[1].AxisY_Home==1) and (NroAlambres==0): ctrlEjes[1].abs_Move(axisY,0,65)
                if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,650,45)
        
        if StepId == 3:                                                     #Alimentar Alambre Soldadora                                           
            if ctrlEjes[1].AxisX_Home==1:                                            
                if NroAlambres==0:
                #Recoger Alambre, hasta el extremo
                    if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,2600,65)
                    #if ctrlEjes[1].AxisY_Home==1: ctrlEjes[1].abs_Move(axisY,0,65)
                    #if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,650,45)
                    
                if NroAlambres>0:
                    #Recoger Alambre, primera aproximacion
                    if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,2400,65)
                    #if ctrlEjes[1].AxisY_Home==1: ctrlEjes[1].abs_Move(axisY,0,65)
                    #if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,650,45)
                if NroAlambres==NroAlambres: NroAlambres= NroAlambres + 1 
                else: NroAlambres=1 
                    
        
        if StepId == 4:                                                     #Posicionar alambre para ingreso Soldadora                                           
            if (ctrlEjes[1].AxisX_Home==1) and (ctrlEjes[1].AxisY_Home==1) and (ctrlEjes[1].AxisZ_Home==1):                                            #Recoger Alambre
                #Posicionar Grippers
                if NroAlambres==0:
                    if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,2400,65)
                    if ctrlEjes[1].AxisY_Home==1: ctrlEjes[1].abs_Move(axisY,400,65)
                    #if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,650,45)
                
                if NroAlambres>0:
                    if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,2700,35)
                    # if ctrlEjes[1].AxisY_Home==1: ctrlEjes[1].abs_Move(axisY,400,65)
                    #if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,650,45)
                  
        
        if StepId == 5:                                                     #Posicionar alambre Salida Soldadora                                           
            if (ctrlEjes[1].AxisX_Home==1) and (ctrlEjes[1].AxisY_Home==1) and (ctrlEjes[1].AxisZ_Home==1):                                            #Recoger Alambre
                #Posicionar Grippers
                if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,2200,65)
                if ctrlEjes[1].AxisY_Home==1: ctrlEjes[1].abs_Move(axisY,2500,65)
                #if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,650,45)
        
        if StepId == 6:                                                     #Posicionar Soldadora                                           
            if (ctrlEjes[1].AxisX_Home==1) and (ctrlEjes[1].AxisY_Home==1) and (ctrlEjes[1].AxisZ_Home==1):                                            #Recoger Alambre
                #Posicionar Grippers
                # if ctrlEjes[1].AxisX_Home==1: ctrlEjes[1].abs_Move(axisX,2200,65)
                # if ctrlEjes[1].AxisY_Home==1: ctrlEjes[1].abs_Move(axisY,2500,65)
                if ctrlEjes[1].AxisZ_Home==1: ctrlEjes[1].abs_Move(axisZ,1000,55)
    
    return jsonify({"funcion": "Step"+str(StepId), "estado": step_status})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
