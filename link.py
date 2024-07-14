import ctypes as ct
import os

path = os.getcwd()
lib = ct.CDLL(os.path.join(path, 'htmlparser.so'))

def html_parse():
    pathin = ct.c_char_p(b"tmp/index.html")
    pathout = ct.c_char_p(b"tmp/index_parsed.html")
    N_BUFFER = ct.c_int(400)
    
    lib.init_htmlparse.argtypes = [ct.c_char_p, ct.c_char_p, ct.c_int]
    lib.init_htmlparse.restype = ct.c_int
    result = lib.init_htmlparse(pathin, pathout, N_BUFFER)
    if result != 0:
        print("Parsing done. Sucess!")
    else:
        raise ValueError("Some error occurred.")