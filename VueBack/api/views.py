from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import requests,json,time,datetime,math,re,telnetlib,asyncio,subprocess,random
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from django.shortcuts import render
from django.http import FileResponse
from .models import Info,Devices,Contacts
from django.db.models import Q
# Create your views here.
xlat = [0x64, 0x73, 0x66, 0x64, 0x3b, 0x6b, 0x66, 0x6f, 0x41, 0x2c, 0x2e, 0x69, 0x79, 0x65, 0x77, 0x72, 0x6b, 0x6c, 0x64
, 0x4a, 0x4b, 0x44, 0x48, 0x53, 0x55, 0x42, 0x73, 0x67, 0x76, 0x63, 0x61, 0x36, 0x39, 0x38, 0x33, 0x34, 0x6e, 0x63,
0x78, 0x76, 0x39, 0x38, 0x37, 0x33, 0x32, 0x35, 0x34, 0x6b, 0x3b, 0x66, 0x67, 0x38, 0x37]


def time12to24(time_string, formats="%m/%d/%Y %H:%M:%S %p"):
    times = time.strftime("%Y/%m/%d %H:%M:%S", time.strptime(time_string, formats))  # 将时间转为hh.mm类型
    timehhmm = time.strftime("%H.%M", time.strptime(time_string, "%m/%d/%Y %H:%M:%S %p"))  # 将时间转为hh.mm类型
    ftime = datetime.datetime.strptime(times, "%Y/%m/%d %H:%M:%S")  # 将times字符串转为%H.%M的datetime类型
    if time_string.find("AM") > -1:
        if timehhmm >= '12.00':
            ftime = ftime + datetime.timedelta(hours=-12)  # +36小时而不是-12小时的原因：如果未提供年份，则默认为1900，如果-12小时，年份有可能为1899，会异常
    elif time_string.find("PM") > -1:
        if timehhmm < '12.00':
            ftime = ftime + datetime.timedelta(hours=12)
    return ftime


@require_POST
def getHistoryFromPRTG(request):
    """封装一个函数取PRTG的historicdata"""
    request_data=json.loads(request.body)
    customTable = {"0":["Zoe_Shen","3346723892"], "1":["Dashboard_MTL","812086805"]}
    # dataTypeTb = {"1":"RTT", "2":"Traffic"}
    # dataType = dataTypeTb.get(request_data.get("type"))
    sdate = request_data.get("sdate")
    edate = request_data.get("edate")
    custom = request_data.get('custom')
    idDict = request_data.get("idDict")          #传进[{"name":"香港","id":"5235"},]等
    username= customTable.get(custom,"0")[0]
    password = customTable.get(custom,"0")[1]
    data = {}
    for i in idDict:
        data_test = []
        name = i['name']
        url = 'http://10.68.253.13/api/historicdata.json?username=%s&passhash=%s&id=%s&sdate=%s&edate=%s&avg=0&pctshow=false&pctmode=false&usecaption=1'%(username,password,i["id"],sdate,edate)
        # print(url)
        response = requests.get(url).json()['histdata']
        # if not data:
        for j in response:
            tiMe = time12to24(j['datetime'])   # 12小时时间制转换为24小时制
            newObj = [tiMe, j['Avg. Round Trip Time (RTT)']]
            data_test.append(newObj)
        if name:
            data[name] = data_test
    return JsonResponse({"code":0, "data":data})


@require_POST
def getHistory_speed_FromPRTG(request):
    """封装一个函数取PRTG的historicdata"""
    request_data=json.loads(request.body)
    customTable = {"0":["Zoe_Shen","3346723892"], "1":["Dashboard_MTL","812086805"]}
    # dataTypeTb = {"1":"RTT", "2":"Traffic"}
    # dataType = dataTypeTb.get(request_data.get("type"))
    sdate = request_data.get("sdate")
    edate = request_data.get("edate")
    custom = request_data.get('custom')
    idDict = request_data.get("idDict")          #传进[{"name":"香港","id":"5235"},]等
    username= customTable.get(custom,"0")[0]
    password = customTable.get(custom,"0")[1]
    data = {}
    for i in idDict:
        data_in = []
        data_out = []
        name = i['name']
        url = 'http://10.68.253.13/api/historicdata.json?username=%s&passhash=%s&id=%s&sdate=%s&edate=%s&avg=0&pctshow=false&pctmode=false&usecaption=1'%(username,password,i["id"],sdate,edate)
        # print(url)
        response = requests.get(url).json()['histdata']
        # if not data:
        for j in response:
            tiMe = time12to24(j['datetime'])  # 12小时时间制转换为24小时制
            Traffic_in = math.ceil(j['Traffic In (speed)'] / 125)
            Traffic_out = math.ceil(j['Traffic Out (speed)'] / 125)
            Tra_in = [tiMe, Traffic_in]
            Tra_out = [tiMe, Traffic_out]
            data_in.append(Tra_in)
            data_out.append((Tra_out))
        if name:
            data[name + "-" + "In"] = data_in
            data[name + "-" + "Out"] = data_out
    return JsonResponse({"code":0, "data":data})


@require_POST
def getNow_data_fromPRTG(request):#获取prtg线路in或out占比
    """封装一个函数取PRTG的historicdata"""
    request_data=json.loads(request.body)
    customTable = {"0":["Zoe_Shen","3346723892"], "1":["Dashboard_MTL","812086805"]}
    sdate = request_data.get("sdate")
    edate = request_data.get("edate")
    custom = request_data.get('custom')
    idDict = request_data.get("idDict")          #传进[{"name":"香港","id":"5235"},]等
    username= customTable.get(custom,"0")[0]
    password = customTable.get(custom,"0")[1]
    data = {}
    for i in idDict:
        url_data = 'http://10.68.253.13/api/historicdata.json?username=%s&passhash=%s&id=%s&sdate=%s&edate=%s&avg=0&pctshow=false&pctmode=false&usecaption=1'%(username,password,i["id"],sdate,edate)
        response = requests.get(url_data).json()['histdata']
        url_name = 'http://10.68.253.13/api/getsensordetails.json?username=Jace_Mo&passhash=3188079540&id=%s'%(i['id'])
        response_name = requests.get(url_name).json()['sensordata']['name']
        if re.search(r'\d+M',response_name):
            Bandwidth = int(re.search(r'\d+M',response_name).group()[:-1])*1000
        In = int(response[-1]['Traffic In (speed)'])
        Out = int(response[-1]['Traffic Out (speed)'])
        proportion = str(math.ceil(round(max(In,Out)/1000)/Bandwidth*100)) + "%"
        data[response_name] = proportion

    return JsonResponse({"code":0, "data":data})


@require_GET
def getMTLvpnUser(request):
    url = 'http://172.22.254.12:8086/query?q=SELECT%20*%20FROM%20%22MTLVPNUsers%22%20WHERE%20time%20%3E=%20now()%20-%205m%20and%20%22status%22=%27Online%27%20and%20%22device%22=%27MTGZ-IDC-FW5512-VPN%27&db=WTC_DB'
    All_list = requests.get(url).json()['results'][0]['series'][0]['values']
    data = []
    for i in All_list:
        someOne = {
            "time": None,
            "device": None,
            'name': None,
            "status": None
        }
        tiem1 = i[0]
        time2 = tiem1[0:19]+tiem1[-1:]
        date_ = datetime.datetime.strptime(time2, "%Y-%m-%dT%H:%M:%SZ")
        local_time = date_ + datetime.timedelta(hours=8)
        del i[1]
        someOne['time'] = str(local_time)
        someOne['device'] = i[1]
        someOne['name'] = i[2]
        someOne['status'] = i[3]
        data.append(someOne)

    return JsonResponse({"code":0, "data":data})


def SankeyToJsonFromUrl(url):
    data={}
    response = requests.get(url).content.decode()
    response = response.split("\r\n")
    print(response)
    soIndex = 2
    nodes = []
    links = []
    deIndex = 4
    BytesIndex = 7
    perIndex = 9

    for row in response[1:30]:
        rowList = row.split(',"')
        sourceIp = rowList[soIndex].replace('"', '').replace('[', '').replace(']', '')
        destinIp = rowList[deIndex].replace('"', '').replace('[', '').replace(']', '')
        Bytes = int(rowList[perIndex].replace('"', ''))
        nodesList = set([key["name"] for key in nodes])
        # print(Bytes)
        # Bytes = int(Bytes / 1024 / 1024)
        # print(nodesList)
        if sourceIp == "":
            # nodes.append({"name": 'Other'})
            # nodes.append({"name": '其他'})
            # links.append({"source": 'Other', "target": '其他', "value": Bytes})
            continue
        if sourceIp not in nodesList:
            # print(sourceIp)
            nodes.append({"name": sourceIp, "value":Bytes})
        if destinIp not in nodesList:
            nodes.append({"name": destinIp, "value":Bytes})
        links.append({"source": sourceIp, "target": destinIp, "value": Bytes})
    data["nodes"] = nodes
    # print("clear",links)
    data["links"] = links
    return data


@require_GET
def getSankeyFromUrl(request):
    data={}
    try:
        url = "http://10.68.253.13/api/table.csv?&content=topdata&columns=position%2Cvalue_%2Cminigraph%2Cobjid%2Cbaselink&sortby=-value_2V&display=extendedheaders&subid=1&topnumber=-1&id=53718&username=Jace_Mo&passhash=3188079540"
        data["NetFlow"] = SankeyToJsonFromUrl(url)
    except Exception as e:
        print(e)
    return JsonResponse({"code":0, "data":data})


@require_POST
def Cisco_data(request):
    start = time.time()
    request_data = json.loads(request.body)
    stores = request_data.get("stores")
    if '.' in stores:
        Stores = Devices.objects.filter(router_ip=stores)
    else:
        Stores = Devices.objects.filter(storeno=stores)
    if Stores :
        for i in Stores:
            if re.search(r'\d+.\d+.\d+.\d+',i.router_ip):
                result = do_telnet(re.search(r'\d+.\d+.\d+.\d+',i.router_ip).group())
        print('运行时间 {}'.format(time.time()-start))
        # return JsonResponse({"code": 0, "message": result})
        return result
    else:
        return JsonResponse({"code": 2, "message": '未查询到该店铺'})


def do_telnet(Host):#telnet店铺函数
    try:
        comman = 'ping -c 4 -s 1000 {}'.format(Host)
        p = subprocess.Popen(
            [comman],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        out = p.stdout.read().decode('utf8')
        if re.search(r'/\d+.\d+/', out):
            vns = re.search(r'/(\d+).\d+/', out).group().strip('/')
            if int(re.search(r'\d+', vns).group()) > 200:
                return JsonResponse({"code": 2, "message": '网络延迟过高或断网'})
                # return '网络延迟过高或断网'

            else:
                global response
                response = []

                try:
                    tn = telnetlib.Telnet(Host, port=23, timeout=5)
                    print('CISCO延迟正常')
                    tn.set_debuglevel(0)
                    tn.write(b'mtlops' + b'\n')
                    tn.write(b'online' + b'\n')
                    host_end = re.search(r'\d+$', Host).group()
                    host_head = re.search(r'\d+.\d+.\d+.', Host).group()
                    g, h, j = tn.expect([], timeout=3)
                    tn.write(b'en' + b'\n')
                    if re.search(r'ASW.+\d+', str(j, encoding='utf8')):
                        sds = bytes(re.search(r'ASW.+\d+', str(j, encoding='utf8')).group() + '1223',encoding='utf8')
                    else:
                        sds = bytes(re.search(r'[A-Z]+-[A-Z]+-\d+', str(j, encoding='utf8')).group() + '1223',encoding='utf8')
                    tn.write(sds + b'\n')
                    #loop = asyncio.get_event_loop()  # 创建一个循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    dns_check = loop.create_task(Dns_check(tn=tn, host=Host))
                    dhcp_check = loop.create_task(DHCP_check(tn=tn))
                    vlan_check = loop.create_task(VLAN_check(tn=tn))
                    pwd_check = loop.create_task(PWD_check(tn=tn))
                    pc01 = loop.create_task(PC01_check(Host=Host, host_end=host_end, host_head=host_head))
                    pc02 = loop.create_task(PC02_check(Host=Host, host_end=host_end, host_head=host_head))
                    ap01 = loop.create_task(AP01_check(Host=Host, host_end=host_end, host_head=host_head))
                    ap02 = loop.create_task(AP02_check(Host=Host, host_end=host_end, host_head=host_head))
                    ap03 = loop.create_task(AP03_check(Host=Host, host_end=host_end, host_head=host_head))
                    ap04 = loop.create_task(AP04_check(Host=Host, host_end=host_end, host_head=host_head))
                    tasks = [
                        ap01,
                        ap02,
                        ap03,
                        ap04,
                        pc01,
                        pc02,
                        vlan_check,
                        dns_check,
                        dhcp_check,
                        pwd_check,

                    ]
                    loop.run_until_complete(asyncio.wait(tasks))
                    loop.close()
                    tn.close()


                except:
                    host_end = re.search(r'\d+$', Host).group()
                    host_head = re.search(r'\d+.\d+.\d+.', Host).group()
                    tn = telnetlib.Telnet(host_head+str(int(host_end)+36), port=23, timeout=5)
                    print('SDWAN延迟正常')
                    tn.set_debuglevel(0)
                    tn.write(b'mtlops' + b'\n')
                    tn.write(b'online' + b'\n')
                    g, h, j = tn.expect([], timeout=3)
                    tn.write(b'en' + b'\n')
                    if re.search(r'ASW.+\d+', str(j, encoding='utf8')):
                        sds = bytes(re.search(r'ASW.+\d+', str(j, encoding='utf8')).group() + '1223',encoding='utf8')
                    else:
                        sds = bytes(re.search(r'[A-Z]+-[A-Z]+-\d+', str(j, encoding='utf8')).group() + '1223',encoding='utf8')
                    tn.write(sds + b'\n')
                    # loop = asyncio.get_event_loop()  # 创建一个循环
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    dns_check = loop.create_task(Dns_check(tn=tn, host=Host))
                    dhcp_check = loop.create_task(DHCP_check(tn=tn))
                    vlan_check = loop.create_task(VLAN_check(tn=tn))
                    #pwd_check = loop.create_task(PWD_check(tn=tn))
                    pc01 = loop.create_task(PC01_check(Host=host_head+str(int(host_end)+36), host_end=host_end, host_head=host_head))
                    pc02 = loop.create_task(PC02_check(Host=host_head+str(int(host_end)+36), host_end=host_end, host_head=host_head))
                    ap01 = loop.create_task(AP01_check(Host=host_head+str(int(host_end)+36), host_end=host_end, host_head=host_head))
                    ap02 = loop.create_task(AP02_check(Host=host_head+str(int(host_end)+36), host_end=host_end, host_head=host_head))
                    ap03 = loop.create_task(AP03_check(Host=host_head+str(int(host_end)+36), host_end=host_end, host_head=host_head))
                    ap04 = loop.create_task(AP04_check(Host=host_head+str(int(host_end)+36), host_end=host_end, host_head=host_head))
                    tasks = [
                        ap01,
                        ap02,
                        ap03,
                        ap04,
                        pc01,
                        pc02,
                        vlan_check,
                        dns_check,
                        dhcp_check,
                        #pwd_check,
                    ]
                    loop.run_until_complete(asyncio.wait(tasks))
                    loop.close()
                    tn.close()

                finally:
                    return JsonResponse({"code":0,"data":response})
                    # return HttpResponse(responsee)

        else:
            return JsonResponse({"code": 2, "message": '店铺断网'})
            # return  '店铺断网'
    except Exception as e:
    # except:
        return JsonResponse({"code": 2, "message": 'Ping店铺异常'})
        # return 'Ping店铺异常'


async def AP01_check(Host,host_end, host_head):#异步函数检查AP01在线情况
    start = time.time()
    print('开始执行ap01')
    data = {
        "label":None,
        "value":None
    }
    ap = 'ping {}'.format(host_head + str(int(host_end) + 55))
    tn = telnetlib.Telnet(Host, port=23, timeout=5)
    tn.write(b'mtlops' + b'\n')
    tn.write(b'online' + b'\n')
    tn.write(bytes(ap, encoding='utf8') + b'\n')
    await asyncio.sleep(8)
    g, h, j = tn.expect([], timeout=1)
    tn.close()
    if re.search(r'(4/5)', str(j, encoding='utf8')) or re.search(r'(5/5)', str(j, encoding='utf8')):
        data['label'] = 'AP01在线'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap01 {}'.format(time.time() - start))
        response.append(data)
        return response
    else:
        data['label'] = 'AP01不在线或延迟高'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap01 {}'.format(time.time() - start))
        response.append(data)
        return response


async def AP02_check(Host, host_end, host_head):#异步函数检查AP02在线情况
    start = time.time()
    print('开始执行ap02')
    data = {
        "label": None,
        "value": None
    }
    ap = 'ping {}'.format(host_head + str(int(host_end) + 56))
    tn = telnetlib.Telnet(Host, port=23, timeout=5)
    tn.write(b'mtlops' + b'\n')
    tn.write(b'online' + b'\n')
    tn.write(bytes(ap, encoding='utf8') + b'\n')
    await asyncio.sleep(8)
    g, h, j = tn.expect([], timeout=1)
    tn.close()
    if re.search(r'(4/5)', str(j, encoding='utf8')) or re.search(r'(5/5)', str(j, encoding='utf8')):
        data['label'] = 'AP02在线'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap02 {}'.format(time.time() - start))
        response.append(data)
        return response
    else:
        data['label'] = 'AP02不在线或延迟高'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap02 {}'.format(time.time() - start))
        response.append(data)
        return response


async def AP03_check(Host, host_end, host_head):#异步函数检查AP03在线情况
    start = time.time()
    print('开始执行ap03')
    data = {
        "label": None,
        "value": None
    }
    ap = 'ping {}'.format(host_head + str(int(host_end) + 32))
    tn = telnetlib.Telnet(Host, port=23, timeout=5)
    tn.write(b'mtlops' + b'\n')
    tn.write(b'online' + b'\n')
    tn.write(bytes(ap, encoding='utf8') + b'\n')
    await  asyncio.sleep(8)
    g, h, j = tn.expect([], timeout=1)
    tn.close()
    if re.search(r'(4/5)', str(j, encoding='utf8')) or re.search(r'(5/5)', str(j, encoding='utf8')):
        data['label'] = 'AP03在线'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap03 {}'.format(time.time() - start))
        response.append(data)
        return response
    else:
        data['label'] = 'AP03不在线或延迟高'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap03 {}'.format(time.time() - start))
        response.append(data)
        return response


async def AP04_check(Host, host_end, host_head):#异步函数检查AP04在线情况
    start = time.time()
    print('开始执行ap04')
    data = {
        "label": None,
        "value": None
    }
    ap = 'ping {}'.format(host_head + str(int(host_end) + 33))
    tn = telnetlib.Telnet(Host, port=23, timeout=5)
    tn.write(b'mtlops' + b'\n')
    tn.write(b'online' + b'\n')
    tn.write(bytes(ap, encoding='utf8') + b'\n')
    await asyncio.sleep(8)
    g, h, j = tn.expect([], timeout=1)
    tn.close()
    if re.search(r'(4/5)', str(j, encoding='utf8')) or re.search(r'(5/5)', str(j, encoding='utf8')):
        data['label'] = 'AP04在线'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap04 {}'.format(time.time() - start))
        response.append(data)
        return response
    else:
        data['label'] = 'AP04不在线或延迟高'
        data['value'] = str(j, encoding='utf8')
        print('执行完ap04 {}'.format(time.time() - start))
        response.append(data)
        return response


async def PC01_check(Host, host_end, host_head):#异步函数检查pc01在线情况
    start = time.time()
    print('开始执行pc01')
    data = {
        "label": None,
        "value": None
    }
    pc = 'ping {}'.format(host_head + str(int(host_end) + 1))
    tn = telnetlib.Telnet(Host, port=23, timeout=5)
    tn.write(b'mtlops' + b'\n')
    tn.write(b'online' + b'\n')
    tn.write(bytes(pc, encoding='utf8') + b'\n')
    await asyncio.sleep(8)
    g, h, j = tn.expect([], timeout=1)
    tn.close()
    if re.search(r'(4/5)', str(j, encoding='utf8')) or re.search(r'(5/5)', str(j, encoding='utf8')):
        data['label'] = 'PC01在线'
        data['value'] = str(j, encoding='utf8')
        print('执行完pc01 {}'.format(time.time() - start))
        response.append(data)
        return response
    else:
        data['label'] = 'PC01不在线或延迟高'
        data['value'] = str(j, encoding='utf8')
        print('执行完pc01 {}'.format(time.time() - start))
        response.append(data)
        return response


async def PC02_check(Host, host_end, host_head):#异步函数检查pc02在线情况
    start = time.time()
    print('开始执行pc02')
    data = {
        "label": None,
        "value": None
    }
    pc = 'ping {}'.format(host_head + str(int(host_end) + 18))
    tn = telnetlib.Telnet(Host, port=23, timeout=5)
    tn.write(b'mtlops' + b'\n')
    tn.write(b'online' + b'\n')
    tn.write(bytes(pc, encoding='utf8') + b'\n')
    await asyncio.sleep(8)
    g, h, j = tn.expect([], timeout=1)
    tn.close()
    if re.search(r'(4/5)', str(j, encoding='utf8')) or re.search(r'(5/5)', str(j, encoding='utf8')):
        data['label'] = 'PC02在线'
        data['value'] = str(j, encoding='utf8')
        print('执行完pc02 {}'.format(time.time() - start))
        response.append(data)
        return response
    else:
        data['label'] = 'PC02不在线或延迟高'
        data['value'] = str(j, encoding='utf8')
        print('执行完pc02 {}'.format(time.time() - start))
        response.append(data)
        return response


async def Dns_check(tn, host):#异步函数检查DNS配置
    start = time.time()
    data = {
        "label":"DNS",
        "value":None
    }
    host_end = re.search(r'\d+$', host).group()
    data2 = {
        'dns': 'ip dns server error',
        'dns_analysis': 'ip host mfs1 error',
        'dns_domain': 'ip domain error',
        'mfs1': 'ping mfs1 error'
    }
    overview = {'status': None, 'data': None}
    commands = ['show run | se ip dns', 'show run | se ip host', 'show run | se domain name','ping mfs1']
    for command in commands:
        tn.write(bytes(command, encoding='utf8') + b'\n')
        time.sleep(1)
    result = tn.read_very_eager().decode()
    if re.search(r'ip dns server', result):
        data2['dns'] = 'ip dns server OK'
    if re.search(r'ip host.+{}'.format(re.search(r'\d+.\d+.\d+.', host).group() + str(int(host_end) + 1)), result):
        data2['dns_analysis'] = 'ip host mfs1 OK'
    if re.search(r'ip domain.+net', result):
        data2['dns_domain'] = 'ip domain OK'
    if re.search(r'(\d+/\d+)', result):
        data2['mfs1'] = 'ping mfs1 OK'
    Err = 4
    for i in data2:
        if 'OK' in data2[i]:
            Err -= 1
    overview['status'] = '{} Error'.format(Err)
    overview['data'] = data2
    data['value'] = overview
    response.append(data)
    print('执行了Dns {}'.format(time.time() - start))
    return response


async def DHCP_check(tn):#异步函数检查DHCP配置
    start = time.time()
    data = {
        "label": "DHCP",
        "value": None
    }
    overview = {'status': None, 'data': None}
    data2 = {
        'dhcp_pool': 'dhcp_pool OK',
        'address_out': 'address_out OK',
        'dhcp_dns': 'dhcp_dns OK'
    }

    commands = ['show run | se dhcp', 'show ip dhcp pool']
    for command in commands:
        tn.write(bytes(command, encoding='utf8') + b'\n')
        # await asyncio.sleep(0.5)
        time.sleep(1)
    result = tn.read_very_eager().decode()
    if len(re.findall(r'ip dhcp excluded-address \d+.\d+.\d+.\d+ \d+.\d+.\d+.\d+', result,re.S)) < 2:
        data2['address_out'] = 'address_out error'
    if len(re.findall(r'dns-server.+', result)) < 4:
        data2['dhcp_dns'] = 'dhcp_dns error'
    for i in re.findall('Leased addresses\r\n(.*?)\r\n', result, re.S):
        if re.search(r'\d+.\d+.\d+.\d+', i).group() == '0.0.0.0':
            data2['dhcp_pool'] = 'dhcp_pool error'
            break
    Err = 3
    for i in data2:
        if 'OK' in data2[i]:
            Err -= 1
    overview['status'] = '{} Error'.format(Err)
    overview['data'] = data2
    data['value'] = overview
    response.append(data)
    print('执行了dhcp {}'.format(time.time() - start))
    return response


async def VLAN_check(tn):#异步函数检查VLAN配置
    start = time.time()
    data = {
        "label":"VLAN",
        "value":None
    }
    data2 = {}
    commands = ['show run int vlan 1', 'show run int vlan 20', 'show run int vlan 30', ]
    for command in commands:
        tn.write(bytes(command, encoding='utf8') + b'\n')
        time.sleep(1)
    result = str()
    for i in re.findall(r'!(.*?)end', tn.read_very_eager().decode(), re.S): result += i
    data2['vlan'] = result
    tn.write(b'show ip int brief' + b'\n')
    time.sleep(1)
    result1 = tn.read_very_eager().decode()
    if re.search(r'Vlan\d.+$', result1, re.S):
        survey = re.search(r'Vlan\d.+$', result1, re.S).group()
        data2['survey'] = survey[:-15]
    else:
        data2['survey'] = ''
    data['value'] = data2
    response.append(data)
    print('执行了vlan {}'.format(time.time() - start))
    return response


async def PWD_check(tn):#异步函数处理获取上网账号密码
    start = time.time()
    print('执行了pwd')
    data = {
        "label":'PPPOE',
        "value":None
    }
    data2 = {}
    tn.write(b' sh run | se ip route' + b'\n')
    time.sleep(2)
    result = tn.read_very_eager().decode()
    print(result)
    if re.search(r'ip route 0.0.0.0 .+192.168.+', result):
        print(re.search(r'ip route 0.0.0.0 .+192.168..+', result).group()+'-------'+'DHCP')
        data2['PPPOE'] = 'DHCP'
        data['value'] = data2
        response.append(data)
        return response
    elif re.search(r'ip route 0.0.0.0 0.0.0.0 Dialer2', result):
        print(re.search(r'ip route 0.0.0.0 0.0.0.0 Dialer2', result).group()+'-------'+'Dialer2')
        tn.write(b'sh run | se ppp' + b'\n')
        time.sleep(2)
        result1 = tn.read_very_eager().decode()
        print(result1)
        hostname = re.findall('hostname (.*).',result1)[0]
        print(hostname)
        password = re.findall('password \d (.*).', result1)[0]
        print(password)
        pwd = decrypt_type7(password)
        data2['PPPOE'] = 'Dialer2'
        data2['username'] = hostname
        data2['password'] = pwd
        data['value'] = data2
        response.append(data)
        return response
    else:
        data2['PPPOE'] = '获取错误'
        data['value'] = ''
        response.append(data)
        return response


@require_POST
def Info_Refer(request):#从数据库获取店铺相关信息
    start = time.time()
    data = {
        "stores":None,
        "area":None,
        "address":None,
        "stores_phone":None,
        "manager":None,
        "manager_phone":None,
        "router":None,
        "router_ip":None,
        "ap_type":None,
        "AP01":None,
        "AP02":None,
        "AP03":None,
        "AP04":None,
        "AP05":None,
    }
    request_data = json.loads(request.body)
    stores = request_data.get("stores")
    info = Info.objects.filter(storenumber = stores)
    for i in info:
        data['stores'] = i.storenumber
        data['address'] = i.address
        data['area'] = i.region
    phone = Contacts.objects.filter(storeno=stores)
    for i in phone:
        data['stores_phone'] = i.telephone
        data['manager'] = i.regional_manager
        data['manager_phone'] = i.regional_manager_phone
    devices = Devices.objects.filter(storeno=stores)
    for i in devices:
        data['router'] = i.router
        data['router_ip'] = i.router_ip
        if i.is_aruba == '是':
            data['ap_type'] = 'Aruba'
            data['AP01'] = i.ap_1
            data['AP02'] = i.ap_2
            data['AP03'] = i.ap_3
            data['AP04'] = i.ap_4
            data['AP05'] = i.ap_5
        else:
            data['ap_type'] = 'Cisco'
            data['AP01'] = {'ap_1_model':i.ap_1_model,'ap_1_ip':i.ap_1_ip}
            data['AP02'] = {'ap_2_model':i.ap_2_model,'ap_2_ip':i.ap_2_ip}
            data['AP03'] = {'ap_3_model':i.ap_3_model,'ap_3_ip':i.ap_3_ip}
            data['AP04'] = {'ap_4_model':i.ap_4_model,'ap_4_ip':i.ap_4_ip}
            data['AP05'] = {'ap_5_model':i.ap_5_model,'ap_5_ip':i.ap_5_ip}
    print('数据查询运行时间 {}'.format(time.time()-start))
    return JsonResponse({"code": 0, "data":data})


@require_POST
def regular_check(request):#实时监测AP类型
    start = time.time()
    request_data = json.loads(request.body)
    stores = request_data.get("stores")
    if '.' in stores:
        Stores = Devices.objects.filter(router_ip=stores)
    else:
        Stores = Devices.objects.filter(storeno=stores)
    if Stores :
        for i in Stores:
            if re.search(r'\d+.\d+.\d+.\d+',i.router_ip):
                Host = re.search(r'\d+.\d+.\d+.\d+', i.router_ip).group()
                try:
                    tn = telnetlib.Telnet(Host, port=23, timeout=5)
                    tn.set_debuglevel(0)
                    tn.write(b'mtlops' + b'\n')
                    tn.write(b'online' + b'\n')
                    print('cisco')
                    host_end = re.search(r'\d+$', Host).group()
                    host_head = re.search(r'\d+.\d+.\d+.', Host).group()
                    ap01 = host_head + str(int(host_end)+55)
                    telnet = bytes('telnet {}'.format(ap01),encoding='utf8')
                    tn.write(telnet + b'\n')
                    result = tn.read_very_eager().decode()
                    print(result)
                    tn.close()
                    # return data

                    # except Exception as e:
                except:
                    host_end = re.search(r'\d+$', Host).group()
                    host_head = re.search(r'\d+.\d+.\d+.', Host).group()
                    tn = telnetlib.Telnet(host_head + str(int(host_end) + 36), port=23, timeout=5)
                    tn.set_debuglevel(0)
                    tn.write(b'mtlops' + b'\n')
                    tn.write(b'online' + b'\n')
                    print('sdwan')
                    ap01 = host_head + str(int(host_end) + 55)
                    telnet = bytes('telnet {}'.format(ap01), encoding='utf8')
                    tn.write(telnet + b'\n')
                    result = tn.read_very_eager().decode()
                    print(result)
                    tn.close()
                    # return data

                finally:
                    print('执行完毕')
        print('运行时间 {}'.format(time.time()-start))
        return JsonResponse({"code": 0, "data": 'yes'})
    else:
        return JsonResponse({"code": 2, "message": '未查询到该店铺'})


class Do_telnet():#根据输入指令获取所需信息
    def __init__(self,Host,List):
        self.Host = Host
        self.List = List

    def Telnet(self):
        if '.' in self.Host:
            Stores = Devices.objects.filter(router_ip=self.Host)
        else:
            Stores = Devices.objects.filter(storeno=self.Host)
        if Stores:
            for i in Stores:
                if re.search(r'\d+.\d+.\d+.\d+', i.router_ip):
                    try:
                        tn = telnetlib.Telnet(self.Host, port=23, timeout=5)   #CISCO
                        tn.set_debuglevel(0)
                        tn.write(b'mtlops' + b'\n')
                        tn.write(b'online' + b'\n')
                        g, h, j = tn.expect([], timeout=3)
                        tn.write(b'en' + b'\n')
                        if re.search(r'ASW.+\d+', str(j, encoding='utf8')):
                            sds = bytes(re.search(r'ASW.+\d+', str(j, encoding='utf8')).group() + '1223',
                                        encoding='utf8')
                        else:
                            sds = bytes(re.search(r'[A-Z]+-[A-Z]+-\d+', str(j, encoding='utf8')).group() + '1223',
                                        encoding='utf8')
                        tn.write(sds + b'\n')
                        result = tn.read_very_eager().decode()
                        tn.close()



                    except:
                        host_end = re.search(r'\d+$', self.Host).group()
                        host_head = re.search(r'\d+.\d+.\d+.', self.Host).group()
                        tn = telnetlib.Telnet(host_head + str(int(host_end) + 36), port=23, timeout=5)  #SDWAN
                        tn.set_debuglevel(0)
                        tn.write(b'mtlops' + b'\n')
                        tn.write(b'online' + b'\n')
                        g, h, j = tn.expect([], timeout=3)
                        tn.write(b'en' + b'\n')
                        if re.search(r'ASW.+\d+', str(j, encoding='utf8')):
                            sds = bytes(re.search(r'ASW.+\d+', str(j, encoding='utf8')).group() + '1223',
                                        encoding='utf8')
                        else:
                            sds = bytes(re.search(r'[A-Z]+-[A-Z]+-\d+', str(j, encoding='utf8')).group() + '1223',
                                        encoding='utf8')
                        tn.write(sds + b'\n')

                        result = tn.read_very_eager().decode()
                        tn.close()


                    finally:
                        print('执行完毕')
            # print('运行时间 {}'.format(time.time() - start))
            return JsonResponse({"code": 0, "data": 'yes'})
        else:
            return JsonResponse({"code": 2, "message": '未查询到该店铺'})


    # def Order(self):
    #     for i in self.List:


def SankeyToJsonFromUrl_new(url):#桑基图数据处理
    data={}
    response = requests.get(url).content.decode()
    response = response.split("\r\n")
    nodes = []
    links = []
    soIndex = 2
    portIndex = 4
    deIndex = 6
    perIndex = 11
    for row in response[1:30]:
        rowList = row.split(',"')
        sourceIp = rowList[soIndex].replace('"', '').replace('[', '').replace(']', '')

        destinIp = rowList[deIndex].replace('"', '').replace('[', '').replace(']', '')
        Bytes = int(rowList[perIndex].replace('"', ''))
        sourcePort = rowList[portIndex].replace('"', '')
        # print(sourcePort)

        nodesList = set([key["name"] for key in nodes])

        if sourceIp == "":
            continue

        if sourceIp not in nodesList:
            nodes.append({"name": sourceIp, "value":Bytes})

        if destinIp not in nodesList:
            nodes.append({"name": destinIp, "value":Bytes})

        links.append({"source": sourceIp, "target": destinIp, "value": Bytes, "port":sourcePort})
    data["nodes"] = nodes

    data["links"] = links
    return data


@require_GET
def getSankeyFromUrl_GZ_HK(request):
    data={}
    try:
        url = "http://10.68.253.13/api/table.csv?&content=topdata&columns=position%2Cvalue_%2Cminigraph%2Cobjid%2Cbaselink&sortby=-value_2V&display=extendedheaders&subid=1&topnumber=-1&id=61236&username=Jace_Mo&passhash=3188079540"
        data["NetFlow"] = SankeyToJsonFromUrl_new(url)
    except Exception as e:
        print(e)
        # pass
    return JsonResponse({"code":0, "data":data})


@require_GET
def getSankeyFromUrl_HK_GZ(request):
    data={}
    try:
        url = "http://10.68.253.13/api/table.csv?&content=topdata&columns=position%2Cvalue_%2Cminigraph%2Cobjid%2Cbaselink&sortby=-value_2V&display=extendedheaders&subid=1&topnumber=-1&id=61235&username=Jace_Mo&passhash=3188079540"
        data["NetFlow"] = SankeyToJsonFromUrl_new(url)
    except Exception as e:
        print(e)
        # pass
    return JsonResponse({"code":0, "data":data})


def decrypt_type7(ep):#思科7型密码解密
	"""
	Based on http://pypi.python.org/pypi/cisco_decrypt/
	Regex improved
	"""
	dp = ''
	regex = re.compile('(^[0-9A-Fa-f]{2})([0-9A-Fa-f]+)')
	result = regex.search(ep)
	s, e = int(result.group(1)), result.group(2)
	for pos in range(0, len(e), 2):
		magic = int(e[pos] + e[pos+1], 16)
		if s <= 50:
			# xlat length is 51
			newchar = '%c' % (magic ^ xlat[s])
			s += 1
		if s == 51: s = 0
		dp += newchar
	return dp

def encrypt_type7(pt):#思科7型密码加密
	"""
	Make Type 7 Cisco password from a string
	"""
	salt = random.randrange(0,15);
	ep = "%02x" % salt
	for i in range(len(pt)):
		ep += "%02x" % (ord(pt[i]) ^ xlat[salt])
		salt += 1
		if salt == 51: salt = 0
	return ep
