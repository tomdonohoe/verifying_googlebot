import socket


def get_host_name(client_ip):
    try:
        host = socket.gethostbyaddr(client_ip)
        host_name = host[0]
    except:
        host_name = 'no host found'

    return host_name


def verify_host_name(host_name):
    return any([host_name.find('googlebot.com') > 0, host_name.find('google.com') > 0])


def get_bot_ip(host_name):
    return socket.gethostbyname(host_name)


def reverse_dns_lookup(client_ip):
    host_name = get_host_name(client_ip)
    verify_google = verify_host_name(host_name)
    if verify_google == True:
        bot_ip = get_bot_ip(host_name)

    return client_ip == bot_ip