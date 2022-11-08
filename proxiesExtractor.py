import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm

class proxiesExtractor:
    def __init__(self) -> None:
        self.proxyUrl = "https://free-proxy-list.net/"
        self.TestIpUrl = "http://httpbin.org/ip"
        self.dfProxies = pd.DataFrame(columns=["proxy","ResponseTime","isAvailable"])
        print("Getting free proxies from source ...!")
        self.proxies = self.get_free_proxies()
        if len(self.proxies)>0:
            print(f"Found {len(self.proxies)} proxies")
        else :
            print("no proxies found ! try again later.")

    def get_free_proxies(self):
       
        soup = bs(requests.get(self.proxyUrl).content, 'html.parser')
        proxies = []
        for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip, port = tds[0].text.strip(), tds[1].text.strip()
                proxies.append(f"{ip}:{port}")
            except Exception as e:
                continue
        return proxies
    
    def testProxies(self, maxNumber = 10, timeOut = 2):
        
        print("testing proxies... !")
        for proxy in tqdm(self.proxies[:maxNumber]):
            try:
                response = requests.get(self.TestIpUrl, proxies = {"http":proxy, "https":proxy}, timeout=timeOut)
                self.dfProxies = self.dfProxies.append({"proxy": proxy,"ResponseTime" : response.elapsed.total_seconds(),"isAvailable" : True},ignore_index = True)
            except:
                # if the proxy Ip is pre occupied
                self.dfProxies = self.dfProxies.append({"proxy": proxy,"ResponseTime" : -1,"isAvailable" : False},ignore_index = True)
        self.dfProxies.to_excel("proxies.xlsx",index=False)

if __name__ == "__main__":
    ips= proxiesExtractor()
    ips.testProxies()