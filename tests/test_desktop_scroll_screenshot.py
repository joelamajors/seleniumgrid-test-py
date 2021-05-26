import os
import pytest
from pylenium.driver import Pylenium


base_url = 'https://ntg.hatfield.marketing'

# def test_desktop_scroll_screenshot(py):
#     py.visit(base_url)
#     py.find('.footer-hatfield-links')

#     window_height = py.window_size['height']

#     scroll_length = window_height

    # py.scroll_to(0, scroll_length)

    # py.screenshot()


def test_screen_height(py: Pylenium):
    py.visit(base_url)
    file = open('ntg_test', 'w+')
    window_height = py.window_size['height']
    file.write(str(window_height))

