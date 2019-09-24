# Verifying Googlebot with Python

When preparing server log files for SEO analysis you must verify requests from Googlebot are real.

To verify hits from Googlebot are real you need to run a DNS lookup. In this guide, I will explain how you can run the DNS lookup using Python.

## Steps to verify Googlebot with a DNS lookup
There are three steps outlined by Google in their documentation for verifying Googlebot that you must follow:

1. Run a reverse DNS lookup on the accessing IP address from your logs, using the host command.
2. Verify that the domain name is in either googlebot.com or google.com
3. Run a forward DNS lookup on the domain name retrieved in step 1 using the host command on the retrieved domain name. Verify that it is the same as the original accessing IP address from your logs.

## Step 1: reverse DNS lookup
First, run a reverse DNS lookup on the accessing IP address from the server log files.

Use the ```socket``` module to get the hostname from the IP address:
```python
host = socket.gethostbyaddr(client_ip)
print(host)
# ('crawl-66-249-79-136.googlebot.com', ['136.79.249.66.in-addr.arpa'], ['66.249.79.136'])

host_name = host[0]
print(host_name)
# crawl-66-249-79-136.googlebot.com
```

Here's the function I've defined:
```python
def get_host_name(client_ip):
    try:
        host = socket.gethostbyaddr(client_ip)
        host_name = host[0]
    except:
        host_name = 'no host found'

    return host_name
```

The function will return the hostname of the IP address, otherwise 'no host found'.

## Step 2: verify the host name
Second, we must verify that the host name contains either googlebot.com or google.com:

We can use the function above to store the hostname as a variable:
```python
dns_host_name = get_host_name(client_ip)
# 'crawl-66-249-79-136.googlebot.com'
```
Then use the string method ```find()``` to check if googlebot.com or google.com are in the string.
```python
googlebot = dns_host_name.find('googlebot.com')
google = dns_host_name.find('google.com')

print(googlebot)
# 20
print(google)
# -1
```
The ```find()``` method finds the first occurrence of the specified value returns the index, otherwise returns -1 if the value is not found.

Knowing this we can create a list with logical operators to return true if the string contains one of the hostnames or false if it doesn't.
```python
check = [dns_host_name.find('googlebot.com') > 0, dns_host_name.find('google.com') > 0]
print(check)
# [True, False]
```
Finally, we want to verify if the host name contains either googlebot.com or google.com. 

We can use the ``` any() ``` function, which returns True if any item in an iterable are true, otherwise it returns False.
```python
is_google = any(check)
print(is_google)
# True
```
Here's the function I've defined:
```python
def verify_host_name(host_name):
    return any([host_name.find('googlebot.com') > 0, host_name.find('google.com') > 0])
```
## Step 3: forward DNS lookup hostname
Third, run a forward DNS lookup on the host name retrieved in step 1 to get the IP address. 

Verify that the IP is the same as the original accessing IP address from your logs.

Use the ```socket``` module again to forward lookup the hostname to get the IP address:

```python
ip = socket.gethostbyname(host_name)
print(ip)
# 66.249.79.136 
```
Then check to see if the client_ip from log files equals the IP from DNS lookup:
```python
print(client_ip == ip)
# True
```
Here's the function I've defined:
```python
def get_bot_ip(host_name):
    return socket.gethostbyname(host_name)
```
## Bring it together in a Function

The last step is to build a function that brings all the steps together.

The function needs to:

1. Store the host name as a variable via a reverse DNS on client ip address from log files.
2. Verify the host name contains googlebot.com or google.com.
3. If the host name does contain googlebot.com or google.com then get the ip address associated with the host name.
4. Return True if the client ip from logs is the same as reverse ip lookup, otherwise False.

Here is the final function:
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