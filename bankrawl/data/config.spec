loglevel = option('DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL', default='WARN')
banks = list()

[banks]
[[__many__]]
username=string(default=None)
password=string(default=None)
accounts=list(default=None)
__many__=string()
