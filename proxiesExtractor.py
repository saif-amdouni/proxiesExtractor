import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
import argparse


class proxiesExtractor:
    def __init__(self, country = None) -> None:
        self.proxyUrl = "https://free-proxy-list.net/"
        self.TestIpUrl = "http://httpbin.org/ip"
        self.dfProxies = pd.DataFrame(columns=["proxy","ResponseTime","isAvailable"])
        print("Getting free proxies from source ...!")
        self.proxies = self.get_free_proxies(country)
        if len(self.proxies)>0:
            print(f"Found {len(self.proxies)} proxies")
        else :
            print("no proxies found ! try again later.")

    def get_free_proxies(self,country = None):
       
        soup = bs(requests.get(self.proxyUrl).content, 'html.parser')
        proxies = []
        for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
            tds = row.find_all("td")
            try:
                ip, port = tds[0].text.strip(), tds[1].text.strip()
                
                if country and (tds[2].text.strip() != country):
                    continue
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


    parser = argparse.ArgumentParser()
    parser.add_argument('--country',default=None,type=str, help='Retrieve proxies from specific country')
    parser.add_argument('--maxNumber',default=10,type=int, help='The maximum number of proxies to test')
    parser.add_argument('--timeOut',default=2,type=int, help='timeout')

    args = parser.parse_args()
    print(args)
    ips= proxiesExtractor(country = args.country)
    ips.testProxies(maxNumber = args.maxNumber, timeOut = args.timeOut)


