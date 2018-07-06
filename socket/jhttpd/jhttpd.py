#!/usr/bin/python3

import socket
import os
import sys
import threading
import random
import datetime
import time
import json
import signal
import prettytable

GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

NORMAL_FORM = 'application/x-www-form-urlencoded'
FORM_DATA = 'multipart/form-data'


def splitByFisrt(raw, sepatator):
    try:
        pos = raw.index(sepatator)
        return (pos, raw[0: pos], raw[pos + len(sepatator):])
    except:
        return (-1, raw, None)


def parseAttrs(raw_data, attr_separator='&', name_value_separator='=', default_name='default'):
    attr_list = raw_data.split(attr_separator)
    data = dict()
    no_name = []
    for item in attr_list:
        pos, part1, part2 = splitByFisrt(item, name_value_separator)
        if pos == -1:
            no_name.append(item.strip())
        else:
            data[part1.strip()] = part2.strip()
    no_name_attr_amount = len(no_name)
    if no_name_attr_amount > 0:
        if len(no_name) == 1 or default_name != 'default':
            data[default_name] = no_name[0]
        elif len(no_name) > 1:
            data[default_name] = no_name
    return data

def getDir(path):
    path = path.strip('/')
    try:
        pos = path.rindex('/')
        return '/' + path[0:pos + 1]
    except:
        return '/'


# 处理http头部中每一行内部的参数
def parseHttpInnerAttrs(attr_value, attr_name='default'):
    inner_attr_list = attr_value.split(';')
    result = dict()
    for inner_attr in inner_attr_list:
        pos, part1, part2 = splitByFisrt(inner_attr, '=')
        if pos == -1:
            result[attr_name] = inner_attr
        else:
            result[part1.strip()] = part2.strip(' \n"')
    return result


# 生成随机字符串
def randomStr(length):
    result = ''
    for i in range(length):
        code_pool = [random.randint(97, 122), random.randint(64, 90), random.randint(48, 57)]
        code_pick = random.randint(0, len(code_pool) - 1)
        code = code_pool[code_pick]
        result = result + chr(code)
    return result

# 根据后缀获取http协议中的type
def getContentTypeBySuffix(suffix):
    try:
        result = config.conf['content_type'][suffix]
    except:
        result = 'application/octet-stream'
    return result

# 记录日志
class Log(object):
    TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEFAULT_LOG_FILE = 'jhttpd_default.log'

    def __init__(self):
        self.default_log_file = open(Log.DEFAULT_LOG_FILE, 'a')
        self.log_file = self.default_log_file
        self.debug = False

    def __del__(self):
        self.log_file.close()

    def setLogFile(self, path, log=False):
        try:
            file = open(path + 'jhttpd.log', 'a')
            self.log_file.close()
            self.log_file = file
            if log == True:
                self.log_i('set new log file at {path}'.format(path=path))
        except:
            pass

    # 记录错误信息
    def log_e(self, notice):
        log_info = 'ERROR {time}: {notice}\n'.format(time=self.getTime(), notice=notice)
        print(log_info, end='')
        self.log_file.write(log_info)

    # 记录提示信息
    def log_i(self, notice):
        log_info = 'INFO {time}: {notice}\n'.format(time=self.getTime(), notice=notice)
        print(log_info, end='')
        self.log_file.write(log_info)

    # 记录debug信息
    def log_d(self, notice):
        log_info = 'DEBUG {time}: {notice}\n'.format(time=self.getTime(), notice=notice)
        print(log_info, end='')
        if self.debug == True:
            self.log_file.write(log_info)

    def getTime(self):
        return time.strftime(Log.TIME_FORMAT, time.localtime())


# 服务器配置
class Config(object):
    # 可以通过短命令指定的配置项
    SHORT_ARGV = {
        'l': 'listen_port',
        'd': 'document_root',
        'm': 'max_client',
        't': 'timeout'
    }
    # 可以通过命令指定的配置项
    ARGV = [
        'listen_port',
        'document_root',
        'tmp_file_path',
        'max_client',
        'timeout'
    ]
    # 可通过配置文件配置的配置项
    CONFIG = [
        'listen_port',
        'document_root',
        'max_waiting_line',
        'tmp_file_path',
        'max_client',
        'timeout',
        'script_type',
        'default_page',
        'listen_ip',
        'show_dir',
        'max_header_size',
        'max_form_size',
        'max_entity_size',
        'max_form_data_header',
        'restart_interval'
    ]

    # 时间格式
    GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'

    def __init__(self):
        self.initDefaultConfig()
        self.readConfigFile()
        if self.readInputConfig() < 0:
            sys.exit(0)
        self.createWorkDir()
        log.setLogFile(self.conf['log_path'])
        self.setConfig()

    def createWorkDir(self):
        paths = [self.conf['document_root'], self.conf['tmp_file_path'], self.conf['log_path']]
        for item in paths:
            if not os.path.isdir(item):
                os.mkdir(item)
                log.log_i('Create new dir {path}'.format(path=item))

    def initDefaultConfig(self):
        conf = dict()
        work_path = os.getcwd()
        conf['document_root'] = work_path + '/www'
        conf['log_path'] = work_path + '/log/'
        conf['tmp_file_path'] = work_path + '/tmp/'
        conf['script_type'] = ['.sh', '.py']
        conf['default_page'] = ['index.html', 'index.py']
        conf['content_type'] = {
            '.css': 'text/css',
            '.js' : 'application/x-javascript',
            '.png': 'image/png',
            '.ico': 'image/x-icon',
            '.html': 'text/html',
            '.sh': 'text/html',
            '.pdf': 'application/pdf',
            '.php': 'text/html',
            '.c': 'text/plain',
            '.java': 'text/plain'
        }
        conf['listen_ip'] = '0.0.0.0'
        conf['listen_port'] = '9999'
        conf['max_client'] = '50'
        conf['timeout'] = '10'
        conf['max_waiting_line'] = '10'
        conf['max_entity_size'] = '10240'
        conf['max_form_size'] = '4096'
        conf['max_form_data'] = '4096'
        conf['max_form_data_header'] = '1024'
        conf['max_header_size'] = '2048'
        conf['show_dir'] = 'False'
        conf['restart_interval'] = '2'
        self.conf = conf

    def readConfigFile(self):
        config_path1 = '/etc/jhttpd/config.conf'
        config_path2 = './config/config.conf'
        if os.path.exists(config_path1):
            self.doReadConfigFile(config_path1)
        if os.path.exists(config_path2):
            self.doReadConfigFile(config_path2)

    def doReadConfigFile(self, file):
        linenum = 0
        with open(file, 'r') as f:
            while True:
                data = f.readline()
                linenum = linenum + 1
                # 读取结束
                if data == '':
                    break
                # 去掉行收尾空格等空白字符
                data = data.strip()
                # 该行为注释或空行时跳过
                if data == '' or data[0] == '#':
                    continue
                # 读取该行的数据
                else:
                    # 获取配置项名和值
                    pos, attr_name, attr_value = splitByFisrt(data, '=')
                    attr_name = attr_name.strip()
                    attr_value = attr_value.strip()
                    # 跳过不完整的配置项
                    if pos == -1:
                        log.log_e('uncomplete config item at line {linenum}'.format(linenum=linenum))
                        continue
                    elif attr_name not in Config.CONFIG:
                        log.log_e(
                            'unknown config item "{name}" at line {linenum}'.format(name=attr_name, linenum=linenum))
                        continue
                    else:
                        # 检查配置项的值是否为多个
                        multiple_value = attr_value.split(',')
                        if len(multiple_value) < 2:
                            # 读取单值配置项
                            self.conf[attr_name] = attr_value.strip()
                        else:
                            # 读取多值配置项
                            for i in range(len(multiple_value)):
                                multiple_value[i] = multiple_value[i].strip()
                            self.conf[attr_name] = multiple_value

    def readInputConfig(self):
        state = 0
        for item in sys.argv[1:]:
            # 读取配置项名称
            if state == 0:
                if item[0] != '-':
                    print('expect argument, not value:' + item)
                    return -1
                if item[0:2] == '--':
                    argv_name = item[2:]
                    if argv_name in Config.ARGV:
                        state = 1
                    else:
                        print('unknown argument ' + item)
                        return -1
                else:
                    try:
                        argv_name = Config.SHORT_ARGV[item[1:]]
                        state = 1
                    except:
                        print('unknown argument ' + item)
                        return -1
            # 读取配置项值
            elif state == 1:
                if item[0] == '-':
                    print('argument ' + last_argv + ' need value')
                    return -1
                self.conf[argv_name] = item
                state = 0
            else:
                print('unknown error')
                return -1
            last_argv = item

        if state == 1:
            print('argument ' + last_argv + ' need value')
            return -1
        return 0

    def setConfig(self):
        Request.MAX_FORM_DATA = int(self.conf['max_form_size'])
        Request.MAX_ENTIRY_SIZE = int(self.conf['max_entity_size'])
        Request.MAX_FORM_DATA_HEADER  = int(self.conf['max_form_data_header'])
        Request.MAX_FORM_SIZE = int(self.conf['max_form_size'])
        Request.MAX_HEADER_SIZE = int(self.conf['max_header_size'])
        Jhttpd.RESTART_INTERVAL = int(self.conf['restart_interval'])

    def show(self):
        a = prettytable.PrettyTable(['name', 'value'])
        a.align['value'] = 'l'
        for item in config.conf.items():
            a.add_row(item)
        print(a)

# 解析请求数据
class Request(object):
    # 请求实体最大长度
    MAX_ENTIRY_SIZE = 10240
    MAX_FORM_SIZE = 4096
    # form-data非文件项最大长度
    MAX_FORM_DATA = 4096
    # form-data项头部最大长度
    MAX_FORM_DATA_HEADER = 1024
    #http头部最大长度
    MAX_HEADER_SIZE = 2048
    # q请求接收状态
    DONE = 3

    def __init__(self, raw_data=None):
        # 整个http请求解析状态
        self.state = 0
        # post请求的整个form-data数据解析状态
        self.fd_state = 0
        # form-data中每项数据的解析状态
        self.fd_item_state = 0

        # 请求内容缓冲区，用于缓存为完全接收而暂时无法解析的数据
        self.byte_buf = b''

        # 当前接收的http请求正文长度
        self.recv_body_len = 0

        ##以下变量保存解析得到的数据
        # http头数据
        self.header = dict()
        # post获取的数据
        self.post = dict()
        # get获取的数据
        self.get = dict()
        # 上传的file
        self.file = dict()
        # 请求的url
        self.url = ''
        # 请求的类型
        self.type = ''
        # 实体长度
        self.content_length = 0
        self.content_type = None
        # 解析http请求得到的json文件路径，访问CGI脚本时会生成，CGI脚本可通过这些json文件获取该请求发送的数据
        self.variable_file = []

        # 完整的实体数据
        self.entity_data = None

        # 解析请求过程中对应的http响应状态，初始为正常
        self.status_code = 200

    def __del__(self):
        for file in self.variable_file:
            try:
                os.remove(file)
            except:
                pass

    def parse(self, raw_data):
        if raw_data == None or raw_data == b'':
            return self.state
        if self.recv_body_len > self.content_length:
            log.log_d('data is longer than said in content-length')
            self.status_code = 400
            self.state = -1
            return self.state
        # 处理新请求
        if self.state == 0:
            # 分割请求头
            header_len, header, body = splitByFisrt(raw_data, b'\r\n\r\n')
            if header_len == -1:
                log.log_d('http header is too long')
                self.state = -1
                self.status_code = 414
                return self.state

            # 解析请求头
            self.header = parseAttrs(header.decode('utf8'), '\r\n', ':', default_name='request_line')
            request_line = self.header['request_line'].split()
            if len(request_line) != 3:
                log.log_d('bad request-line')
                self.status_code = 400
                self.state = -2
                return self.state
            self.header['request_line'] = request_line

            # 获取请求类型和url
            request_type = self.header['request_line'][0]
            full_url = self.header['request_line'][1]
            pos, url, para = splitByFisrt(full_url, '?')
            self.type = request_type
            #检查url中是否有..
            file_names_in_url = url.split('/')
            if '..' in file_names_in_url or '.' in file_names_in_url:
                log.log_d('dectect .. or . in url, dangerours')
                self.state = -1
                self.status_code = 400
                return self.state
            self.url = url.strip('.')
            # 获取get请求url中的参数
            if request_type == 'GET':
                if pos != -1:
                    self.get = parseAttrs(para, '&', '=')
                self.state = Request.DONE
                return self.state
            # 处理包含数据的post方法
            elif request_type == 'POST':
                try:
                    self.content_length = int(self.header['Content-Length'])
                except:
                    log.log_d('receive post request but no content length')
                    self.state = -5
                    self.status_code = 411
                    return self.state
                if self.content_length > Request.MAX_ENTIRY_SIZE:
                    log.log_d('data is too long')
                    self.status_code = 413
                    self.state = -1
                    return self.state

                try:
                    content_type = parseAttrs(self.header['Content-Type'], ';', '=', 'content_type')
                except:
                    log.log_d('receive post request but no content type')
                    self.state = -6
                    self.status_code = 400
                    return self.state

                self.content_type = content_type['content_type']

                # 设置状态为处理数据部分
                if self.content_type == NORMAL_FORM:
                    # 清空缓冲区
                    self.content_type = NORMAL_FORM
                    self.byte_buf = b''
                    self.state = 1
                elif self.content_type == FORM_DATA:
                    self.content_type = NORMAL_FORM
                    self.fd_boudary = ('--' + content_type['boundary']).encode('utf8')
                    self.state = 2
                else:
                    log.log_d('unknown content-type')
                    self.status_code = 400
                    self.state = -2
                    return self.state

                # 处理数据
                if len(body) == 0:
                    log.log_d('waiting for entity data')
                    return self.state
                else:
                    return self.parse(body)

        # 处理普通表格数据的请求
        elif self.state == 1:
            # 统计接收内容长度
            self.recv_body_len = self.recv_body_len + len(raw_data)
            return self.parseNormalForm(raw_data)
        # 处理form-data
        elif self.state == 2:
            # 统计接收内容长度
            self.recv_body_len = self.recv_body_len + len(raw_data)
            return self.parseFormData(raw_data)
        # 请求处理完成
        else:
            return self.state

    def parseNormalForm(self, raw_data):
        # 统计接收到的body长度，全部接收时才开始处理
        self.recv_body_len = self.recv_body_len + len(raw_data)
        if self.recv_body_len < self.content_length:
            self.byte_buf = self.byte_buf + raw_data
            # post表单数据过大
            if len(self.byte_buf) > Request.MAX_FORM_SIZE:
                log.log_d('post form is too long')
                self.state = -4
                self.status_code = 413
            return self.state

        data = self.byte_buf.decode('utf8')
        self.entity_data = parseAttrs(data, '&', '=')
        # 记录post数据
        self.post = self.entity_data
        # 处理完成
        self.status_code = 202
        self.state = Request.DONE
        return self.state

    def parseFormData(self, raw_data):
        if self.fd_state == 0:
            self.entity_data = []
            self.is_item_last_part = False
            after_boundary = raw_data[len(self.fd_boudary): len(self.fd_boudary) + 2]
            raw_data = raw_data[len(self.fd_boudary) + 2:]

            # boundary后接两个短横线表示处理完成
            if after_boundary == b'--':
                self.state = Request.DONE
                self.status_code = 202
                return self.state
            self.fd_state = 1
            self.fd_item_state = 0
            return self.parseFormData(raw_data)
        elif self.fd_state == 1:
            try:
                end_pos = raw_data.index(self.fd_boudary)
            except:
                # 继续处理该item
                return self.parseFormDataItem(raw_data)
            form_data = raw_data[:end_pos - 2]
            # 处理form-data一个item的最后一部分数据
            self.is_item_last_part = True
            if self.parseFormDataItem(form_data) < 0:
                return self.state
            # 处理下一项
            self.is_item_last_part = False
            self.fd_state = 0
            return self.parseFormData(raw_data[end_pos:])

    def parseFormDataItem(self, form_data):
        # 初始化
        if self.fd_item_state == 0:
            self.fd_item = []
            self.fd_item_header = b''
            self.fd_item_state = 1
            return self.parseFormDataItem(form_data)
        # 处理头部
        elif self.fd_item_state == 1:
            header_len, header, body = splitByFisrt(form_data, b'\r\n\r\n')
            # 接收的数据不包含头部结束标志，头部还没有读取完整,等待头部数据继续处理
            if header_len == -1:
                log.log_d('waiting for form-data header')
                # 将新数据加入头部缓冲区
                self.fd_item_header = self.fd_item_header + form_data
                # 如果头部过长则报错
                if len(self.fd_item_header) > Request.MAX_FORM_DATA_HEADER:
                    log.log_d('form-data header too long')
                    self.state = -3
                    return self.state
            # 头部数据接收完成
            else:
                # 将头部最后一部分数据加入头部缓冲区，开始解析
                self.fd_item_header = self.fd_item_header + header
                header = parseAttrs(self.fd_item_header.decode('utf8'), '\r\n', ':')
                self.fd_item.append(header)
                if 'Content-Type' in header.keys():
                    # 该form-data为文件，转到处理文件的部分
                    self.fd_item_state = 2
                    # 生成临时文件名
                    self.tmp_file_name = config.conf['tmp_file_path'] + randomStr(20)
                    self.tmp_file = open(self.tmp_file_name, 'wb')

                    return self.parseFormDataItem(body)
                else:
                    # 该form-data为表单，转到处理表单的部分
                    self.fd_item_state = 3
                    # 清空数据缓冲区
                    self.byte_buf = b''
                    return self.parseFormDataItem(body)
        # 处理文件
        elif self.fd_item_state == 2:
            self.tmp_file.write(form_data)
            if self.is_item_last_part == True:
                self.tmp_file.close()
                self.fd_item.append(self.tmp_file_name)
                self.entity_data.append(self.fd_item)
                # 记录上传的文件
                attrs = parseHttpInnerAttrs(self.fd_item[0]['Content-Disposition'])
                self.file[attrs['name']] = {
                    'filename': attrs['filename'],
                    'path': self.fd_item[1]
                }
                return 0
        elif self.fd_item_state == 3:
            self.byte_buf = self.byte_buf + form_data
            if len(self.byte_buf) > Request.MAX_FORM_DATA:
                log.log_d('form data item is too long')
                self.state = -1
                self.status_code = 413
                return self.state
            if self.is_item_last_part == True:
                self.fd_item.append(self.byte_buf.decode('utf8'))
                self.entity_data.append(self.fd_item)
                # 记录post数据
                attrs = parseHttpInnerAttrs(self.fd_item[0]['Content-Disposition'])
                self.post[attrs['name']] = self.fd_item[1]
                return 0

    def generateSuperVariableFile(self):
        variable_file_type = ['server', 'get', 'post', 'file']
        variable_file_content = [self.header, self.get, self.post, self.file]
        for i in range(len(variable_file_content)):
            if len(variable_file_content[i]) != 0:
                file_name = '{dir}{type}_{random}'.format(dir=config.conf['tmp_file_path'], type=variable_file_type[i],
                                                          random=randomStr(10))
                with open(file_name, 'w') as f:
                    json.dump(variable_file_content[i], f)
                self.variable_file.append(file_name)


# 构造响应数据
class Response(object):
    # 响应数据构造状态
    DONE = 3
    # 单个数据包最大长度
    PACKAGE_MAX = 2048
    # http响应状态
    OK = 200
    ACCEPTED = 202
    BAD_REQUEST = 400
    NOT_FOUND = 404
    FORBIDDEN = 403
    INTERNAL_SERVER_ERROR = 500
    Length_Required = 411
    Request_Entity_Too_Large = 413
    Request_URI_Too_Large = 414
    # 状态码对应的说明
    REASON_PHRASE = {
        200: 'OK',
        202: 'ACCEPTED',
        400: 'BAD REQUEST',
        411: 'Length Required',
        413: 'Request Entity Too Large',
        414: 'Request-URI Too Large',
        404: 'NOT FOUND',
        403: 'FORBIDDEN',
        500: 'INTERNAL SERVER ERROR'

    }

    # 文件类型和后缀名


    def __init__(self, http_version='HTTP/1.1', status_code=200, content_type='text/html', content_filename=None,
                 entity_data=None, keep_alive = True):
        self.http_version = http_version
        self.status_code = str(status_code)
        self.reason_phrase = Response.REASON_PHRASE[status_code]
        self.date = datetime.datetime.utcnow().strftime(GMT_FORMAT)
        self.content_type = content_type
        self.content_length = 0
        self.entity_data = entity_data
        self.content_filename = content_filename
        self.pack_state = 0
        if keep_alive is True:
            self.connection = 'keep-alive'
        else:
            self.connection = 'close'
        self.extraHeader = ''
    #构造header
    def packHeader(self):
        header_format = (
            '{http_version} {status_code} {reason_phrase}\r\n'
            'Date: {date}\r\n'
            'Connection: {connection}\r\n'
            'Content-Type: {content_type}\r\n'
            'Content-Length: {content_length}\r\n'
        )

        header = header_format.format(http_version=self.http_version,
                                      status_code=self.status_code,
                                      reason_phrase=self.reason_phrase,
                                      date=self.date,
                                      connection=self.connection,
                                      content_type=self.content_type,
                                      content_length=self.content_length)
        header = header + self.extraHeader + '\r\n'
        return header.encode('utf8')
    #添加更多的http-header字段
    def addExtraHeader(self, items):
        for item in items:
            self.extraHeader = self.extraHeader + item + '\r\n'

    def pack(self):
        # 初始化，构造头部+较短的数据
        if self.pack_state == 0:
            entity = b''
            # 数据较短，和头部合并发送给客户端
            if self.entity_data != None:
                self.content_length = str(len(self.entity_data))
                self.state = Response.DONE
                entity = self.entity_data.encode('utf8')
            # 数据较长，单独发送给客户端
            elif self.content_filename != None:
                self.content_length = str(os.path.getsize(self.content_filename))
                self.content_file = open(self.content_filename, 'rb')
                self.pack_state = 1
            # 没有数据
            else:
                self.state = Response.DONE

            # 返回处理状态和数据
            data = self.packHeader() + entity
            return (self.pack_state, data)
        # 发送数据
        elif self.pack_state == 1:
            data = self.content_file.read(Response.PACKAGE_MAX)
            if data == b'':
                self.pack_state = Response.DONE
            return (self.pack_state, data)
        # 处理完成
        else:
            return (self.pack_state, None)

    # 发送数据
    def sendto(self, sk):
        while self.pack_state != Response.DONE:
            state, data = self.pack()
            if len(data) == 0:
                break
            try:
                sk.send(data)
            except:
                log.log_d('send failed')
                return -1
        return 0




class RequestHander(object):
    def __init__(self, socket):
        self.sk = socket

    def handle(self, request):
        # 请求解析失败
        if request.state < 0:
            return self.handleError(request.status_code)
        # 请求解析成功
        elif request.state == Request.DONE:
            self.request = request
            request_full_path = config.conf['document_root'] + request.url
            self.request_full_path = request_full_path
            if os.path.exists(request_full_path) == True:
                if os.path.isfile(request_full_path) == True:
                    return self.handleFileRequest()
                else:
                    for item in config.conf['default_page']:
                        file_path = request_full_path + item
                        if os.path.isfile(file_path) == True:
                            self.request_full_path = file_path
                            return self.handleFileRequest()
                    # 当前目录下不包含默认页面时显示目录
                    #目录不是以/结尾时添加/号
                    if self.request_full_path[-1] != '/':
                        self.request_full_path = self.request_full_path + '/'
                    return self.handleDirRequest()
            else:
                return self.handleError(Response.NOT_FOUND)
        # 等待解析完成
        else:
            pass

        return 0

    def handleError(self, error, response_message=None, response_page=None):
        # 不指定回显的错误信息时设置为默认错误提示
        if response_page == None and response_message == None:
            response_message = Response.REASON_PHRASE[error]
        # response类会优先使用entity-data, 没有时才使用文件

        response = Response(status_code=error, entity_data=response_message, content_filename=response_page)
        response.sendto(self.sk)
        return -1


    def handleDirRequest(self):
        if config.conf['show_dir'] == 'False':
            return self.handleError(Response.FORBIDDEN)
        files = os.listdir(self.request_full_path)
        # url为目录，需要和文件名拼接成path，如果url不是以/结尾则加上/
        if self.request.url[-1] != '/':
            url = self.request.url + '/'
        else:
            url = self.request.url

        # 生成页面
        page_name = self.generateDirHtml(url, files)
        # 构造响应并发送
        response = Response(content_filename=page_name)
        state = response.sendto(self.sk)
        # 移除临时文件
        os.remove(page_name)
        return state


    def generateDirHtml(self, path, files):
        html_format = '''
        <html>
            <head>
                <title>{title}</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>Current Path: {title}</h1>
                <a href={up_path}>上一级</a>
                {body}
            </body>
        </html>
        '''
        item_format = '<div><a href={path}>{filename}</div>'

        tmp_file_name = config.conf['tmp_file_path'] + randomStr(10)
        body = ''
        with open(tmp_file_name, 'w') as f:
            for file in files:
                if os.path.isdir(self.request_full_path + file):
                    file = file + '/'
                item = item_format.format(path=path + file, filename=file)
                body = body + item
            html = html_format.format(title=path, up_path=getDir(path), body=body)
            f.write(html)
        return tmp_file_name



    def handleFileRequest(self):
        # 获取文件后缀名
        nouse, suffix = os.path.splitext(self.request_full_path)
        suffix = suffix.lower()

        # 如果是可执行脚本，执行后将结果返回
        if suffix in config.conf['script_type']:
            # 执行脚本
            tmp_file_path = config.conf['tmp_file_path'] + randomStr(20)
            command = self.request_full_path + '>>' + tmp_file_path
            self.request.generateSuperVariableFile()
            exit_code = os.system(command)
            # 脚本执行出错
            if exit_code != 0:
                self.handleError(Response.INTERNAL_SERVER_ERROR)
                os.remove(tmp_file_path)
                return -1
            # 构造响应数据
            response = Response(status_code=self.request.status_code, content_filename=tmp_file_path)
        else:
            # 构造响应数据
            content_type = getContentTypeBySuffix(suffix)
            response = Response(status_code=self.request.status_code, content_filename=self.request_full_path,
                                content_type=content_type)

        # 发送响应数据
        state = response.sendto(self.sk)
        # 如果存在临时文件则删除
        try:
            os.remove(tmp_file_path)
        except:
            pass

        return state

class Sighandler(object):
    def __init__(self):
        signal.signal(signal.SIGINT, self.sigint)
        signal.signal(signal.SIGPIPE, self.sigpipe)
        signal.signal(signal.SIGCHLD, self.sigchild)
    def sigint(self, num, frame):
        if os.getpid() == daemon_id:
            log.log_i('server daemon exit manually')
            sys.exit(0)
        else:
            log.log_i('server exit manually')
            os._exit(0)


    def sigpipe(self, num, frame):
        log.log_i('session closed, pid is {pid}'.format(pid=pid))
        sys.exit(0)

    def sigchild(self, num, frame):
        pass

class Resource(object):
    def __init__(self, resource_amount):
        self.lock = threading.Lock()
        self.res = resource_amount

    def get(self):
        self.res = self.res - 1
        if self.res <= 0:
            if self.res == 0:
                log.log_d('resource not sufficient, thread will be block')
            self.lock.acquire()
    def release(self):
        self.res = self.res + 1
        if self.res == 1:
            log.log_d('release a resource')
            self.lock.release()

#服务器对象
class Jhttpd(object):
    # 服务器进程异常终止后重启服务器进程的时间间隔
    RESTART_INTERVAL = 2

    def __init__(self):
        self.initSocket()
        self.res = Resource(int(config.conf['max_client']))

    def __del__(self):
        self.listen_sk.close()

    def initSocket(self):
        listen_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.listen_sk = listen_sk
        listen_sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        address = (config.conf['listen_ip'], int(config.conf['listen_port']))
        listen_sk.bind(address)
        listen_sk.listen(5)

    #服务器主过程
    def run(self):
        while True:
            log.log_d('waiting for connection')
            se, addr = self.listen_sk.accept()
            #接收到一个请求就新建一个线程来处理
            #新建一个线程就消耗一个资源，当资源耗尽时服务器等待其他会话结束再响应请求
            self.res.get()
            session = threading.Thread(target=self.session, args=(se,))
            session.start()

    def session(self, se):
        try:
            # 设置超时
            se.settimeout(int(config.conf['timeout']))
            # 建立请求处理对象
            request_handler = RequestHander(se)
            # 建立请求解析对象
            request = Request()
            # 接收请求
            while True:
                try:
                    data = se.recv(Request.MAX_HEADER_SIZE)
                except:
                    # 超时则关闭此会话
                    log.log_d('session timeout')
                    se.close()
                    self.res.release()
                    return

                # 接收并解析请求数据
                request_parse_state = request.parse(data)
                request_handle_state = request_handler.handle(request)
                if request_handle_state < 0:
                    se.close()
                    self.res.release()
                    return

                if request_parse_state == Response.DONE:
                    # 处理完毕后构造新请求对象用于处理下一次请求
                    request = Request()
        except:
            self.res.release()
            se.close()

#主程序
#记录守护进程id
daemon_id = os.getpid()
#初始化日志
log = Log()
#初始化配置
config = Config()

#初始化信号处理
sighandler = Sighandler()
#主循环
while True:
    #创建服务器进程
    pid = os.fork()
    if pid == 0:
        server = Jhttpd()
        server.run()
    else:
        #守护进程在服务器进程意外结束时负责重启服务器进程
        id, info = os.wait()
        time.sleep(Jhttpd.RESTART_INTERVAL)
        if info == 0:
            log.log_i('server closed')
            sys.exit(0)
        else:
            log.log_e('server process exit unexpectedly')
