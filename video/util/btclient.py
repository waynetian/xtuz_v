#coding=utf-8
import logging
import subprocess
import sys
#sys.path.append('..')


logger = logging.getLogger('app')
state_logger = logging.getLogger('state')

#from video import settings
#settings.configure()

#from video.settings import BT_CLIENT

#port = BT_CLIENT['port']

#import libtorrent as l0t
##BT_SESSION = lt.session()
#BT_SESSION.listen_on(port, port+10)

import Queue, time
TASK_QUEUE = Queue.Queue()


import threading
import os

import rtorrent
import socket
socket.setdefaulttimeout(1) 
sgi = rtorrent.RTorrent('http://localhost/RPC2/')


def compress(save_path):
    from service.views import check_format

    for root, dirs, files in os.walk(save_path):  
        for i in files:
            f = os.path.join(root, i)         
            r, n = check_format(f)
            #f = f.replace(' ', '\ ').replace('(', '\(').replace(')', '\)')
            #n = n.replace(' ', '\ ').replace('(', '\(').replace(')', '\)')

            if r:
                cmd = r'ffmpeg -i %s -vf scale=320:-1 -y -c:v libx264  -b:v 100k -b:a 50k %s' %(f, n) 
                #lst = ['ffmpeg', "-i", f, "-vf", "scale=320:-1", "-y", "-c:v", "libx264", "-b:v", "100k", "-b:a", "50k", n]
                print cmd
                try:
                    logger.info(cmd)
                    #p=subprocess.Popen(cmd, shell=True)
                    #ret = p.wait()
                    ret = subprocess.check_call(cmd, shell=True)
                    #import shlex
                    #lst = shlex.split(cmd)
                    #ret = subprocess.check_call(lst, shell=True)
                    logger.info('ffmpeg ret:%s' %ret)
 
                except Exception, e:
                    import traceback
                    ex = traceback.format_exc()
                    logger.error(ex)
                    continue
 

def pool():
    while True:
        logger.info('poll ...')
        l = []
        #'''
        try:
            logger.info('get_torrent begin ...')
            l=sgi.get_torrents()
            logger.info('get_torrent_end ...')
        except:
            import traceback
            ex = traceback.format_exc()
            logger.error(ex)
        
        logger.info('Torrent Info List:')
        info = ''
        for i in l:
            try:
                info = '\r%s %s %s %s %s' %(i.get_state(), i.get_down_rate(), i.get_down_total, i.is_complete(), i.info_hash)
                logger.info(info)

                if i.is_complete() == True:
                    # 1. finish 
                    # 2. compress
                    # 3. rsync
                    logger.info('process finish...%s' %i.info_hash)
                    compress(i.get_directory())
                    from service.models import File
                    f = File()
                    f.hashinfo = i.info_hash
                    f.save()
                    i.erase()
                if i.is_active() == False:
                    i.start()
            except Exception, e:
                import traceback
                ex = traceback.format_exc()
                logger.error(ex)
                continue
        logger.info('Torrent Info List End')
        try:
            logger.info('Compress Queue')
            path = TASK_QUEUE.get_nowait()
            logger.info('get_path %s' %path)
            compress(path)
        except Queue.Empty:
            pass
        except Exception, e:
            import traceback
            ex = traceback.format_exc()
            logger.error(ex)
        #'''
        #state_logger.info(info)
        time.sleep(1)
 


class ThreadPool:
    def __init__(self): 
        self.thread_pool = []
        self.t = threading.Thread(target=pool)
        self.t.setDaemon(True)
        self.t.start()

    def put_download_task(self, torrent_file, hashinfo):
        try:
            sgi.load_torrent_simple(torrent_file, 'file', start=False)
            t = sgi.find_torrent(hashinfo)
            t.set_directory('/home/downloads/%s' %hashinfo[:8])
            t.start()
        except Exception,e:
            import traceback
            ex = traceback.format_exc()
            logger.error(ex)
 



    def retrieve_state(self, hashinfo):
        try:
            t = sgi.find_torrent(hashinfo)
            data = { 
                 'state': t.get_state(),
                 'is_complete': t.is_complete(),
                 'name': t.get_name(),
                 'down_rate':  t.get_down_rate(),
                 'down_total': t.get_down_total(),
                 'ratio': t.get_ratio(),
                 'size_bytes': t.get_size_bytes(),
                }
            return data
        except Exception, e:
            import traceback
            ex = traceback.format_exc()
            logger.error(ex)
            return None 


    def retrieve_all_state(self):
        l=sgi.get_torrents()
        state_list = []
        for t in l:
            try:
                state = {'state': t.get_state(),
                     'is_complete': t.is_complete(),
                     'name': t.get_name(),
                     'down_rate':  t.get_down_rate(),
                     'down_total': t.get_down_total(),
                     'ratio': t.get_ratio(),
                     'size_bytes': t.get_size_bytes(),
                     }
                state_list.append(state)
            except Exception, e:
                import traceback
                ex = traceback.format_exc()
                logger.error(ex)
                continue
        return state_list


    def delete_task(self, hashinfo):
        #while True:
        #    state_logger.info('test')
        #    time.sleep(1) 
        try:
            t = sgi.find_torrent(hashinfo)
            t.erase()
        except Exception, e:
            import traceback
            ex = traceback.format_exc()
            logger.error(ex)
 
    def compress(self, path):
        logger.info('put task %s' %path)
        TASK_QUEUE.put(path)
        #compress(i.get_directory())

if __name__ == '__main__':
    compress('/home/downloads/134467F8/')

 


