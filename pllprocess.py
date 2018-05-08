from multiprocessing import Process
import time

strt=time.time()
t=10

def f(name):
	for name in a:
		print ('hello', name)
def g(name):
	print ('hello', name)

if __name__ == '__main__':
	a=["Gaurav","Yukti","Mahima","Gungun","Ranjana"]
	p = Process(target=f, args=('name',))
	p.start()
	p.join()

print (time.time()-strt)

strt=time.time()

for i in range(5):
	g(a[i])

print (time.time()-strt)