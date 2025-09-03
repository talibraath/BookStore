from django.http import HttpResponseForbidden
from ipaddress import ip_address, ip_network


class IPBlockerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        agent_meta = request.META
        ip = agent_meta.get('REMOTE_ADDR')

        blocked_ips = [
            '127.0.1.1',
        ]
        blocked_networks = [
            '39.32.0.0/11', 
        ]

        if ip in blocked_ips:
            return HttpResponseForbidden("Access denied.")

        for net in blocked_networks:
            if ip_address(ip) in ip_network(net):
                # print("Blocked IP:", ip)
                return HttpResponseForbidden("Access denied.")

        return self.get_response(request)