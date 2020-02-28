
import pyvisauto
import pyautogui
import pygetwindow
from numpy import random


# name of window
win = pygetwindow.getWindowsWithTitle("Girls' Frontline")[0]

# padding for window of MuMU emulator
top_pad = 36
bot_pad = 53
# region of just game screen
reg = [win.left, win.top+top_pad, win.width, win.height-(bot_pad+top_pad)]
# make it not move at speed of slow
pyvisauto.ImageMatch.MOUSE_MOVE_SPEED = 0


class Locations():
    def __init__(self):
        self.cc_1 = [992, 504, 61, 69]
        self.scarecrow = [1034, 23, 50, 45]


r = pyvisauto.Region(reg[0], reg[1], reg[2], reg[3])
loc = Locations()


def click(box, pad=(0, 0, 0, 0)):
    # clicks for the constant Locations and adds
    rx = random.randint(box[0] - pad[3], box[0] + box[2] + pad[1])
    ry = random.randint(box[1] - pad[0], box[1] + box[3] + pad[2])
    rx += win.left
    ry += win.top + top_pad
    pyautogui.click(rx, ry)
    pyautogui.sleep(0.5)


def deploy(deploy_location, timeout=10, delay=0.5):
    while timeout > 0:
        click(deploy_location)
        pyautogui.sleep(delay)
        found = r.exists('assets/ok.png', 0.9)
        timeout -= 1
        if found:
            m1 = r.find('assets/ok.png', 0.9, cached=True)
            m1.click()
            pyautogui.sleep(0.4)
            m1.click()
            break
    else:
        print('Timed out')


def planning(timeout=10, delay=0.5):
    planning_mode = False
    m1 = r.wait('assets/combat/battle/plan.png', 10, 0.9)
    pyautogui.sleep(1)
    while timeout > 0:
        try:
            m1.click()
            m1.wait_vanish('assets/combat/battle/plan.png', 1, 0.9)
            planning_mode = True
        except pyvisauto.VanishFailed:
            timeout -= 1
        if planning_mode:
            break
    print('Planning mode')


def wait_gnk_splash():
    try:
        r.wait('assets/combat/battle/splash.png', 10, 0.9)
    except pyvisauto.FindFailed:
        print('Missed splash screen')


def path():
    click(loc.cc_1)
    click(loc.scarecrow)
    m1 = r.find('assets/combat/battle/plan-execute.png', 0.8)
    m1.click()


def skip_battle_results():
    r.wait('assets/combat/battle/results.png', 30, 0.9)
    pyautogui.sleep(2)
    for i in range(5):
        click(loc.scarecrow)
    return


def resupply(echelon_location, retries=5):
    found = r.exists('assets/combat/battle/resupply.png', 10, 0.9)
    while not found:
        if retries <= 0:
            break
        # 2 clicks for if they are not selected
        click(echelon_location)
        click(echelon_location)
        retries -= 1
        found = r.exists('assets/combat/battle/resupply.png', 0.9)

    print('Resupply')
    m1 = r.wait('assets/combat/battle/resupply.png', 10, 0.9)
    m1.click()
    r.wait('assets/combat/battle/plan.png', 10, 0.9)


def enter_map():
    m1 = r.wait('ctboxfarm.png', 10, 0.9)
    pyvisauto.sleep(3)
    pyautogui.moveTo(m1.x, m1.y-100)
    pyautogui.click()
    r.wait('ctfarewellscarecrow.png', 5, 0.9)
    m1 = r.find('event_start.png', 0.9)
    m1.click()
    r.wait('assets/combat/battle/plan.png', 10, 0.9)
    pyvisauto.sleep(1)
    print('Entered map')


def run_boxes(runs):
    while runs > 0:
        enter_map()
        deploy(loc.cc_1)
        wait_gnk_splash()
        pyautogui.sleep(2)
        resupply(loc.cc_1)
        planning()
        path()
        pyautogui.sleep(60)
        print('waiting for turn to end')
        skip_battle_results()
        print('run complete')
        runs -= 1


run_boxes(int(input("runs: ")))
