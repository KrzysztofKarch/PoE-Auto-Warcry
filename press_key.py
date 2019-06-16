from pynput.keyboard import Key, Controller
import time, random

def press_key(key:str = 'r', delay:float = 3.43) -> None:
    """
    Automatic key pressing after a fixed delay.

    Function will add some little random delay and works
    with 3 different scenarios to imitate real human.

    Created for Path of Exile instant warcies.
    Default setting for 20% increased Warcry Cooldown Recovery Speed.

    Parameters:
    key : string
          keyboard key you want to press

    delay : float
            delay in seconds, you can take value from tooltip in game
            and add 0.1 to time displayed in tooltip in game, otherwise
            you'll be missing some warcies due to latency in connection

    Typical run:
    - - time
    X - working click
    f - fake click during cooldown
    ----------X----------X-f--------X------f-f-X----------X
    """

    keyboard = Controller()
    # additional, random delay 1-30 ms
    additional_delay = random.randrange(1, 31)
    additional_delay /= 1000

    scenario = random.random()
    # 50% chance for 1 click
    # this scenario also 'reset' time for other scenarios,
    # when you switch to game, so it should has high chance
    # time stamps:
    # ----------X
    if scenario < 0.5:
        time.sleep(delay + additional_delay)
        keyboard.press(key)
        keyboard.release(key)

    # 25% chance for fake delayed additional click
    # time stamps:
    # -x--------X
    elif scenario < 0.75:
        fake_delay = random.randrange(200, 301)
        fake_delay /= 1000
        time.sleep(fake_delay)
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(delay + additional_delay - fake_delay)
        keyboard.press(key)
        keyboard.release(key)

    # 25% chance for panic clicking
    # note that people can click max 5-7 times a second
    # so time between them is set to 140-240 ms
    # time stamps:
    # ------x-x-X
    else:
        fake_delay = random.randrange(180, 241)
        fake_delay /= 1000
        time.sleep(delay - fake_delay * 2)
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(fake_delay)
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(fake_delay + additional_delay)
        keyboard.press(key)
        keyboard.release(key)

if __name__ == '__main__':
    print('This is module file for program PoE Auto Warcry. \n\n'
        + 'Designed to import. Do not run this program alone.')
    input()
