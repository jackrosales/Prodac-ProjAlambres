import requests
import snap7
import time
from snap7 import util
from ClientHttp import *


class PLCDataParser(HTTPDataSender):
    
    id = 0
    plc_ip = '192.168.90.10'
    rack = 0
    slot = 1
    idCtrl = 1
    conn_diag = 0
    conn_stat_busy = False 
    
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
    
    
    def __init__(self, id, plc_ip, db_number, start, len):
        self.id = id
        self.plc_ip = plc_ip
        self.db_number = db_number
        self.start = start
        self.len = len
        self.plc = snap7.client.Client()
        self.connect_plc()
        super().__init__('http://192.168.90.78:5000/datos_json/', 'http://127.0.0.1:5000/datos_json/status')
        
    def __del__(self):
        self.disconnect_plc()    

    def connect_plc(self):
        self.conn = self.plc.connect(self.plc_ip, self.rack, self.slot)

    def disconnect_plc(self):
        self.plc.disconnect()

    def get_plc_data(self):
        self.data_gen = self.plc.db_read(self.db_number, self.start, 8)
        self.data_AxisX_STW = self.plc.db_read(self.db_number, self.start+8, 2)
        self.data_AxisX = self.plc.db_read(self.db_number, self.start+10, 22)
        self.data_AxisY_STW = self.plc.db_read(self.db_number, self.start+32, 2)
        self.data_AxisY = self.plc.db_read(self.db_number, self.start+34, 22)
        self.data_AxisZ_STW = self.plc.db_read(self.db_number, self.start+56, 2)
        self.data_AxisZ = self.plc.db_read(self.db_number, self.start+58, 22)
        self.data_23ARC = self.plc.db_read(self.db_number, self.start+80, 64)
    
    def set_plc_data(self):
        self.plc.db_write(self.db_number, self.start, self.data_gen)
        self.plc.db_write(self.db_number, self.start+8, self.data_AxisX_STW)
        self.plc.db_write(self.db_number, self.start+32, self.data_AxisY_STW)
        self.plc.db_write(self.db_number, self.start+56, self.data_AxisZ_STW)
        
    def get_fmc_values(self):
        # Parse Values PLC -> FMC
        
        # Axis X - Data Values
        ind = 0        
        for parX in self.data_struc["AxisX"]:
            if parX != "STW": 
                self.data_struc["AxisX"][parX] = util.get_int(self.data_AxisX, ind)
                ind+=2
        
        # Axis Y - Data Values
        ind = 0
        for parY in self.data_struc["AxisY"]:
            if parY != "STW":
                self.data_struc["AxisY"][parY] = util.get_int(self.data_AxisY, ind)
                ind+=2
        
        # Axis Z - Data Values
        ind = 0
        for parZ in self.data_struc["AxisZ"]:
            if parZ != "STW":
                self.data_struc["AxisZ"][parZ] = util.get_int(self.data_AxisZ, ind)
                ind+=2
        
        # 2Axis XY - Data Values
        ind = 0
        for parXY in self.data_struc["2Axis_XY"]:
            self.data_struc["2Axis_XY"][parXY] = util.get_word(self.data_23ARC, ind)
            ind+=2
        
        # 3Axis XYZ - Data Values    
        ind = 20
        for parXYZ in self.data_struc["3Axis_XYZ"]:
            self.data_struc["3Axis_XYZ"][parXYZ] = util.get_int(self.data_23ARC, ind)
            ind+=2
        
        # ARC XY - Data Values    
        ind = 40
        for parARC in self.data_struc["ARC_XY"]:
            self.data_struc["ARC_XY"][parARC] = util.get_int(self.data_23ARC, ind)
            ind+=2
    
    def set_fmc_values(self):
        # Parse values FMC -> PLC
        util.set_bool(self.data_gen, 0, 0, self.data_struc["SYSTEM"]["LINK"])
        util.set_int(self.data_gen, 2, self.data_struc["SYSTEM"]["STATUS"])
        util.set_bool(self.data_gen, 4, 0, self.data_struc["SYSTEM"]["INPUTS"]&0x01)
        util.set_bool(self.data_gen, 4, 1, self.data_struc["SYSTEM"]["INPUTS"]&0x02)
        util.set_bool(self.data_gen, 4, 2, self.data_struc["SYSTEM"]["INPUTS"]&0x04)
        util.set_bool(self.data_gen, 4, 3, self.data_struc["SYSTEM"]["INPUTS"]&0x08)
        util.set_bool(self.data_gen, 6, 0, self.data_struc["SYSTEM"]["OUTPUTS"]&0x01)
        util.set_bool(self.data_gen, 6, 1, self.data_struc["SYSTEM"]["OUTPUTS"]&0x02)
        util.set_bool(self.data_gen, 6, 2, self.data_struc["SYSTEM"]["OUTPUTS"]&0x04)
        util.set_bool(self.data_gen, 6, 3, self.data_struc["SYSTEM"]["OUTPUTS"]&0x08)
        util.set_int(self.data_AxisX_STW, 0, self.data_struc["AxisX"]["STW"])
        util.set_int(self.data_AxisY_STW, 0, self.data_struc["AxisY"]["STW"])
        util.set_int(self.data_AxisZ_STW, 0, self.data_struc["AxisZ"]["STW"])
    
    def send_http(self, AxeId):
        # Select Axis to move
        if AxeId == 0: Axis = "AxisX"
        elif AxeId == 1: Axis = "AxisY" 
        elif AxeId == 2: Axis = "AxisZ" 
        
        # Evaluating Axis CTW
        comm_jog_fwd = True if self.data_struc[Axis]["CTW"] & 0x0100 else  False
        comm_jog_rev = True if self.data_struc[Axis]["CTW"] & 0x0200 else  False
        comm_abs = True if self.data_struc[Axis]["CTW"] & 0x0400 else  False
        comm_rel = True if self.data_struc[Axis]["CTW"] & 0x0800 else  False
        comm_home = True if self.data_struc[Axis]["CTW"] & 0x1000 else  False
        comm_stop = True if self.data_struc[Axis]["CTW"] & 0x2000 else  False
        
        # Jog Move
        if (comm_jog_fwd or comm_jog_rev) and not self.conn_stat_busy :
            self.data_post = {"Id": self.id, "AxeId": AxeId, "Pos": 20 if comm_jog_fwd else -20, "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"], "Mode": 1}
            self.send_data("jog_move")
            self.conn_stat_busy = True   
        
        # Absolute Move
        if comm_abs and not self.conn_stat_busy :
            self.data_post = {"Id": self.id, "AxeId": AxeId, "Pos": self.data_struc[Axis]["SP_POS"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"]}
            self.send_data("abs_move")
            self.conn_stat_busy = True   
        
        # Relative Move
        if comm_rel and not self.conn_stat_busy :
            self.data_post = {"Id": self.id, "AxeId": AxeId, "Pos": self.data_struc[Axis]["SP_POS"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"]}
            self.send_data("rel_move")
            self.conn_stat_busy = True  
        
        # Home Move
        if comm_home and not self.conn_stat_busy :
            self.data_post = {"Id": self.id, "AxeId": AxeId, "Speed": self.data_struc[Axis]["SP_HVEL"], "Acc": self.data_struc[Axis]["HACC"], "Fall": self.data_struc[Axis]["FALL"], "Dir": self.data_struc[Axis]["DIR"]}
            self.send_data("home_move")
            self.conn_stat_busy = True  
            
        # Stop Move
        if comm_stop and not self.conn_stat_busy :
            self.data_post = {"Id": self.id, "AxeId": AxeId, "Mode": 2}
            self.send_data("stop_move")
            self.conn_stat_busy = True 
          


        
FMC01 = PLCDataParser(1,'192.168.90.10',43,0,144)
print (FMC01.data_struc["AxisX"]["STW"])
while True:
    if FMC01.data_struc["AxisX"]["CTW"] == 0: FMC01.conn_stat_busy =False
    
    FMC01.get_plc_data()
    time.sleep(0.1)
    FMC01.get_fmc_values()
    time.sleep(0.1)
    FMC01.send_http(0)
    time.sleep(0.1)
    FMC01.set_fmc_values()
    time.sleep(0.1)
    FMC01.set_plc_data()
    time.sleep(0.1)
