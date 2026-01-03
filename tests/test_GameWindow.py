import pytest

from pygame import Rect
from src.screens.game_window import GameWindow

def test_calculate_bounce_angle():
    paddlerect = Rect(0,0,100,1)
    ballrect = Rect(0,0,1,1)
    speed = 5
    hardleft = GameWindow.calculate_bounce_angle(None,paddlerect,ballrect,speed)

    ballrect = Rect(99,0,1,1)
    hardright = GameWindow.calculate_bounce_angle(None,paddlerect,ballrect,speed)

    ballrect = Rect(50,0,1,1)
    up = GameWindow.calculate_bounce_angle(None,paddlerect,ballrect,speed)

    print(hardleft)
    print(hardright)
    print(up)

    assert up[0].approx(5)
    assert 1==2