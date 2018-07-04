
import sys
import os
import traceback
import ctypes
from ctypes import wintypes
import win32con
import win32api
import win32gui
import win32process

#
# Used source code posted by CristiFati 
# https://stackoverflow.com/questions/31278590/get-the-title-of-a-window-of-another-program-using-the-process-name
#

title = None

def enumWindowsProc(hwnd, lParam):
    global title
    if (lParam is None) or ((lParam is not None) and (win32process.GetWindowThreadProcessId(hwnd)[1] == lParam)):
        text = win32gui.GetWindowText(hwnd)
        if text:
            wStyle = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
            if wStyle & win32con.WS_VISIBLE:
                #print("%08X - %s" % (hwnd, text))
                title = text

def enumProcWnds(pid=None):
	global title
	win32gui.EnumWindows(enumWindowsProc, pid)
	return title

def enumProcs(procName=None):
    pids = win32process.EnumProcesses()
    if procName is not None:
        bufLen = 0x100
        bytes = wintypes.DWORD(bufLen)
        _OpenProcess = ctypes.cdll.kernel32.OpenProcess
        _GetProcessImageFileName = ctypes.cdll.psapi.GetProcessImageFileNameA
        _CloseHandle = ctypes.cdll.kernel32.CloseHandle
        filteredPids = ()
        for pid in pids:
            try:
                hProc = _OpenProcess(wintypes.DWORD(win32con.PROCESS_ALL_ACCESS), ctypes.c_int(0), wintypes.DWORD(pid))
            except:
                print("Process [%d] couldn't be opened: %s" % (pid, traceback.format_exc()))
                continue
            try:
                buf = ctypes.create_string_buffer(bufLen)
                _GetProcessImageFileName(hProc, ctypes.pointer(buf), ctypes.pointer(bytes))
                if buf.value:
                    name = buf.value.decode().split(os.path.sep)[-1]
                    #print name
                else:
                    _CloseHandle(hProc)
                    continue
            except:
                print("Error getting process name: %s" % traceback.format_exc())
                _CloseHandle(hProc)
                continue
            if name.lower() == procName.lower():
                filteredPids += (pid,)
        return filteredPids
    else:
        return pids
		
def search(procName):
	pids = enumProcs(procName)
	return pids
	
