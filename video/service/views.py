#coding=utf-8
import json
from django.shortcuts import render
import urllib
# Create your views here.
from .models import *

from video.settings import TORRENT_URL_PREFIX
from util.btclient import ThreadPool
from django.http import HttpResponse

from django.views.generic import TemplateView
tp = ThreadPool()

import libtorrent as lt

def check_format(name):
    vedio_format = ('.mp4', '.avi', '.mov', '.3gp', '.wmv', '.mkv', '.flv')
    import os
    f, ext = os.path.splitext(name)
    if ext.lower() in vedio_format:
        return (True, f+'.wt.mp4')
    return (False, None)




class CreateView(TemplateView):
    def get(self, request, hashinfo):
        #film = Film.objects.get(hashcode=hashcode)
        url = TORRENT_URL_PREFIX + hashinfo
        #'''
        r = urllib.urlopen(url)
        
        torrent_file = 'torrent/%s.torrent' %hashinfo
        f = open(torrent_file, 'wb')
        f.write(r.read())
        f.close()
        #''' 
        #torrent_file = 'torrent/test.torrent'
        tp.put_download_task(torrent_file, hashinfo)  
        return HttpResponse('ok')
       


class RetrieveView(TemplateView):
    def get(self, request, hashinfo):
        ret = tp.retrieve_state(hashinfo)  
        return HttpResponse(json.dumps({'ret':ret}))


class RetrieveAllView(TemplateView):
    def get(self, request):
        ret = tp.retrieve_all_state()  
        return HttpResponse(json.dumps({'ret':ret}))
      

class DeleteView(TemplateView):
    def get(self, request, hashinfo):
        tp.delete_task(hashinfo)  
        return HttpResponse('ok')

class CompressView(TemplateView):
    def get(self, request):
        path = request.GET.get('path', None)
        tp.compress(path)  
        return HttpResponse('ok')



 
from django.core.exceptions import ObjectDoesNotExist
class QueryView(TemplateView):
    def get(self, request, hashinfo):
        try:
            o = File.objects.get(hashinfo=hashinfo) 
         
            torrent_file = 'torrent/%s.torrent' %hashinfo

            torinfo = lt.torrent_info(torrent_file)

            ret = []
            file_list = torinfo.files()
            for i in file_list:
                r, name = check_format(i.path) 
                if r:
                    ret.append('/mp4/%s/%s' %(torrent_file[8:16], name)) 
            return HttpResponse(json.dumps({'ret': ret, 'code':200}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'ret': None, 'code':400}))
        



         
