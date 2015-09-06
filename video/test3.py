#coding=utf-8
import rtorrent


a = rtorrent.RTorrent('http://localhost/RPC2/')
#print a.get_available_rpc_methods()
#print a.get_conn()
#print a.get_rpc_methods()
#131B26AACD0C0FCB4910D4D92664D4F2287CC5E1.torrent

#print a.load_torrent_simple('torrent/1390374C45BCE3349B06BC92E212A7EB0ED06CF1.torrent', 'file', start=True)
#print a.load_torrent_simple('torrent/131B26AACD0C0FCB4910D4D92664D4F2287CC5E1.torrent', 'file', start=True)





#print a.get_directory()
#print a.start()
#print a.start()
l=a.get_torrents()

for i in l:
    i.start()
    print i.get_down_rate()
    print i.get_directory_base()
    print i.get_down_total()
    print i.is_complete()
    print i.info_hash
    #print dir(i)


