import os,sys
import threading

import pytest

sys.path.append(os.getcwd())

from scripts.qg.crontask import login_device

def test_login_device():
    login_device()
    pass


if __name__ == "__main__":
    pytest.main(["-s", "scripts\qg\crontask_test.py"])