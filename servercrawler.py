import requests
from bs4 import BeautifulSoup as bs
import time

start_time = time.time()
directory = 'pythontest/index.html'
pages = 3
ips = []
articlename = []
articlelink = []
statuslink = ''

html_prefix= """<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
}
</style>
</head>
<body>

<h2>巴哈伺服器爬蟲</h2>
<p>Credit: https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18</p>

<table style="width:100%">
  <tr>
    <th>伺服器名稱</th>
    <th>IP</th> 
    <th>文章連結</th>
  </tr>"""

html_table=""""""

html_suffix= """</table>

</body>
</html>"""

def articlesfrombahamut():
    listurl = 'https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18&page='
    for no in range(1,pages+1):
        listres = requests.get(listurl+str(no))
        listsoup = bs(listres.text,'html.parser')
        articles = listsoup.find_all('a',class_='b-list__main__title')
        statusfromarticle(articles)
        
def statusfromarticle(articles):
    for art in articles:
        res = requests.get('https://forum.gamer.com.tw/'+art['href'])
        soup = bs(res.text,'html.parser')
        status = soup.find_all('a',class_='url-image')
        for stat in status:
            if(stat['href'][:25]=='https://minecraft-mp.com/') or (stat['href'][:24]=='http://minecraft-mp.com/'):
                articlename.append(soup.find_all('h1')[0].string)
                articlelink.append('https://forum.gamer.com.tw/'+art['href'])
                statuslink = stat['href']
                ipfromstatus(statuslink)
                
def ipfromstatus(statuslink):
    statres = requests.get(statuslink)
    statsoup = bs(statres.text,'html.parser')
    strong = statsoup.find_all('strong')
    ips.append(strong[1].string)

articlesfrombahamut()
for server in range(2,len(articlename)):
    if(ips[server] is None):
        continue
    html_table= html_table+"""
      <tr>
        <td>&1</td>
        <td>&2</td>
        <td>&3</td>
      </tr>"""
    html_table = html_table.replace('&1',articlename[server])
    html_table = html_table.replace('&2',ips[server])
    html_table = html_table.replace('&3',articlelink[server])
html_out = open(directory,'w',encoding="utf-8")
html_out.write(html_prefix+html_table+html_suffix)
html_out.close()
print('Crawler has successfully exported the content to index.html in'+ str(time.time()-start_time) + 'seconds')
