import json
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto import rfc1902

# 转换规则字典
translations = {
    "1.3.6.1.4.1.2011.2.15.1.7.3.1.0": "设备类型",
    "1.3.6.1.4.1.2011.2.15.1.7.3.2.0": "设备名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.3.0": "事件类型",
    "1.3.6.1.4.1.2011.2.15.1.7.3.4.0": "告警产生时间",
    "1.3.6.1.4.1.2011.2.15.1.7.3.7.0": "告警级别",
    "1.3.6.1.4.1.2011.2.15.1.7.3.8.0": "告警序列号",
    "1.3.6.1.4.1.2011.2.15.1.7.3.9.0": "清除告警的流水号",
    "1.3.6.1.4.1.2011.2.15.1.7.3.12.0": "EMS名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.13.0": "网元名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.15.0": "机柜名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.16.0": "子架名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.17.0": "单板名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.18.0": "端口类型",
    "1.3.6.1.4.1.2011.2.15.1.7.3.20.0": "告警定位对象",
    "1.3.6.1.4.1.2011.2.15.1.7.3.22.0": "告警ID",
    "1.3.6.1.4.1.2011.2.15.1.7.3.23.0": "告警名称",
    "1.3.6.1.4.1.2011.2.15.1.7.3.24.0": "告警产生对象的设备IP地址",
    "1.3.6.1.4.1.2011.2.15.1.7.3.26.0": "是否是清除告警"
}


# 需要转换为UTF-8字符串的OID列表
hex_to_utf8_oids = [
    "1.3.6.1.4.1.2011.2.15.1.7.3.2.0",  # 设备名称
    "1.3.6.1.4.1.2011.2.15.1.7.3.13.0", # 网元名称
    "1.3.6.1.4.1.2011.2.15.1.7.3.16.0", # 子架名称
    # ... 其他需要转换的OID
]

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
    trap_info = {}
    for name, val in varBinds:
        oid = str(name)
        value = val.prettyPrint()

        if oid in hex_to_utf8_oids:
            try:
                # 去除前缀0x并转换为UTF-8
                #value = binascii.unhexlify(value[2:]).decode('utf-8')
                value = bytes.fromhex(value[2:]).decode('utf-8')
            except:
                value = '转换错误'

        translated_name = translations.get(oid, oid)
        trap_info[translated_name] = value

    json_data = json.dumps(trap_info, ensure_ascii=False)
    print("Received new trap message:")
    print(json_data)

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
