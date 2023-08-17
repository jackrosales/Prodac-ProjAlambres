import requests
import StatusClass
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
        super().__init__('http://192.168.90.78:5000/datos_json/', 'http://192.168.90.78:5000/datos_json/status')
        
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
        self.plc.db_write(self.db_number, self.start+18, self.data_AxisZ_POSACT)
        self.plc.db_write(self.db_number, self.start+20, self.data_AxisZ_VELACT)
        
    def get_fmc_values(self):
        # Parse Values PLC -> FMC
        
        # Axis X - Data Values
        self.data_struc["AxisX"]["CTW"] = util.get_int(self.data_AxisX_DATA, 0)
        self.data_struc["AxisX"]["SP_POS"] = util.get_int(self.data_AxisX_DATA, 2)
        self.data_struc["AxisX"]["SP_VEL"] = util.get_int(self.data_AxisX_DATA, 4)  
        self.data_struc["AxisX"]["SP_HVEL"] = util.get_int(self.data_AxisX_DATA, 6) 
        self.data_struc["AxisX"]["ACC"] = util.get_int(self.data_AxisX_PARAM, 0)
        self.data_struc["AxisX"]["DEC"] = util.get_int(self.data_AxisX_PARAM, 2)
        self.data_struc["AxisX"]["HACC"] = util.get_int(self.data_AxisX_PARAM, 4)  
        self.data_struc["AxisX"]["DIR"] = util.get_int(self.data_AxisX_PARAM, 6)
        self.data_struc["AxisX"]["FALL"] = util.get_int(self.data_AxisX_PARAM, 8)  
        
        # Axis Y - Data Values
        self.data_struc["AxisX"]["CTW"] = util.get_int(self.data_AxisY_DATA, 0)
        self.data_struc["AxisX"]["SP_POS"] = util.get_int(self.data_AxisY_DATA, 2)
        self.data_struc["AxisX"]["SP_VEL"] = util.get_int(self.data_AxisY_DATA, 4)  
        self.data_struc["AxisX"]["SP_HVEL"] = util.get_int(self.data_AxisY_DATA, 6) 
        self.data_struc["AxisX"]["ACC"] = util.get_int(self.data_AxisY_PARAM, 0)
        self.data_struc["AxisX"]["DEC"] = util.get_int(self.data_AxisY_PARAM, 2)
        self.data_struc["AxisX"]["HACC"] = util.get_int(self.data_AxisY_PARAM, 4)  
        self.data_struc["AxisX"]["DIR"] = util.get_int(self.data_AxisY_PARAM, 6)
        self.data_struc["AxisX"]["FALL"] = util.get_int(self.data_AxisY_PARAM, 8) 
        
        # Axis Z - Data Values
        self.data_struc["AxisX"]["CTW"] = util.get_int(self.data_AxisZ_DATA, 0)
        self.data_struc["AxisX"]["SP_POS"] = util.get_int(self.data_AxisZ_DATA, 2)
        self.data_struc["AxisX"]["SP_VEL"] = util.get_int(self.data_AxisZ_DATA, 4)  
        self.data_struc["AxisX"]["SP_HVEL"] = util.get_int(self.data_AxisZ_DATA, 6) 
        self.data_struc["AxisX"]["ACC"] = util.get_int(self.data_AxisZ_PARAM, 0)
        self.data_struc["AxisX"]["DEC"] = util.get_int(self.data_AxisZ_PARAM, 2)
        self.data_struc["AxisX"]["HACC"] = util.get_int(self.data_AxisZ_PARAM, 4)  
        self.data_struc["AxisX"]["DIR"] = util.get_int(self.data_AxisZ_PARAM, 6)
        self.data_struc["AxisX"]["FALL"] = util.get_int(self.data_AxisZ_PARAM, 8) 
        
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
        util.set_bool(self.data_gen, 4, 0, self.data_struc["SYSTEM"]["INPUTS"]&0x01)
        util.set_bool(self.data_gen, 4, 1, self.data_struc["SYSTEM"]["INPUTS"]&0x02)
        util.set_bool(self.data_gen, 4, 2, self.data_struc["SYSTEM"]["INPUTS"]&0x04)
        util.set_bool(self.data_gen, 4, 3, self.data_struc["SYSTEM"]["INPUTS"]&0x08)
        util.set_bool(self.data_gen, 6, 0, self.data_struc["SYSTEM"]["OUTPUTS"]&0x01)
        util.set_bool(self.data_gen, 6, 1, self.data_struc["SYSTEM"]["OUTPUTS"]&0x02)
        util.set_bool(self.data_gen, 6, 2, self.data_struc["SYSTEM"]["OUTPUTS"]&0x04)
        util.set_bool(self.data_gen, 6, 3, self.data_struc["SYSTEM"]["OUTPUTS"]&0x08)
        util.set_int(self.data_AxisX_STW, 0, self.data_struc["AxisX"]["STW"])
        util.set_int(self.data_AxisX_POSACT, 0, self.data_struc["AxisX"]["PV_POS"])
        util.set_int(self.data_AxisX_VELACT, 0, self.data_struc["AxisX"]["PV_VEL"])
        util.set_int(self.data_AxisY_STW, 0, self.data_struc["AxisY"]["STW"])
        util.set_int(self.data_AxisY_POSACT, 0, self.data_struc["AxisY"]["PV_POS"])
        util.set_int(self.data_AxisY_VELACT, 0, self.data_struc["AxisY"]["PV_VEL"])
        util.set_int(self.data_AxisZ_STW, 0, self.data_struc["AxisZ"]["STW"])
        util.set_int(self.data_AxisZ_POSACT, 0, self.data_struc["AxisZ"]["PV_POS"])
        util.set_int(self.data_AxisZ_VELACT, 0, self.data_struc["AxisZ"]["PV_VEL"])
    
    def send_http(self):
        for AxeId in range(9):
            if AxeId == 4: AxeId+=1
            # Select Axis to move
            if AxeId == 0: Axis = "AxisX"
            elif AxeId == 1: Axis = "AxisY" 
            elif AxeId == 2: Axis = "AxisZ" 
            elif AxeId == 3: Axis = "2Axis_XY" 
            elif AxeId == 5: Axis = "2Axis_XY" 
            elif AxeId == 6: Axis = "2Axis_XY" 
            elif AxeId == 7: Axis = "3Axis_XYZ"
            elif AxeId == 8: Axis = "ARC_XY"  
            
            # Evaluating Axis CTW
            comm_jog_fwd = True if self.data_struc[Axis]["CTW"] & 0x0100 else  False
            comm_jog_rev = True if self.data_struc[Axis]["CTW"] & 0x0200 else  False
            comm_abs_Axis = True if self.data_struc[Axis]["CTW"] & 0x0400 else  False
            comm_rel = True if self.data_struc[Axis]["CTW"] & 0x0800 else  False
            comm_home = True if self.data_struc[Axis]["CTW"] & 0x1000 else  False
            comm_stop = True if self.data_struc[Axis]["CTW"] & 0x2000 else  False
            comm_abs_2AxisXY = True if self.data_struc[Axis]["CTW"] & 0x0001 else  False
            comm_abs_2AxisXZ = True if self.data_struc[Axis]["CTW"] & 0x0002 else  False
            comm_abs_2AxisYZ = True if self.data_struc[Axis]["CTW"] & 0x0004 else  False
            comm_abs_3Axis = True if self.data_struc[Axis]["CTW"] & 0x0008 else  False
            comm_abs_2Arc = True if self.data_struc[Axis]["CTW"] & 0x0010 else  False
            
            
            # Jog Move
            if (comm_jog_fwd or comm_jog_rev) and not self.conn_stat_busy :
                self.data_post = {"Id": self.id, "AxeId": AxeId, "Pos": 20 if comm_jog_fwd else -20, "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"], "Mode": 1}
                self.send_data("jog_move")
                self.conn_stat_busy = True   
            
            # Absolute Move
            if comm_abs_Axis and not self.conn_stat_busy :
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
            
            # 2Axis Move
            if (comm_abs_2AxisXY or comm_abs_2AxisXZ or comm_abs_2AxisYZ) and not self.conn_stat_busy :
                if comm_abs_2AxisXY: axe = 3
                elif comm_abs_2AxisXZ: axe = 5
                elif comm_abs_2AxisYZ: axe = 6
                
                self.data_post = {"Id": self.id, "AxeId": axe, "EndX": self.data_struc[Axis]["SP_POSX"], "EndY": self.data_struc[Axis]["SP_POSY"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"]}
                self.send_data("2axis_move")
                self.conn_stat_busy = True  
            
            # 3Axis Move
            if comm_abs_3Axis and not self.conn_stat_busy :
                self.data_post = {"Id": self.id, "EndX": self.data_struc[Axis]["SP_POSX"], "EndY": self.data_struc[Axis]["SP_POSY"], "EndZ": self.data_struc[Axis]["SP_POSZ"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"]}
                self.send_data("3axis_move")
                self.conn_stat_busy = True  
            
            # 2Arc Move
            if comm_abs_2Arc and not self.conn_stat_busy :
                self.data_post = {"Id": self.id, "AxeId": 3, "EndX": self.data_struc[Axis]["SP_POSX"], "EndY": self.data_struc[Axis]["SP_POSY"], "CenterX": self.data_struc[Axis]["CENTERX"], "CenterY": self.data_struc[Axis]["CENTERY"], "Radius": self.data_struc[Axis]["RADIUS"], "Speed": self.data_struc[Axis]["SP_VEL"], "Acc": self.data_struc[Axis]["ACC"], "Dec": self.data_struc[Axis]["DEC"], "Dir": self.data_struc[Axis]["DIR"]}
                self.send_data("2arc_move")
                self.conn_stat_busy = True 
     
    def recieve_http(self):
        get_data = self.receive_data(self.id)  
        # Data Axis X
        self.data_struc['AxisX']['INPUTS'] = int(get_data['Inputs']) 
        self.data_struc['AxisX']['OUTPUTS'] = int(get_data['Outputs'])
        self.data_struc['AxisX']['PV_POS'] = int(get_data['PosX'])
        status = (status or 0x0100) if int(get_data['StatX']) & 0x0001 else (status and 0xfeff) #Run
        status = (status or 0x0200) if int(get_data['StatX']) & 0x0008 else (status and 0xfdff) #Stop
        status = (status or 0x0400) if int(get_data['StatX']) & 0x0080 else (status and 0xfbff) #Home
        status = (status or 0x0800) if int(get_data['StatX']) & 0x0010 else (status and 0xf7ff) #LimN
        status = (status or 0x1000) if int(get_data['StatX']) & 0x0020 else (status and 0xefff) #LimP
        status = (status or 0x4000) if (status & 0x0010) or (status & 0x0020) else (status and 0xbfff) #Lock
        status = (status or 0x8000) if int(get_data['StatX']) & 0x0040 else (status and 0x7fff) #Home Done
        self.data_struc['AxisX']['STW'] = status


   
FMC01 = PLCDataParser(1,'192.168.90.10',43,0,144)
print (FMC01.data_struc["AxisX"]["STW"])
FMC01.recieve_http()
while True:
    if FMC01.data_struc["AxisX"]["CTW"] == 0: FMC01.conn_stat_busy =False
    
    FMC01.get_plc_data()
    time.sleep(0.1)
    FMC01.get_fmc_values()
    time.sleep(0.1)
    FMC01.send_http()
    time.sleep(0.1)
    FMC01.set_fmc_values()
    time.sleep(0.1)
    FMC01.set_plc_data()
    time.sleep(0.1)
