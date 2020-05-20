from bs4 import BeautifulSoup
import requests
import json

def job_desc(s, x):

	print("Job Description:", x)
	l=list(s.split())

	import re
	c0=0
	c1=0
	res=''
	for i in range(len(l)):
	    if(re.search("title=\"*",l[i])):
	        c0= i
	        tmp = l[c0:]
	        for j in range(len(tmp)):
	            if(re.search(".*//",tmp[j])):
	                c1=j+1
	                res=tmp[:c1]
	                #print(tmp[:c1])
	                break
	        
	res=' '.join(res)
	res=res.replace('title=\"', '')
	res=res.replace('//', '')
	print("Title: ", res)

	res1=''
	for i in range(len(l)):

	    if(re.search("Keyskills:*",l[i])):
	            c0= i
	            tmp = l[c0:]
	            for j in range(len(tmp)):
	                if(re.search(".*\<\/span><\/div>",tmp[j])):
	                    c1=j+1
	                    res1=tmp[:c1]
	                    #print(tmp[:c1])
	                    break

	res1=' '.join(res1)
	res1=res1.replace('class=\"black\">', '')
	res1=res1.replace('</span><span>', '')
	res1=res1.replace('</span></div>,', '')
	print(res1)

	res2=''
	for i in range(len(l)):

	    if(re.search("Summary:*",l[i])):
	            c0= i
	            tmp = l[c0:]
	            for j in range(len(tmp)):
	                if(re.search(".*\<\/span><\/div>",tmp[j])):
	                    c1=j+1
	                    res2=tmp[:c1]
	                    #print(tmp[:c1])
	                    break

	res2=' '.join(res2)
	k = list(res2.split())
	for i in range(len(k)):
	    if(re.search("</span><span>*", k[i])):
	        c1 = i
	        tmp = k[c1:]
	        for j in range(len(tmp)):
	            if(re.search(".*\<\/span><\/div>",tmp[j])):
	                    c1=j+1
	                    res2=tmp[:c1]
	                    #print(tmp[:c1])
	                    break
	res2=' '.join(res2)
	res2 = res2.replace('</span><span>','')
	res2 = res2.replace(' </span></div>,','')
	print(res2)

def main():		
	alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	for x in alpha:
		url = 'https://my.monsterindia.com/find-companies.html?l='+x
		response = requests.get(url, timeout=30)
		content = BeautifulSoup(response.content)
		# print("bhanu1")
		# print(content)

		tweetArr = []
		i = 0
		for tweet in content.findAll('div', attrs = {"class":"col-xs-8"}):
			# print("bhanu")
			tweetObject = {
		        "Name": tweet.find("span", attrs = {"class":"cmpname"}),
		        "Jobs": tweet.find("a", attrs = {"class":"mn-lnk1"})
		    }
			tweetArr.append(str(tweetObject))
			urlArr = []
			for a in range(0,len(tweetArr)):
				if(a == i):
					i1 = tweetArr[a].index('href')
					i2 = tweetArr[a].index('target')
					link = tweetArr[a]
					m = link[i1+6:i2-2]
					m = 'https:' + m
					xurl = m
					print(xurl)
					urlArr.append(m)
					linkresp = requests.get(xurl,timeout=1000)
					linkcont = BeautifulSoup(linkresp.content, features = "lxml")
					# for x in linkcont.findAll()
					# print(linkcont)
					arr = []
					for x in linkcont.findAll('div', attrs = {"class":"jobwrap"}):
						xObject = {
							"Job Desc": x.find('a', attrs = {"class":"title_in"}),
							"Keyskills and Summary": x.findAll('div', attrs = {"class":"jtxt"}),
							"Location": x.find('div', attrs = {"class":"jtxt jico ico1"}),
							"Exp": x.find('div', attrs = {"class":"jtxt jico ico2"})
						}
						arr.append(str(xObject))
					for k in arr:
						job_desc(k, arr.index(k))
					#print(arr)
		print(urlArr)
		i = i + 1

		with open('jobdata.json','w') as outfile:
			json.dump(tweetArr,outfile)



if(__name__ == "__main__"):
	main()