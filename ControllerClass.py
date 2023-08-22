import threading
from ctypes import *
from StatusClass import *
from ClientS7 import *
from Proceso import *
import socket
import time

class FMC4030:

    # Ruta de driver para controlador FMC4030
    so_file = "/home/ubuntu/fmc4030-rasperry-demo/libFMC4030-Lib.so"
    fmc4030 = CDLL(so_file)    
    ms = machine_status() # Instancia de estado
    
    # Número del controlador, este número de identificación es único
    id = 1 
    ip = '192.168.0.30'
    port = 8088
    
    # Actual Pos
    AxisX_RealPos = 0
    AxisY_RealPos = 0
    AxisZ_RealPos = 0
    
    # Home Status
    AxisX_Home = 0
    AxisY_Home = 0
    AxisZ_Home = 0
    
    # Run Status
    AxisX_Run = False
    AxisY_Run = False
    AxisZ_Run = False
    
    # DI Status
    DIn0 = False  #Sensor de alambre
    DIn1 = False
    DIn2 = False
    DIn3 = False
    
    
    def __init__(self, controller_id: int, ipAddr: str, port: int):
        self.id = controller_id
        self.ip = ipAddr
        self.port = port
        self.connect_Machine()
        self.listening_thread = threading.Thread(target=self.listening)
        self.listening_thread.daemon = True
        self.listening_thread.start()

    def __del__(self):
        self.disconnect_Machine()
        self.listening_thread.join()
    

    def connect_Machine(self):
        
        try:
            conn = self.fmc4030.FMC4030_Open_Device(self.id, c_char_p(bytes(self.ip, 'utf-8')), self.port)
            time.sleep(0.3)
            if conn ==0 :
                print("Connectado correctamente FMC: ", self.id)
                self.get_Status()
                time.sleep(0.3)
                # CtrlParseS7 = PLCDataParser(self.id,'192.168.90.78', 43,0,144)
            else: 
                print("Error de conexion FMC: ",self.id)
                raise ConnectionError(conn)
        except ConnectionError:
            print("Codiggo de error: ")
            raise
    
        print("Pos X: {:.2f} Y: {:.2f} Z: {:.2f}".format(self.ms.realPos[0], self.ms.realPos[1], self.ms.realPos[2]))
        print("Inputs: {}".format(self.ms.inputStatus[0]))
        print("Outputs: {}".format(self.ms.outputStatus[0]))
        print("LimitN: {}".format(self.ms.limitNStatus[0]))
        print("LimitP: {}".format(self.ms.limitPStatus[0]))
        print("Mach RUN: {}".format(self.ms.machineRunStatus[0]))
        print("Axe Stat X: {} Y: {} Z: {}".format(self.ms.axisStatus[0], self.ms.axisStatus[1], self.ms.axisStatus[2]))
        print("Home Stat: {}".format(self.ms.homeStatus[0]))
        
    def disconnect_Machine(self):
        # Código para desconectarse de la máquina
        print("Desconectando : {}".format(self.fmc4030.FMC4030_Close_Device(self.id)))

    def get_Status(self):
        # Código para leer status de la máquina
        self.fmc4030.FMC4030_Get_Machine_Status(self.id, pointer(self.ms))
        time.sleep(0.2)
        #Din 01: XS001
        self.DIn0 = False if self.ms.inputStatus[0] & 0x0001 else True
        self.DIn1 = False if self.ms.inputStatus[0] & 0x0002 else True
        self.DIn2 = False if self.ms.inputStatus[0] & 0x0004 else True
        self.DIn3 = False if self.ms.inputStatus[0] & 0x0008 else True
        #Set Home Status
        self.AxisX_Home = True if self.ms.axisStatus[0] & 0x0800 else False
        self.AxisY_Home = True if self.ms.axisStatus[1] & 0x0800 else False
        self.AxisZ_Home = True if self.ms.axisStatus[2] & 0x0800 else False
        #Set RUN Status
        self.AxisX_Run = True if self.ms.axisStatus[0] & 0x0001 else False
        self.AxisY_Run = True if self.ms.axisStatus[1] & 0x0001 else False
        self.AxisZ_Run = True if self.ms.axisStatus[2] & 0x0001 else False
        #Set Actual Pos
        self.AxisX_RealPos = int(self.ms.realPos[0])
        self.AxisY_RealPos = int(self.ms.realPos[1])
        self.AxisZ_RealPos = int(self.ms.realPos[2])
        
    
    def get_Input(self, IO):
        # Código para leer estatus entradas digitales
        if IO==DIn0: print("Get Input: {}".format(self.fmc4030.FMC4030_Get_Input(self.id, IO, pointer(self.DIn0))))
        elif IO==DIn1: print("Get Input: {}".format(self.fmc4030.FMC4030_Get_Input(self.id, IO, pointer(self.DIn1))))
        elif IO==DIn2: print("Get Input: {}".format(self.fmc4030.FMC4030_Get_Input(self.id, IO, pointer(self.DIn2))))
        elif IO==DIn3: print("Get Input: {}".format(self.fmc4030.FMC4030_Get_Input(self.id, IO, pointer(self.DIn3))))
        
        
    def set_Output(self, IO=DOut0, Status=0):
        # Código para activar salida digital
        self.fmc4030.FMC4030_Set_Output(self.id, IO, Status)
        
    def get_AxisIsStop(self, Axis=axisX):
        # Código para leer si el eje esta detenido
        match Axis:
            case 0: 
                axeState = self.fmc4030.FMC4030_Check_Axis_Is_Stop(self.id, axisX)
            case 1:
                axeState = self.fmc4030.FMC4030_Check_Axis_Is_Stop(self.id, axisY)
            case 2:
                axeState = self.fmc4030.FMC4030_Check_Axis_Is_Stop(self.id, axisZ)
            case 3:
                axeState = 1 if (self.fmc4030.FMC4030_Check_Axis_Is_Stop(self.id, axisX) and 
                            self.fmc4030.FMC4030_Check_Axis_Is_Stop(self.id, axisY) and 
                            self.fmc4030.FMC4030_Check_Axis_Is_Stop(self.id, axisZ)) else 0
        
        print("Axis is Stop: {} {}".format(Axis,axeState))
        return axeState
        
    def stop_Axis(self, Axis=axisX, Mode=2):
        print("Stop: {}".format(self.fmc4030.FMC4030_Stop_Single_Axis(self.id, Axis, Mode)))
        time.sleep(0.3)
    
    def home_Move(self, Axe=axisX, HomeSpeed=15, HomeAcc=200, HomeFall=15, HomeDir=2):
        # Código para poner a Home Eje
        print ("Home: {}".format(self.fmc4030.FMC4030_Home_Single_Axis(self.id, Axe, c_float(HomeSpeed), c_float(HomeAcc), c_float(HomeFall), HomeDir)))
        time.sleep(0.3)
    
    def jog_Move(self, Axe=axisX, AxePos=20, Speed=20, Acc=200, Dec=200):
        # Código para mover el Eje en modo JOG
        print ("Jog: {}".format(self.fmc4030.FMC4030_Jog_Single_Axis(self.id, Axe, c_float(AxePos), c_float(Speed), c_float(Acc), c_float(Dec), 1)))
        time.sleep(0.3)
    
    def abs_Move(self,Axe=axisX, AxePos=20, Speed=65, Acc=200, Dec=200):
        # Código para mover el Eje en modo Absoluto
        print ("Abs: {}".format(self.fmc4030.FMC4030_Jog_Single_Axis(self.id, Axe, c_float(AxePos), c_float(Speed), c_float(Acc), c_float(Dec), 2)))
        time.sleep(0.3)
    
    def rel_Move(self,Axe=axisX, AxePos=20, Speed=45, Acc=200, Dec=200):
        # Código para mover el Eje en modo Relativo
        print ("Rel: {}".format(self.fmc4030.FMC4030_Jog_Single_Axis(self.id, Axe, c_float(AxePos), c_float(Speed), c_float(Acc), c_float(Dec), 1)))
        time.sleep(0.3)
    
    def move_2Axis(self, Axis, EndX, EndY, Speed=10, Acc=200, Dec=200):
        # Código para mover 2 Ejes Sincronizados
        print ("2Axis: {}" + self.fmc4030.FMC4030_Line_2Axis(self.id, Axis, c_float(EndX), c_float(EndY), c_float(Speed), c_float(Acc), c_float(Dec)))
        time.sleep(0.3)
    
    def move_3Axis(self, EndX, EndY, EndZ, Speed=10, Acc=200, Dec=200):
        # Código para mover 3 Ejes Sincronizados
        print ("3Axis: {}".format(self.fmc4030.FMC4030_Line_3Axis(self.id, 0, c_float(EndX), c_float(EndY), c_float(EndZ), c_float(Speed), c_float(Acc), c_float(Dec))))
        time.sleep(0.3)
    
    def move_Arc2Axis(self, Axis, EndX, EndY, CenterX, CenterY, Radius, Speed=10, Acc=200, Dec=200, Dir=1):
        # Código para mover 2 Ejes Sincronizados
        print ("Arc2Axis: {}".format(self.fmc4030.FMC4030_Arc_2Axis(self.id, Axis, c_float(EndX), c_float(EndY), c_float(CenterX), c_float(CenterY), c_float(Radius), c_float(Speed), c_float(Acc), c_float(Dec), Dir)))
        time.sleep(0.3)

    def listening(self):
        while True:
            # Lectura de Status general
            self.get_Status()
            # Control Digital Output 1 - Axis X - Switching positiong 1500mm
            if (self.AxisX_RealPos > 1500) and (self.AxisX_Run==True) and (self.AxisX_Home==True): 
                self.set_Output(DOut0,1)
            elif ((self.AxisX_RealPos <= 1500) or (self.AxisX_Home==False)) and (self.AxisX_Run==1): self.set_Output(DOut0,0)
            # Control Digital Output 2 - Axis Y - Switching positiong 1500mm
            if (self.AxisY_RealPos > 1500) and (self.AxisY_Run==True) and (self.AxisY_Home==True): 
                self.set_Output(DOut1,1)
            elif ((self.AxisY_RealPos <= 1500) or (self.AxisY_Home==False)) and (self.AxisY_Run==1): self.set_Output(DOut1,0)
        
          

