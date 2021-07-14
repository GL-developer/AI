import time, threading
if __name__ == '__main__':
    import DobotDllType as dType
else:
    from . import DobotDllType as dType
    
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

def init():
    global api
    api = dType.load()
    state = dType.ConnectDobot(api, "", 115200)[0]
    print("Connect status:",CON_STR[state])
    dType.SetQueuedCmdClear(api)
    
def PickAndPlace(*args):
    pick, place, height  = args

    #Pick
    dType.SetPTPCmd(api,1, pick['X'], pick['Y'], height, pick['R'],1)
    dType.SetPTPCmd(api,1, pick['X'], pick['Y'], pick['Z'], pick['R'],1)
    dType.SetEndEffectorSuctionCup(api,1,1,1)
    dType.SetWAITCmd(api,1,1)
    dType.SetPTPCmd(api,1, pick['X'], pick['Y'], height, pick['R'],1)
    
    #Place
    dType.SetPTPCmd(api,1, place['X'], place['Y'], height, place['R'],1)
    dType.SetPTPCmd(api,1, place['X'], place['Y'], place['Z'], place['R'],1)
    dType.SetEndEffectorSuctionCup(api,0,0,1)
    index = dType.SetPTPCmd(api,1, place['X'], place['Y'], height, place['R'],1)
    while True:
        if dType.GetQueuedCmdCurrentIndex(api) == index:
            break;
def disconnect():
    dType.DisconnectDobot(api)
    
def gogo():
    From = {'X':200, 'Y':100, 'Z':-40, 'R':0}
    To = {'X':200, 'Y':-100, 'Z':-40, 'R':0}
    height = 0
    PickAndPlace(From,To,height)
    
if __name__ == '__main__':
    gogo()
    