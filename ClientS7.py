import requests
import snap7
import time
from snap7 import util


class PLCDataParser:
    
    plc_ip = '192.168.90.10'
    rack = 0
    slot = 1
    idCtrl = 1
    conn_diag = 0
    conn_stat_busy = False 
    
    fmc_data = {
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
    
    
    def __init__(self, plc_ip, db_number, start, len):
        self.plc_ip = plc_ip
        self.db_number = db_number
        self.start = start
        self.len = len
        self.plc = snap7.client.Client()
        

    def connect_plc(self):
        self.conn = self.plc.connect(self.plc_ip, self.rack, self.slot)

    def disconnect_plc(self):
        self.plc.disconnect()

    def get_plc_data(self):
        self.data = self.plc.db_read(self.db_number, self.start, self.len)
    
    def set_plc_data(self):
        self.plc.db_write(self.db_number, self.start, self.data)
        
    def get_fmc_values(self):
        # Parse Values PLC -> FMC
        
        # Axis X - Data Values
        ind = 8        
        for parX in self.fmc_data["AxisX"]:
            if parX != "STW": self.fmc_data["AxisX"][parX] = util.get_int(self.data, ind)
            ind+=2
        
        # Axis Y - Data Values
        ind = 32
        for parY in self.fmc_data["AxisY"]:
            if parY != "STW": self.fmc_data["AxisY"][parY] = util.get_int(self.data, ind)
            ind+=2
        
        # Axis Z - Data Values
        ind = 56
        for parZ in self.fmc_data["AxisZ"]:
            if parZ != "STW": self.fmc_data["AxisZ"][parZ] = util.get_int(self.data, ind)
            ind+=2
        
        # 2Axis XY - Data Values
        ind = 80
        for parXY in self.fmc_data["2Axis_XY"]:
            self.fmc_data["2Axis_XY"][parXY] = util.get_word(self.data, ind)
            ind+=2
        
        # 3Axis XYZ - Data Values    
        ind = 100
        for parXYZ in self.fmc_data["3Axis_XYZ"]:
            self.fmc_data["3Axis_XYZ"][parXYZ] = util.get_int(self.data, ind)
            ind+=2
        
        # ARC XY - Data Values    
        ind = 120
        for parARC in self.fmc_data["ARC_XY"]:
            self.fmc_data["ARC_XY"][parARC] = util.get_int(self.data, ind)
            ind+=2
    
    def set_fmc_values(self):
        # Parse values FMC -> PLC
        util.set_bool(self.data, 0, 0, self.fmc_data["SYSTEM"]["LINK"])
        util.set_int(self.data, 2, self.fmc_data["SYSTEM"]["STATUS"])
        util.set_bool(self.data, 4, 0, self.fmc_data["SYSTEM"]["INPUTS"]&0x01)
        util.set_bool(self.data, 4, 1, self.fmc_data["SYSTEM"]["INPUTS"]&0x02)
        util.set_bool(self.data, 4, 2, self.fmc_data["SYSTEM"]["INPUTS"]&0x04)
        util.set_bool(self.data, 4, 3, self.fmc_data["SYSTEM"]["INPUTS"]&0x08)
        util.set_bool(self.data, 6, 0, self.fmc_data["SYSTEM"]["OUTPUTS"]&0x01)
        util.set_bool(self.data, 6, 1, self.fmc_data["SYSTEM"]["OUTPUTS"]&0x02)
        util.set_bool(self.data, 6, 2, self.fmc_data["SYSTEM"]["OUTPUTS"]&0x04)
        util.set_bool(self.data, 6, 3, self.fmc_data["SYSTEM"]["OUTPUTS"]&0x08)
        util.set_int(self.data, 8, self.fmc_data["AxisX"]["STW"])
        util.set_int(self.data, 32, self.fmc_data["AxisY"]["STW"])
        util.set_int(self.data, 56, self.fmc_data["AxisZ"]["STW"])
        
class HTTPDataSender:
    data_post = []
    data_get =[]
    post_api_url = 'http://localhost:5000/datos_json/'
    get_api_url = 'http://localhost:5000/datos_json/status'
    
    def __init__(self, post_api_url, get_api_url):
        self.post_api_url = post_api_url
        self.get_api_url = get_api_url

    def send_data(self, data):
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code == 200:
                print('HTTP POST request successful.')
            else:
                print('HTTP POST request failed. Status code:', response.status_code)
        except requests.exceptions.RequestException as e:
            print('HTTP POST request error:', e)
    
    def receive_data(self):
        response = requests.get(self.get_api_url)
        return response

        
FMC01 = PLCDataParser("192.168.90.10",43,0,144)
FMC01.connect_plc()
time.sleep(0.1)
FMC01.get_plc_data()
time.sleep(0.1)
FMC01.get_fmc_values()
time.sleep(0.1)
FMC01.fmc_data["AxisX"]["STW"] = 0x01
FMC01.set_fmc_values()
FMC01.set_plc_data()
time.sleep(0.1)


print(FMC01.fmc_data["AxisX"]["CTW"])
print(FMC01.fmc_data["AxisX"]["SP_POS"])
print(FMC01.fmc_data["AxisX"]["FALL"])



FMC01.disconnect_plc()