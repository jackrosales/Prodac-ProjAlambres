import threading
import requests
import StatusClass
import snap7
import time
from snap7 import util
# from ctypes import *
from ClientHttp import *


class PLCDataParser(HTTPDataSender):
    
    id = 0
    plc_ip = '192.168.90.10'
    rack = 0
    slot = 1
    idCtrl = 1
    conn_diag = 0
    ctw_mask = { "AxisX": 0xFFFF, "AxisY": 0xFFFF, "AxisZ": 0xFFFF, "2Axis_XY": 0xFFFF, "3Axis_XYZ": 0xFFFF, "ARC_XY": 0xFFFF}
    
    data_struc = {
        "SYSTEM":{
            "LINK":     False,
            "STATUS":   0,
            "INPUTS":   0,
            "OUTPUTS":  0
        },
        "AxisX":{
            "STW":      0,
            "CTW":      0,
            "SP_POS":   0,
            "SP_VEL":   0,
            "SP_HVEL":  0,
            "PV_POS":   0,
            "PV_VEL":   0,
            "ACC":      0,
            "DEC":      0,
            "HACC":     0,
            "DIR":      0,
            "FALL":     0
            },
        "AxisY":{
            "STW":      0,
            "CTW":      0,
            "SP_POS":   0,
            "SP_VEL":   0,
            "SP_HVEL":  0,
            "PV_POS":   0,
            "PV_VEL":   0,
            "ACC":      0,
            "DEC":      0,
            "HACC":     0,
            "DIR":      0,
            "FALL":     0
            },
        "AxisZ":{
            "STW":      0,
            "CTW":      0,
            "SP_POS":   0,
            "SP_VEL":   0,
            "SP_HVEL":  0,
            "PV_POS":   0,
            "PV_VEL":   0,
            "ACC":      0,
            "DEC":      0,
            "HACC":     0,
            "DIR":      0,
            "FALL":     0
            },
        "2Axis_XY":{
            "CTW":       0,
            "SP_POSX":   0,
            "SP_POSY":   0,
            "SP_POSZ":   0,
            "SP_VEL":    0,
            "ACC":       0,
            "DEC":      0,
            "HACC":     0,
            "DIR":      0,
            "FALL":     0
            },
        "3Axis_XYZ":{
            "CTW":      0,
            "SP_POSX":   0,
            "SP_POSY":   0,
            "SP_POSZ":   0,
            "SP_VEL":  0,
            "ACC":      0,
            "DEC":      0,
            "HACC":     0,
            "DIR":      0,
            "FALL":     0
            },
        "ARC_XY":{
            "CTW":      0,
            "SP_POSX":   0,
            "SP_POSY":   0,
            "CENTERX":   0,
            "CENTERY":  0,
            "RADIUS":  0,
            "SP_VEL":  0,
            "ACC":      0,
            "DEC":      0,
            "HACC":     0,
            "DIR":      0,
            "FALL":     0
            }
    }
    
    stw_fmc={
        "Running" : False, "Pause": False, "Resume": False, "Stop": False, "LimitN": False, "LimitP": False, 
        "Home": False, "HomeDone": False, "AutoRun": False, "LimitN_None": False, "LimitP_None": False, "Home_None": False, "Home_Overtime": False
    }
    
    ctw_plc={
        "AbsXY": False, "AbsXZ": False, "AbsYZ": False, "AbsXYZ": False, "ArcXY": False, "ArcXZ": False, "ArcYZ": False, "Lock": False,
        "JogFwd": False, "JogRev": False, "Abs": False, "Rel": False, "Home": False, "Stop": False, "Pause": False, "Reset": False  
    }
    
    def __init__(self, id, plc_ip, db_number, start, len):
        self.id = id
        self.plc_ip = plc_ip
        self.db_number = db_number
        self.start = start
        self.len = len
        self.plc = snap7.client.Client()
        self.connect_plc()
        super().__init__('http://192.168.90.78:5000/datos_json/', 'http://192.168.90.78:5000/datos_json/status')
        self.listening_thread = threading.Thread(target=self.listening)
        self.listening_thread.daemon = True
        self.listening_thread.start()
        
    def __del__(self):
        self.disconnect_plc()    

    def connect_plc(self):
        self.conn = self.plc.connect(self.plc_ip, self.rack, self.slot)

    def disconnect_plc(self):
        self.plc.disconnect()

    def get_plc_data(self):
        self.data_gen = self.plc.db_read(self.db_number, self.start, 8)
        # Axis X
        self.data_AxisX_STW = self.plc.db_read(self.db_number, self.start+8, 2)
        self.data_AxisX_DATA = self.plc.db_read(self.db_number, self.start+10, 8)
        self.data_AxisX_POSACT = self.plc.db_read(self.db_number, self.start+18, 2)
        self.data_AxisX_VELACT = self.plc.db_read(self.db_number, self.start+20, 2)
        self.data_AxisX_PARAM = self.plc.db_read(self.db_number, self.start+22, 10)
        # Axis Y
        self.data_AxisY_STW = self.plc.db_read(self.db_number, self.start+32, 2)
        self.data_AxisY_DATA = self.plc.db_read(self.db_number, self.start+34, 8)
        self.data_AxisY_POSACT = self.plc.db_read(self.db_number, self.start+42, 2)
        self.data_AxisY_VELACT = self.plc.db_read(self.db_number, self.start+44, 2)
        self.data_AxisY_PARAM = self.plc.db_read(self.db_number, self.start+46, 10)
        # Axis Z
        self.data_AxisZ_STW = self.plc.db_read(self.db_number, self.start+56, 2)
        self.data_AxisZ_DATA = self.plc.db_read(self.db_number, self.start+58, 8)
        self.data_AxisZ_POSACT = self.plc.db_read(self.db_number, self.start+66, 2)
        self.data_AxisZ_VELACT = self.plc.db_read(self.db_number, self.start+68, 2)
        self.data_AxisZ_PARAM = self.plc.db_read(self.db_number, self.start+70, 10)
        
        self.data_2Axis = self.plc.db_read(self.db_number, self.start+80, 20)
        self.data_3Axis = self.plc.db_read(self.db_number, self.start+100, 20)
        self.data_2Arc = self.plc.db_read(self.db_number, self.start+120, 24)
    
    def set_plc_data(self):
        self.plc.db_write(self.db_number, self.start, self.data_gen)
        # Axis X
        self.plc.db_write(self.db_number, self.start+8, self.data_AxisX_STW)
        self.plc.db_write(self.db_number, self.start+18, self.data_AxisX_POSACT)
        self.plc.db_write(self.db_number, self.start+20, self.data_AxisX_VELACT)
        # Axis Y
        self.plc.db_write(self.db_number, self.start+32, self.data_AxisY_STW)
        self.plc.db_write(self.db_number, self.start+42, self.data_AxisY_POSACT)
        self.plc.db_write(self.db_number, self.start+44, self.data_AxisY_VELACT)
        # Axis Z
        self.plc.db_write(self.db_number, self.start+56, self.data_AxisZ_STW)
        self.plc.db_write(self.db_number, self.start+66, self.data_AxisZ_POSACT)
        self.plc.db_write(self.db_number, self.start+68, self.data_AxisZ_VELACT)
        
    def get_fmc_values(self):
        # Parse Values PLC -> FMC
        
        # Axis X - Data Values
        self.data_struc["AxisX"]["CTW"] = util.get_word(self.data_AxisX_DATA, 0)
        self.data_struc["AxisX"]["SP_POS"] = util.get_int(self.data_AxisX_DATA, 2)
        self.data_struc["AxisX"]["SP_VEL"] = util.get_int(self.data_AxisX_DATA, 4)  
        self.data_struc["AxisX"]["SP_HVEL"] = util.get_int(self.data_AxisX_DATA, 6) 
        self.data_struc["AxisX"]["ACC"] = util.get_int(self.data_AxisX_PARAM, 0)
        self.data_struc["AxisX"]["DEC"] = util.get_int(self.data_AxisX_PARAM, 2)
        self.data_struc["AxisX"]["HACC"] = util.get_int(self.data_AxisX_PARAM, 4)  
        self.data_struc["AxisX"]["DIR"] = util.get_int(self.data_AxisX_PARAM, 6)
        self.data_struc["AxisX"]["FALL"] = util.get_int(self.data_AxisX_PARAM, 8)  
        
        # Axis Y - Data Values
        self.data_struc["AxisY"]["CTW"] = util.get_int(self.data_AxisY_DATA, 0)
        self.data_struc["AxisY"]["SP_POS"] = util.get_int(self.data_AxisY_DATA, 2)
        self.data_struc["AxisY"]["SP_VEL"] = util.get_int(self.data_AxisY_DATA, 4)  
        self.data_struc["AxisY"]["SP_HVEL"] = util.get_int(self.data_AxisY_DATA, 6) 
        self.data_struc["AxisY"]["ACC"] = util.get_int(self.data_AxisY_PARAM, 0)
        self.data_struc["AxisY"]["DEC"] = util.get_int(self.data_AxisY_PARAM, 2)
        self.data_struc["AxisY"]["HACC"] = util.get_int(self.data_AxisY_PARAM, 4)  
        self.data_struc["AxisY"]["DIR"] = util.get_int(self.data_AxisY_PARAM, 6)
        self.data_struc["AxisY"]["FALL"] = util.get_int(self.data_AxisY_PARAM, 8) 
        
        # Axis Z - Data Values
        self.data_struc["AxisZ"]["CTW"] = util.get_int(self.data_AxisZ_DATA, 0)
        self.data_struc["AxisZ"]["SP_POS"] = util.get_int(self.data_AxisZ_DATA, 2)
        self.data_struc["AxisZ"]["SP_VEL"] = util.get_int(self.data_AxisZ_DATA, 4)  
        self.data_struc["AxisZ"]["SP_HVEL"] = util.get_int(self.data_AxisZ_DATA, 6) 
        self.data_struc["AxisZ"]["ACC"] = util.get_int(self.data_AxisZ_PARAM, 0)
        self.data_struc["AxisZ"]["DEC"] = util.get_int(self.data_AxisZ_PARAM, 2)
        self.data_struc["AxisZ"]["HACC"] = util.get_int(self.data_AxisZ_PARAM, 4)  
        self.data_struc["AxisZ"]["DIR"] = util.get_int(self.data_AxisZ_PARAM, 6)
        self.data_struc["AxisZ"]["FALL"] = util.get_int(self.data_AxisZ_PARAM, 8) 
        
        # 2Axis XY - Data Values
        ind = 0
        for parXY in self.data_struc["2Axis_XY"]:
            self.data_struc["2Axis_XY"][parXY] = util.get_word(self.data_2Axis, ind)
            ind+=2
        
        # 3Axis XYZ - Data Values    
        ind = 0
        for parXYZ in self.data_struc["3Axis_XYZ"]:
            self.data_struc["3Axis_XYZ"][parXYZ] = util.get_int(self.data_3Axis, ind)
            ind+=2
        
        # ARC XY - Data Values    
        ind = 0
        for parARC in self.data_struc["ARC_XY"]:
            self.data_struc["ARC_XY"][parARC] = util.get_int(self.data_2Arc, ind)
            ind+=2
    
    def set_fmc_values(self):
        # Parse values FMC -> PLC
        util.set_bool(self.data_gen, 0, 0, self.data_struc["SYSTEM"]["LINK"])
        util.set_int(self.data_gen, 2, self.data_struc["SYSTEM"]["STATUS"])
        util.set_bool(self.data_gen, 4, 0, True if self.data_struc["SYSTEM"]["INPUTS"]&0x01 else False)
        util.set_bool(self.data_gen, 4, 1, True if self.data_struc["SYSTEM"]["INPUTS"]&0x02 else False)
        util.set_bool(self.data_gen, 4, 2, True if self.data_struc["SYSTEM"]["INPUTS"]&0x04 else False)
        util.set_bool(self.data_gen, 4, 3, True if self.data_struc["SYSTEM"]["INPUTS"]&0x08 else False)
        util.set_bool(self.data_gen, 6, 0, True if self.data_struc["SYSTEM"]["OUTPUTS"]&0x01 else False)
        util.set_bool(self.data_gen, 6, 1, True if self.data_struc["SYSTEM"]["OUTPUTS"]&0x02 else False)
        util.set_bool(self.data_gen, 6, 2, True if self.data_struc["SYSTEM"]["OUTPUTS"]&0x04 else False)
        util.set_bool(self.data_gen, 6, 3, True if self.data_struc["SYSTEM"]["OUTPUTS"]&0x08 else False)
        util.set_word(self.data_AxisX_STW, 0, self.data_struc["AxisX"]["STW"])
        util.set_int(self.data_AxisX_POSACT, 0, self.data_struc["AxisX"]["PV_POS"])
        util.set_int(self.data_AxisX_VELACT, 0, self.data_struc["AxisX"]["PV_VEL"])
        util.set_word(self.data_AxisY_STW, 0, self.data_struc["AxisY"]["STW"])
        util.set_int(self.data_AxisY_POSACT, 0, self.data_struc["AxisY"]["PV_POS"])
        util.set_int(self.data_AxisY_VELACT, 0, self.data_struc["AxisY"]["PV_VEL"])
        util.set_word(self.data_AxisZ_STW, 0, self.data_struc["AxisZ"]["STW"])
        util.set_int(self.data_AxisZ_POSACT, 0, self.data_struc["AxisZ"]["PV_POS"])
        util.set_int(self.data_AxisZ_VELACT, 0, self.data_struc["AxisZ"]["PV_VEL"])
    
    def comm_axis(self, Axis):
        print("CTW1: {} {}",Axis, self.data_struc[Axis]["CTW"], self.id)
        ctw_tmp = self.data_struc[Axis]["CTW"]
        self.data_struc[Axis]["CTW"] = self.data_struc[Axis]["CTW"] & self.ctw_mask[Axis]
        self.ctw_mask[Axis] = ctw_tmp ^ 0xFFFF
        print("CTW2: {} {}",self.data_struc[Axis]["CTW"], self.id)
        ind = 0x0001
        for x in self.ctw_plc:
            self.ctw_plc[x] = True if self.data_struc[Axis]["CTW"] & ind else False
            ind = ind <<1
        # print(self.ctw_plc)
    def axis_move(self, Axis):
        AxisId = 0 if Axis == "AxisX" else 1 if Axis == "AxisY" else 2 if Axis == "AxisZ" else 0
        
        self.comm_axis(Axis)
        
        # Jog Move
        if (self.ctw_plc["JogFwd"] ^ self.ctw_plc["JogRev"]) :
            self.data_post = {"Id": self.id, "AxeId": AxisId, "Pos": 20 if self.ctw_plc["JogFwd"] else -20, "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"], "Mode": 1}
            self.send_data("jog_move")
             
        # Absolute Move
        if self.ctw_plc["Abs"] :
            self.data_post = {"Id": self.id, "AxeId": AxisId, "Pos": self.data_struc[Axis]["SP_POS"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"]}
            self.send_data("abs_move")
               
        # Relative Move
        if self.ctw_plc["Rel"] :
            self.data_post = {"Id": self.id, "AxeId": AxisId, "Pos": self.data_struc[Axis]["SP_POS"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"]}
            self.send_data("rel_move") 
            
        # Home Move
        if self.ctw_plc["Home"] :
            self.data_post = {"Id": self.id, "AxeId": AxisId, "Speed": self.data_struc[Axis]["SP_HVEL"], "Acc": self.data_struc[Axis]["HACC"], "Fall": self.data_struc[Axis]["FALL"], "Dir": self.data_struc[Axis]["DIR"]}
            self.send_data("home_move") 
                
        # Stop Move
        if self.ctw_plc["Stop"] :
            self.data_post = {"Id": self.id, "AxeId": AxisId, "Mode": 1}
            self.send_data("stop_move")

    
    def send_http(self):
        # Axis X
        self.axis_move("AxisX")
        
        # Axis Y
        self.axis_move("AxisY")
        
        # Axis Z
        self.axis_move("AxisZ")
         
        # 2Axis Move
        self.comm_axis("2Axis_XY")
        if (self.ctw_plc["AbsXY"] ^ self.ctw_plc["AbsXZ"] ^ self.ctw_plc["AbsYZ"]) :
            axe = 3 if self.ctw_plc["AbsXY"] else 5 if self.ctw_plc["AbsXZ"] else 6 if self.ctw_plc["AbsYZ"] else 3
                
            self.data_post = {"Id": self.id, "AxeId": axe, "EndX": self.data_struc["2AxisS_XY"]["SP_POSX"], "EndY": self.data_struc["2Axis_XY"]["SP_POSY"], "Speed": self.data_struc["2Axis_XY"]["SP_VEL"], "Acc": self.data_struc["2Axis_XY"]["ACC"], "Dec": self.data_struc["2Axis_XY"]["DEC"]}
            self.send_data("2axis_move")
            
        # 3Axis Move
        self.comm_axis("3Axis_XYZ")
        if self.ctw_plc["AbsXYZ"] :
            self.data_post = {"Id": self.id, "EndX": self.data_struc["3Axis_XYZ"]["SP_POSX"], "EndY": self.data_struc["3Axis_XYZ"]["SP_POSY"], "EndZ": self.data_struc["3Axis_XYZ"]["SP_POSZ"], "Speed": self.data_struc["3Axis_XYZ"]["SP_VEL"], "Acc": self.data_struc["3Axis_XYZ"]["ACC"], "Dec": self.data_struc["3Axis_XYZ"]["DEC"]}
            self.send_data("3axis_move")
            
        # 2Arc Move
        self.comm_axis("ARC_XY")
        if (self.ctw_plc["ArcXY"] ^ self.ctw_plc["ArcXZ"] ^ self.ctw_plc["ArcYZ"]) :
            axe = 3 if self.ctw_plc["ArcXY"] else 5 if self.ctw_plc["ArcXZ"] else 6 if self.ctw_plc["ArcYZ"] else 3
            
            self.data_post = {"Id": self.id, "AxeId": axe, "EndX": self.data_struc["ARC_XY"]["SP_POSX"], "EndY": self.data_struc["ARC_XY"]["SP_POSY"], "CenterX": self.data_struc["ARC_XY"]["CENTERX"], "CenterY": self.data_struc["ARC_XY"]["CENTERY"], "Radius": self.data_struc["ARC_XY"]["RADIUS"], "Speed": self.data_struc["ARC_XY"]["SP_VEL"], "Acc": self.data_struc["ARC_XY"]["ACC"], "Dec": self.data_struc["ARC_XY"]["DEC"], "Dir": self.data_struc["ARC_XY"]["DIR"]}
            self.send_data("2arc_move")
            
    def stw_proc(self, status: int):
        ind = 1
        for x in self.stw_fmc:
            self.stw_fmc[x] = True if status & ind else False
            ind = ind<<1
        # print("Status1: ", self.stw_fmc)
        stw = 0
        stw = (stw | 0x0100) if self.stw_fmc["Running"] else (stw & 0xfeff) #Run
        stw = (stw | 0x0200) if self.stw_fmc["Stop"] else (stw & 0xfdff) #Stop
        stw = (stw | 0x0400) if self.stw_fmc["Home"] else (stw & 0xfbff) #Home
        stw = (stw | 0x0800) if self.stw_fmc["LimitN"] else (stw & 0xf7ff) #LimN
        stw = (stw | 0x1000) if self.stw_fmc["LimitP"] else (stw & 0xefff) #LimP
        stw = (stw | 0x4000) if self.stw_fmc["LimitN"] or self.stw_fmc["LimitP"] else (stw & 0xbfff) #Lock
        stw = (stw | 0x8000) if self.stw_fmc["Home"] else (stw & 0x7fff) #Home Done
        # print("Status2: ", stw)
        return stw
 
    def recieve_http(self):
        get_data = self.receive_data(self.id)  
        # Data I/O 
        self.data_struc['SYSTEM']['INPUTS'] = int(get_data['Inputs']) 
        self.data_struc['SYSTEM']['OUTPUTS'] = int(get_data['Outputs'])
        # Data Axis X
        self.data_struc['AxisX']['PV_POS'] = round(float(get_data['PosX']))
        self.data_struc['AxisX']['STW'] = self.stw_proc(int(get_data['StatX']))
        # Data Axis Y
        self.data_struc['AxisY']['PV_POS'] = round(float(get_data['PosY']))
        self.data_struc['AxisY']['STW'] = self.stw_proc(int(get_data['StatY']))
        # Data Axis Y
        self.data_struc['AxisZ']['PV_POS'] = round(float(get_data['PosZ']))
        self.data_struc['AxisZ']['STW'] = self.stw_proc(int(get_data['StatZ']))
        
        # print(self.data_struc['AxisX']['PV_POS'])
        print(int(get_data['StatX']))
    
    def listening(self):
        while True:
        
            self.get_plc_data()
            time.sleep(0.02)
            self.get_fmc_values()
            self.recieve_http()
            self.send_http()
            self.set_fmc_values()
            self.set_plc_data()
            time.sleep(0.02)

