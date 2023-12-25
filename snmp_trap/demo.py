from pysnmp.hlapi import *

oids = [
    '1.3.6.1.4.1.2011.2.15.1.7.3.1.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.2.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.3.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.4.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.7.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.8.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.9.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.12.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.13.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.15.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.12.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.13.0',
    '1.3.6.1.4.1.2011.2.15.1.7.3.15.0'
]

def snmp_listener():
    while True:
        for oid in oids:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData('*****'),
                       UdpTransportTarget(('0.0.0.0', 162)),
                       ContextData(),
                       ObjectType(ObjectIdentity(oid)))
            )

            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print(f'Error: {errorStatus.prettyPrint()} at {errorIndex}')
                break
            else:
                for varBind in varBinds:
                    print(varBind.prettyPrint())

# 启动监听
snmp_listener()
