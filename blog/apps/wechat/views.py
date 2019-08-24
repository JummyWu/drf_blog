from django.shortcuts import render
import hashlib
import json
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.

@csrf_exempt
def weixin_main(request):
    if request.method == "GET":
        #接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        #服务器配置中的token
        token = '写你的token在这里'
        #把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist])
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
          return HttpResponse(echostr)
        else:
          return HttpResponse("field")
    else:
        # othercontent = autoreply(request)
        return HttpResponse()
