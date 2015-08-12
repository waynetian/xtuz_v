# -*- coding:utf8 -*- 
import logging
from django.http import HttpResponse
import traceback
import json

class ExceptionMiddleware(object):

    def process_exception(self, request, exception):
        logger = logging.getLogger('app')
        ex = traceback.format_exc()
        logger.info('status:500 ' + request.path + '\r\n' + ex)
        info = json.dumps({'info': str(exception)})
        return HttpResponse(info, status=500)    
