#coding=utf-8
import logging
import subprocess
logger = logging.getLogger('app')
state_logger = logging.getLogger('state')



from video.settings import BT_CLIENT

port = BT_CLIENT['port']

#import libtorrent as l0t
##BT_SESSION = lt.session()
#BT_SESSION.listen_on(port, port+10)

import Queue, time
TASK_QUEUE = Queue.Queue()


import threading
import os

import rtorrent
sgi = rtorrent.RTorrent('http://localhost/RPC2/')


def compress(save_path):
    from service.views import check_format

    for root, dirs, files in os.walk(save_path):  
        for i in files:
            f = os.path.join(root, i)         
            r, n = check_format(f)
            if r:
                cmd = 'ffmpeg -i %s -vf scale=320:-1 -y -c:v libx264  -b:v 100k -b:a 50k %s' %(f, n) 
                print cmd
                try:
                    logger.info(%cmd)
                    p=subprocess.Popen(cmd, shell=True)
                    ret = p.wait()
                except Exception, e:
                    import traceback
                    ex = traceback.format_exc()
                    logger.error(ex)
                    continue
 

def pool():
    while True:
        l=sgi.get_torrents()
        info = ''
        for i in l:
            try:
                info += '\r%s %s %s %s %s' %(i.get_state(), i.get_down_rate(), i.get_down_total, i.is_complete(), i.info_hash)
                if i.is_complete() == True:
                    # 1. finish 
                    # 2. compress
                    # 3. rsync
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
        state_logger.info(info)
        time.sleep(5)
 


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
                 'size_bytes', t.get_size_bytes(),
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
                     'size_bytes', t.get_size_bytes(),
                     }
                state_list.append(state)
            except Exception, e:
                import traceback
                ex = traceback.format_exc()
                logger.error(ex)
                continue
        return state_list


    def delete_task(self, hashinfo):
        try:
            t = sgi.find_torrent(hashinfo)
            t.erase()
        except Exception, e:
            import traceback
            ex = traceback.format_exc()
            logger.error(ex)
 


if __name__ == '__main__':
    compress()

 


