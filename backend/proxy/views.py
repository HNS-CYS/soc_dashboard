import requests
import urllib3
from django.http import HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

# Disable SSL warnings for HTTPS proxying
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target service mappings
SERVICE_URLS = {
    'wazuh': 'http://localhost:5601',
    'shuffle': 'http://localhost:3000',
    'iris': 'https://localhost:443',
    'velociraptor': 'http://localhost:8889',
}

# Hop-by-hop headers that should not be forwarded
HOP_BY_HOP_HEADERS = [
    'connection', 'keep-alive', 'proxy-authenticate',
    'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade'
]


def get_headers(request):
    """Extract and clean headers from the incoming request."""
    headers = {}
    for key, value in request.META.items():
        if key.startswith('HTTP_'):
            header_name = key[5:].replace('_', '-').title()
            if header_name.lower() not in HOP_BY_HOP_HEADERS:
                headers[header_name] = value
    
    # Add content-type if present
    if request.content_type:
        headers['Content-Type'] = request.content_type
    
    return headers


@csrf_exempt
@xframe_options_exempt
def proxy_view(request, service, path=''):
    """
    Generic proxy view that forwards requests to target services.
    Supports GET, POST, PUT, PATCH, DELETE methods.
    """
    
    if service not in SERVICE_URLS:
        return HttpResponse('Service not found', status=404)
    
    target_url = SERVICE_URLS[service]
    
    # Construct full URL
    if path:
        url = f"{target_url}/{path}"
    else:
        url = target_url
    
    # Add query parameters
    if request.GET:
        query_string = request.GET.urlencode()
        url = f"{url}?{query_string}"
    
    # Prepare headers
    headers = get_headers(request)
    
    # Remove host header to avoid conflicts
    headers.pop('Host', None)
    
    # Get cookies
    cookies = request.COOKIES
    
    # Prepare request data
    data = request.body if request.method in ['POST', 'PUT', 'PATCH'] else None
    
    try:
        # Make the request to the target service
        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            data=data,
            cookies=cookies,
            verify=False,  # Disable SSL verification
            allow_redirects=False,
            stream=True,
            timeout=30
        )
        
        # Create Django response
        django_response = StreamingHttpResponse(
            response.iter_content(chunk_size=8192),
            status=response.status_code,
            content_type=response.headers.get('content-type', 'text/html')
        )
        
        # Forward response headers (excluding hop-by-hop)
        for key, value in response.headers.items():
            if key.lower() not in HOP_BY_HOP_HEADERS:
                django_response[key] = value
        
        # Add CORS headers
        django_response['Access-Control-Allow-Origin'] = '*'
        django_response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        django_response['Access-Control-Allow-Headers'] = '*'
        django_response['Access-Control-Allow-Credentials'] = 'true'
        
        # Remove X-Frame-Options to allow iframe embedding
        django_response.pop('X-Frame-Options', None)
        
        # Forward cookies
        for cookie in response.cookies:
            django_response.set_cookie(
                key=cookie.name,
                value=cookie.value,
                max_age=cookie.expires,
                path=cookie.path,
                domain=cookie.domain,
                secure=cookie.secure
            )
        
        return django_response
        
    except requests.exceptions.ConnectionError:
        return HttpResponse(
            f'Unable to connect to {service}. Please ensure the service is running.',
            status=503
        )
    except requests.exceptions.Timeout:
        return HttpResponse(
            f'Request to {service} timed out.',
            status=504
        )
    except Exception as e:
        return HttpResponse(
            f'Proxy error: {str(e)}',
            status=500
        )