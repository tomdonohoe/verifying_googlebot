# Verifying Googlebot with Python

When preparing server log files for SEO analysis you must verify requests from Googlebot are real.

To verify hits from Googlebot are real you need to run a DNS lookup. In this guide, I will explain how you can run the DNS lookup using Python.

## Steps to verify Googlebot with a DNS lookup
There are three steps outlined by Google in their documentation for verifying Googlebot that you must follow:

1. Run a reverse DNS lookup on the accessing IP address from your logs, using the host command.
2. Verify that the domain name is in either googlebot.com or google.com
3. Run a forward DNS lookup on the domain name retrieved in step 1 using the host command on the retrieved domain name. Verify that it is the same as the original accessing IP address from your logs.

## Step 1: reverse DNS lookup
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

## Step 2: verify the host name
Verify that the domain name is in either googlebot.com or google.com:
```python
def verify_host_name(host_name):
    return any([host_name.find('googlebot.com') > 0, host_name.find('google.com') > 0])
```
## Step 3: forward DNS lookup hostname
Run a forward DNS lookup on the domain name retrieved in step 1. Verify that it is the same as the original accessing IP address from your logs:

```python
def get_bot_ip(host_name):
    return socket.gethostbyname(host_name)
```
## Bring it together in a Function
Pull all the steps together into one function:

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
    else:
        bot_ip = False

    return client_ip == bot_ip
```