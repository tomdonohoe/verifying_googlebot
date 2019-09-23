# Verifying Googlebot with Python

Run a reverse DNS lookup on the accessing IP address from your logs:

```python
def get_host_name(client_ip):
    try:
        host = socket.gethostbyaddr(client_ip)
        host_name = host[0]
    except:
        host_name = 'no host found'

    return host_name
```

Verify that the domain name is in either googlebot.com or google.com:
```python
def verify_host_name(host_name):
    return any([host_name.find('googlebot.com') > 0, host_name.find('google.com') > 0])
```

Run a forward DNS lookup on the domain name retrieved in step 1. Verify that it is the same as the original accessing IP address from your logs:

```python
def get_bot_ip(host_name):
    return socket.gethostbyname(host_name)
```

Bring it together by:

1. get the host name via reverse DNS on client ip address
2. check the host name contains googlebot.com or google.com
3. if the host name does contain googlebot.com or google.com get the bot ip
4. check if the client ip from logs is the same as reverse ip lookup

```python
def reverse_dns_lookup(client_ip):
    host_name = get_host_name(client_ip)
    verify_google = verify_host_name(host_name)
    if verify_google == True:
        bot_ip = get_bot_ip(host_name)

    return client_ip == bot_ip
```