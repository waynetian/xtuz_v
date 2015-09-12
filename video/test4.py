#coding=utf-8


a = 'a b c'

#print a.decode('utf8', 'escape')


import subprocess


#lst = ['ffmpeg', "-i", f, "-vf", "scale=320:-1", "-y", "-c:v", "libx264", "-b:v", "100k", "-b:a", "50k", n]


import shlex
test = r'ls -lh a\ b.txt'
lst = shlex.split(test)
print lst
lst = ['ls', '-l',r'a b.txt']
#p=subprocess.Popen(test, shell=True)

p=subprocess.Popen(lst, shell=True)
ret = p.wait()
 
#ret = subprocess.check_call(lst, shell=True)
print ret

