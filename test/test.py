import ctypes

lib = ctypes.cdll.LoadLibrary("./hello.dll")
lib.hello_world()
