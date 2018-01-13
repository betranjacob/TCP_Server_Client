import cProfile
import time
def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('%s function took %0.3f ms' % (f.__name__, (time2-time1)*1000.0))
        return ret
    return wrap

@timing
def parse_data_file(filename='data'):

    ip_cmd_map={}
    with open(filename) as f:
        lines = open(filename).readlines()

        for l in lines:
            l = l.strip('\n')
            ip, cmd, response, delay  = l.split(':')
            ip_cmd_map.setdefault(ip, {})
            ip_cmd_map[ip][cmd] = [delay, response]

    return ip_cmd_map



#from netaddr import IPAddress
ip_cmd_map = parse_data_file('data')

#print(ip_cmd_map[str(IPAddress('137.72.95.001'))]['foo'][0])
#for k in ip_cmd_map:
#    print('{}:{}'.format(k, ip_cmd_map[k]['foo'][0]))
