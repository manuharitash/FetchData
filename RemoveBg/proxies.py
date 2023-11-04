import requests

proxies=open("proxies.txt", "r").read().strip().split("\n")

def get(url, proxy):
	try:
		r = requests.get(url, proxies={"http": f"http://{proxy}"})
		if r.status_code < 400: # client-side and server-side error codes are above 400
			return r
		else:
			print(r.status_code)
	except Exception as e:
		print(e)
	return None

def check_proxy(proxy):
	return get("http://www.google.com", proxy) is not None

available_proxies = list(filter(check_proxy, proxies))

def main():
   for proxy in available_proxies:
       print("available proxy:"+proxy+'\n')

if __name__=="__main__":
    main()
