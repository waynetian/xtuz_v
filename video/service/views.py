from django.shortcuts import render
import urllib
# Create your views here.


from video.settings import TORRENT_URL_PREFIX
from util.btclient import ThreadPool

from django.views.generic import TemplateView


tp = ThreadPool()
#Class T


class DownloadView(TemplateView):
    def get(self, request, hashcode):
        #film = Film.objects.get(hashcode=hashcode)
        url = TORRENT_URL_PREFIX + hashcode
        #'''
        r = urllib.urlopen(url)
        
        torrent_file = 'torrent/%s.torrent' %hashcode
        f = open(torrent_file, 'wb')
        f.write(r.read())
        f.close()
        #''' 
        #torrent_file = 'torrent/test.torrent'
        tp.put_download_task(torrent_file)  
        

      

         
