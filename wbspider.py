def login(nick , pwd) :
        print u"----------登录中----------"
        print  "----------......----------"
        prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.15)&_=1400822309846' % nick
        preLogin = getData(prelogin_url)
        servertime = re.findall('"servertime":(.+?),' , preLogin)[0]
        pubkey = re.findall('"pubkey":"(.+?)",' , preLogin)[0]
        rsakv = re.findall('"rsakv":"(.+?)",' , preLogin)[0]
        nonce = re.findall('"nonce":"(.+?)",' , preLogin)[0]
        #print bytearray('xxxx','utf-8')
        su  = base64.b64encode(urllib.quote(nick))
        rsaPublickey= int(pubkey,16)
        key = rsa.PublicKey(rsaPublickey,65537)
        message = str(servertime) +'\t' + str(nonce) + '\n' + str(pwd)
        sp = binascii.b2a_hex(rsa.encrypt(message,key))
        header = {'User-Agent' : 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
        param = {
                'entry': 'weibo',
                'gateway': '1',
                'from': '',
                'savestate': '7',
                'userticket': '1',
                'ssosimplelogin': '1',
                'vsnf': '1',
                'vsnval': '',
                'su': su,
                'service': 'miniblog',
                'servertime': servertime,
                'nonce': nonce,
                'pwencode': 'rsa2',
                'sp': sp,
                'encoding': 'UTF-8',
                'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
                'returntype': 'META',
                'rsakv' : rsakv,
                }
        s = postData('http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)',param,header)
 
        try:
                urll = re.findall("location.replace\(\'(.+?)\'\);" , s)[0]
                login=getData(urll)
                print u"---------登录成功！-------"
                print  "----------......----------"
        except Exception, e:
                print u"---------登录失败！-------"
                print  "----------......----------"
                exit(0)