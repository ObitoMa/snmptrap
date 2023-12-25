from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv

# 创建SNMP引擎实例
snmpEngine = engine.SnmpEngine()

# 设置监听地址和端口
config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode(('0.0.0.0', 162))
)

# 配置SNMPv2c社区名称
community_name = 'ceni@2023'
config.addV1System(snmpEngine, 'my-area', community_name)

# 定义处理函数
def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print("Received new trap message:")
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))

# 注册回调函数
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

# 运行监听
snmpEngine.transportDispatcher.jobStarted(1)

try:
    # 这将阻塞并处理传入的请求
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise

