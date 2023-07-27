import cv2
import asyncio
import time
from onvif import ONVIFCamera, ONVIFService, ONVIFError

Min = {}
Max = {}

def event_keyboard(k):
    pass
    # global exit_program

    # if k == 27:  # esc
    #     exit_program = 1

    # elif k == ord('w') or k == ord('W'):
    #     X.relative_move(0, 0.1, 0)

    # elif k == ord('a') or k == ord('A'):
    #     X.relative_move(-0.1, 0, 0)

    # elif k == ord('s') or k == ord('S'):
    #     X.relative_move(0, -0.1, 0)

    # elif k == ord('d') or k == ord('D'):
    #     X.relative_move(0.1, 0, 0)

    # elif k == ord('h') or k == ord('H'):
    #     X.go_home_position()

    # elif k == ord('z') or k == ord('Z'):
    #     X.relative_move(0, 0, 0.05)

    # elif k == ord('x') or k == ord('X'):
    #     X.relative_move(0, 0, -0.05)

cap = cv2.VideoCapture('rtsp://admin:Bertek@206036@192.168.90.108')

mycam = ONVIFCamera('192.168.90.108', 80, 'BERTEK', 'Bertek@2060', '/wsdl/')

# await mycam.update_xaddrs()

ptz_service = mycam.create_ptz_service()
media_service = mycam.create_media_service()

mycam.
ptzrequest = mycam.get_capabilities('GetConfigurationOptions')
# Get target profile
media_profile = media_service.GetProfiles()[0]
ptzrequest.ConfigurationToken = media_profile.PTZConfiguration.token
ptz_configuration_options = mycam.GetConfigurationOptions(ptzrequest)
moverequest = mycam.create_type('ContinuousMove')
moverequest.ProfileToken = media_profile.token

if moverequest.Velocity is None:
    moverequest.Velocity = mycam.GetStatus({'ProfileToken': media_profile.token}).Position
    moverequest.Velocity.PanTilt.space = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
    moverequest.Velocity.Zoom.space = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

direction = {
        'panning': move_panning,
        'upleft': move_upleft,
        'up': move_up,
        'upright': move_upright,
        'left': move_left,
        'right': move_right,
        'downleft': move_downleft,
        'down': move_down,
        'downright': move_downright,
        'wide': zoom_wide,
        'tele': zoom_tele,
        'in': iris_in,
        'out': iris_out,
    }

func = direction['down']
active = False


def ptz_move(ptz, request, active):
    if active:
        ptz.ContinuousMove(request)
    else:
        ptz.Stop({'ProfileToken': request.ProfileToken})

def move_down(ptz, request, active):
    request.Velocity.PanTilt.y = -2
    request.Velocity.PanTilt.x = 0
    request.Velocity.Zoom.x = 0
    ptz_move(ptz, request, active)

while True:    
    success, img = cap.read()
    cv2.imshow("Image", img)
    key = (cv2.waitKey(1) & 0xFF)
    if  key == ord('q'): 
       break
    elif key == ord('z') or key == ord('Z'):
        active=True
        func(mycam, moverequest, active)
        time.sleep(0.2)
        active=False
        func(mycam, moverequest, active)
    elif key == ord('s') or key == ord('S'):
        active=False
        func(mycam, moverequest, active)
        time.sleep(0.2)
        
cv2.destroyAllWindows()  
    