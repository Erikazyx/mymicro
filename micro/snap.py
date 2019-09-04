# Append MM directory to path
import sys
import os
from io import BytesIO
import base64
import matplotlib.pyplot as plt



sys.path.append('D:\\workshop\\project\\Micro-Manager-2.0beta3')
system_cfg_file = 'D:\\workshop\\project\\Micro-Manager-2.0beta3\\MMConfig_demo.cfg'

# For most devices it is unnecessary to change to the MM direcotry prior to importing, but in some cases (such as the
# pco.de driver), it is required.

prev_dir = os.getcwd()
os.chdir('D:\\workshop\\project\\Micro-Manager-2.0beta3') # MUST change to micro-manager directory for method to work
import MMCorePy


def initial():
    mmc = MMCorePy.CMMCore()  # Get micro-manager controller object
    # Load system configuration (loads all devices)
    mmc.loadSystemConfiguration(system_cfg_file)
    os.chdir(prev_dir)
    mmc.loadDevice('Cam', 'DemoCamera', 'DCam')
    mmc.loadDevice('xy', 'DemoCamera', 'DXYStage')
    mmc.loadDevice('autofocus', 'DemoCamera', 'DAutoFocus')
    mmc.loadDevice('z', 'DemoCamera', 'DStage')
    mmc.initializeAllDevices()
    mmc.setCameraDevice('Cam')
    return mmc


def snap(mmc):
    mmc.snapImage()
    img = mmc.getImage()
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.0)
    data = buf.getvalue()
    data = base64.encodebytes(data).decode('utf-8').replace('\n', '')
    buf.close()
    src = 'data:image/png;base64,' + str(data)
    # print(data)
    return {'src': src, 'array': data}


def move_stage(mmc, x, y):
    mm = mmc.setXYPosition(x, y)
    return mm


def get_position(mmc):
    x = mmc.getXPosition()
    y = mmc.getYPosition()
    z = mmc.getPosition()
    return {'x': x, 'y':y, 'z':z}


def set_z(mmc, z):
    mmc.setPosition(5.999)
    return mmc


def reset(mmc):
    mmc.reset()





if __name__ == '__main__':
    mmc = initial()
    mmc.setProperty('Cam','PixelType', '32bitRGB')
    mmc.snapImage()
    img = mmc.getImage()
    plt.imshow(img)
    print('the value of x axis:', mmc.getXPosition())
    print('the value of y axis:', mmc.getYPosition())
    plt.show()
    mmc.setXYPosition(0, 0)
    print('the value of x axis:', mmc.getXPosition())
    print('the value of y axis:', mmc.getYPosition())
    mmc.snapImage()
    img = mmc.getImage()
    plt.imshow(img)
    plt.show()
    mmc.setXYPosition(20, 20)
    print(mmc.getXPosition())
    print(mmc.getYPosition())
    mmc.snapImage()
    img = mmc.getImage()
    plt.imshow(img, cmap='gray')
    plt.show()
    mmc.reset()

    #  plt.show()
