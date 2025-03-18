
from multiprocessing import Pool
import time

def coll(n):

    ret=0
    while True:
        time.sleep(0.01)
        if n==1:
            break
        ret=ret+1
        if n % 2 == 0:
            n=n//2
        else:
            n=3*n+1
    return ret

def map_coll(k):

    with Pool(100) as pl:
        zoz=list(range(1,k))
        return list(pl.map(coll,zoz))

print(map_coll(100))
