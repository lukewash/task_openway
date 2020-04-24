#
#	Dmitrii Shaporenko, 2020
#   platform linux -- Python 3.6.9, pytest-5.4.1, py-1.8.1, pluggy-0.13.1 -- /usr/bin/python3.6
#   to execute run in console:
#
#   py.test tests.py -v -p
#
import random
import subprocess
import os
from sys import platform
import time

TOOLNAME = "tool_linux_64" if platform.startswith("linux") else "tool_windows_64.exe"
ERRMSG = "Tool expects one int or float argument."
CWD = os.getcwd()
MAXINT = 9223372036854775807  # Golang
MININT = -MAXINT


def run_tool(n, additional=()):
    wordset = [f"{CWD}/{TOOLNAME}", f"{n}"] + list(additional)
    # print("\n" + " ".join(wordset))
    process = subprocess.run(wordset,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    return [process.returncode,
            process.stdout.decode('utf-8').rstrip(),
            process.stderr.decode('utf-8').rstrip()]


# Every test here checks stdout, stderror and tool exit code
# Positive scenarios always come first


#### POSITIVE TESTS ####
def test_p_positive_int():
    assert run_tool("10") == [0, '0.1', '']


def test_p_negative_int():
    assert run_tool("-10") == [0, '-0.1', '']


def test_p_positive_float():
    assert run_tool("1.6") == [0, '0.625', '']


def test_p_negative_float():
    assert run_tool("-1.6") == [0, '-0.625', '']


def test_p_positive_int_zero():
    assert run_tool("0") == [0, '+Inf', '']


def test_p_positive_float_zero():
    assert run_tool("0.0") == [0, '+Inf', '']


# TODO same for floats
def test_p_positive_maxint():
    assert run_tool(str(MAXINT)) == [0, '1.0842021724855044e-19', '']


def test_p_positive_minint():
    assert run_tool(str(MININT)) == [0, '-1.0842021724855044e-19', '']


#### NEGATIVE TESTS ####

def test_n_empty_arg():
    assert run_tool("") == [1, '', ERRMSG]


def test_n_many_args():
    assert run_tool("1", ["2"]) == [1, '', ERRMSG]


def test_n_wrong_arg():
    assert run_tool("abc") == [1, '', ERRMSG]


# Dummy single-thread perf test
def test_100_executions_per_second():
    test_set = []
    for x in range(100):
        test_set.append(random.SystemRandom().randint(MININT, MAXINT))
    start_time = time.time()

    for n in test_set:
        run_tool(n)
    elapsed = time.time() - start_time
    print(f"Performance test took {elapsed} seconds.")
    assert elapsed < 1
