


def get_headers_generic():
	headers = {"Accept": "application/json", 
	"Content-Type":"application/json;charset=utf-8", 
	"Connection":"keep-alive", 
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0"}
	return headers
def get_headers_authorization(authorization_token):
	headers = get_headers_generic()
	headers["Authorization"] = "Bearer" +" " + authorization_token
	return headers








