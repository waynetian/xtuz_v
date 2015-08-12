#coding=utf-8
import logging
logger = logging.getLogger('app')

from video.settings import BT_CLIENT

port = BT_CLIENT['port']

import libtorrent as lt
BT_SESSION = lt.session()
BT_SESSION.listen_on(port, port+10)

import Queue, time
TASK_QUEUE = Queue.Queue()


import threading
def save_bt_file(torrent_file):
    info = lt.torrent_info(torrent_file)
    params = {
        'ti': info, 
        'save_path': 'file/',
        #'storage_mode': lt.storage_mode_t(1),
        'paused': False,
        'auto_managed': True,
        'duplicate_is_error': True}
    h = BT_SESSION.add_torrent(params)
    while (not h.is_seed()):
        s = h.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                     'downloading', 'finished', 'seeding', 'allocating']
        info =  '\r%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s %.s' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                    s.num_peers, state_str[s.state], s.total_download/1000000)
        logger.info("%s" %info)

        time.sleep(2)


def downloader():

    while True:
        logger.info('waiting task ')
        if TASK_QUEUE.empty():
            time.sleep(1)
            continue
        torrent_file = TASK_QUEUE.get()
        logger.info('got task %s' %torrent_file)
        save_bt_file(torrent_file)



class ThreadPool:
    def __init__(self): 
        self.thread_pool = []
        for i in xrange(0, 1):
            t = threading.Thread(target=downloader)
            t.setDaemon(True)
            self.thread_pool.append(t)
            t.start()

    def put_download_task(self, torrent_file):
        print 'recv-file', torrent_file 
        TASK_QUEUE.put(torrent_file)
