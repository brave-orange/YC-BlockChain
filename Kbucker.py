import random,hashlib
import heapq  #堆
class Kbucket(object):
    def __init__(self):
        self.Kbuck = []

def digest(string):
    if not isinstance(string, bytes):
        string = str(string).encode('utf8')
    return hashlib.sha1(string).digest()
#print (int(digest(random.getrandbits(255)).hex(),16))
list = []
heapq.heappush(list,156)
heapq.heappush(list,986)
heapq.heappush(list,765)
heapq.heappush(list,13)#堆排序
print(list)
a = map(digest,[1,2,3])
for i in a:
    print(2**160)

