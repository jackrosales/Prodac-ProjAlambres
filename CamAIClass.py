import cv2
import asyncio
import keyboard
import time
from onvif import ONVIFCamera, ONVIFService, ONVIFError

Min = {}
Max = {}

# def event_keyboard(k):
    # pass
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


# await mycam.update_xaddrs()

# ptz_service = mycam.create_ptz_service()
# media_service = mycam.create_media_service()

# mycam.
# ptzrequest = mycam.get_capabilities('GetConfigurationOptions')
# # Get target profile
# media_profile = media_service.GetProfiles()[0]
# ptzrequest.ConfigurationToken = media_profile.PTZConfiguration.token
# ptz_configuration_options = mycam.GetConfigurationOptions(ptzrequest)
# moverequest = mycam.create_type('ContinuousMove')
# moverequest.ProfileToken = media_profile.token

# if moverequest.Velocity is None:
#     moverequest.Velocity = mycam.GetStatus({'ProfileToken': media_profile.token}).Position
#     moverequest.Velocity.PanTilt.space = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].URI
#     moverequest.Velocity.Zoom.space = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

# direction = {
#         'panning': move_panning,
#         'upleft': move_upleft,
#         'up': move_up,
#         'upright': move_upright,
#         'left': move_left,
#         'right': move_right,
#         'downleft': move_downleft,
#         'down': move_down,
#         'downright': move_downright,
#         'wide': zoom_wide,
#         'tele': zoom_tele,
#         'in': iris_in,
#         'out': iris_out,
#     }

# func = direction['down']
# active = False


# def ptz_move(ptz, request, active):
#     if active:
#         ptz.ContinuousMove(request)
#     else:
#         ptz.Stop({'ProfileToken': request.ProfileToken})

# def move_down(ptz, request, active):
#     request.Velocity.PanTilt.y = -2
#     request.Velocity.PanTilt.x = 0
#     request.Velocity.Zoom.x = 0
#     ptz_move(ptz, request, active)


cap = cv2.VideoCapture('rtsp://admin:Bertek@206036@192.168.90.108')

# mycam = ONVIFCamera('192.168.90.108', 80, 'BERTEK', 'Bertek@2060', '/wsdl/')

# Configura la dirección IP, puerto, nombre de usuario y contraseña de la cámara ONVIF
CAMERA_IP = '192.168.90.108'
CAMERA_PORT = 80
USERNAME = 'BERTEK'
PASSWORD = 'Bertek@2060'

# Conectarse a la cámara ONVIF
def connect_to_camera():
    mycam = ONVIFCamera(CAMERA_IP, CAMERA_PORT, USERNAME, PASSWORD, 'D:\Documentos\PRODAC - ALAMBRES\Prodac-ProjAlambres-1\wsdl')
    return mycam

# Mover la cámara según la tecla presionada
def move_camera(key):
    if key.name == 'up':
        move_up()
    elif key.name == 'down':
        move_down()
    elif key.name == 'left':
        move_left()
    elif key.name == 'right':
        move_right()

# Mover la cámara hacia arriba
def move_up():
    ptz = get_ptz(mycam)
    ptz.ContinuousMove({'ProfileToken': cam_token, 'Velocity': {'PanTilt': {'x': 0, 'y': 1}}})
    time.sleep(0.1)
    ptz.Stop({'ProfileToken': cam_token})

# Mover la cámara hacia abajo
def move_down():
    ptz = mycam.create_ptz_service()
    ptz.ContinuousMove({'ProfileToken': cam_token, 'Velocity': {'PanTilt': {'x': 0, 'y': -1}}})
    time.sleep(0.1)
    ptz.Stop({'ProfileToken': cam_token})

# Mover la cámara hacia la izquierda
def move_left():
    ptz = mycam.create_ptz_service()
    ptz.ContinuousMove({'ProfileToken': cam_token, 'Velocity': {'PanTilt': {'x': -1, 'y': 0}}})
    time.sleep(0.1)
    ptz.Stop({'ProfileToken': cam_token})

# Mover la cámara hacia la derecha
def move_right():
    ptz = mycam.create_ptz_service()
    ptz.ContinuousMove({'ProfileToken': cam_token, 'Velocity': {'PanTilt': {'x': 1, 'y': 0}}})
    time.sleep(0.1)
    ptz.Stop({'ProfileToken': cam_token})

async def get_media_prof(cam):
    media = await cam.create_media_service()
    prof = await media.GetProfiles()
    cam_token = prof[0]._token
    return cam_token

async def get_ptz(cam):
    ptz = await cam.create_ptz_service()
    return ptz


if __name__ == '__main__':
    mycam = connect_to_camera()
    # media = get_media_serv(mycam)
    # profiles = get_media_prof(mycam)
    cam_token = get_media_prof(mycam)
    print(cam_token)
    time.sleep(3)
    print("Usa las teclas de dirección (arriba, abajo, izquierda, derecha) para mover la cámara ONVIF.")
    print("Presiona 'Q' para salir.")


    while True:    
        success, img = cap.read()
        cv2.imshow("Image", img)

        if (cv2.waitKey(1) & 0xFF) == ord('q'): 
            break
        else: keyboard.on_press(move_camera)
        # keyboard.wait('q')  # Esperar hasta que se presione la tecla 'Q' para salir

        # key = (cv2.waitKey(1) & 0xFF)
        # if  key == ord('q'): 
        #     break
        # elif key == ord('z') or key == ord('Z'):
        #     active=True
        #     func(mycam, moverequest, active)
        #     time.sleep(0.2  )
        #     active=False
        #     func(mycam, moverequest, active)
        # elif key == ord('s') or key == ord('S'):
        #     active=False
        #     func(mycam, moverequest, active)
        #     time.sleep(0.2)

    cv2.destroyAllWindows()    

    