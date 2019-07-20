import requests
import optparse
import bs4
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup, SoupStrainer
import json
import crayons
import colorama
import os
import re
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import pathlib
import sys


colorama.init()

parser = optparse.OptionParser()
parser.add_option("-t", "--target", help="please provide the target", dest="target")
parser.add_option("-f", "--file", help="please provide the file name", dest="filename")
options, args = parser.parse_args()
target = options.target
filename = options.filename

pastebin_url = []
github_content_urls = []
file = None
path = pathlib.Path(filename+".html")


if path.exists() == True:

	
	os.remove(filename+".html")

else:
	pass

file = open(filename+".html", 'a')
file.write("<title> pascan results </title> <center><h1>Pascan Results</h1></center > <h2>Introduction </h2> <p>Pascan is a script which automates the passive scan steps. This scan greps the data from Pastebins, Github, Gitlab. The tool will get update soon with more contents. </p><br><br><center><h1>TARGET - <font color='green'>%s</font></h1></center><br><br><br>"%target)
file.write("<center><h2>Pastebin data results for "+ '"'+target+'"' + "</h2></center><br><br>")


def info():

	print ("\n\n"+ crayons.green("NOTE: THIS SCRIPT WILL HELP TO FIND THE DATA IN PUBLIC SOURCES IN AUTOMATED WAY.\n\n"))

def pastebin_parse():
	r = requests.get('https://www.ask.com/web?o=0&l=dir&qo=serpSearchTopBox&q=pastebin.com+intext:%s'%target)
	soup = BeautifulSoup(r.content, "html.parser")

	for line in soup.findAll('p'):
		if line.has_attr('class'):
			if "PartialSearchResults-item-url" in line.get('class'):
				if 'pastebin.com' in line.text:

					pastebin_url.append('http://'+line.text)
	


def pastebin_main():


	if target:
		pastebin_parse()
		

	else:
		print ("Target parameter is missing.\n")
		print ("Ussage passive_recon -t targetname\n")



def github_parse():
	
	

	github_keywords = ['EMAIL Password', 'Api', 'SMTP', 'FTP', 'SSH', 'LDAP', 'SQL', 'Connection', 'PEM', 'private']

	github_access_token = '' #PLEASE ADD THE ACCESS TOKEN. 
	

	if github_access_token == "":
		print ("Please provide the github access token by signup to Github, then try again.")
		sys.exit(0)

	else:	

		url = "https://api.github.com/search/code?q=\"%s\"&access_token=%s" % (target, github_access_token)
		req = requests.get(url)
		result = req.json()

		if result.get('total_count') > 200:


			print ("\n[!]The mentions are big, so trying to find some keywords. \n")
			print ("\n Target: " + crayons.green("{0}".format(target)) +" Total Github code: "+  crayons.green('{0}'.format(result.get('total_count'))) +"\n")


			for keyword in github_keywords:
				searchTerm = target +' '+ keyword
				url = "https://api.github.com/search/code?q=%s&access_token=%s" % (searchTerm, github_access_token)
				
				try:

					r= requests.get(url)

					results = r.json()
					print ("\n SearchTerm:- ", crayons.green(searchTerm), " \t No. of Codes :- ", crayons.green(results.get('total_count')))
					print ("\n ", crayons.yellow("[+] Greping the URL's from codes.\n"))

					for indexes in range(0, 20):
						urlss = results.get('items')[indexes]['html_url']
						print ("\t", urlss)
						github_content_urls.append(urlss)

				except Exception as e:
					print ("\n[-] Can't find for this SearchTerm.\n")	

		else:

			pass

		


def github_requests(url):
	req = requests.get(url)
	soup = BeautifulSoup(req.content, 'html.parser')
	result = soup.find('table', class_="highlight tab-size js-file-line-container")
	
	
	contents = "<style> body {background: #d0d3d4; } </style> " + " Resource URL: " + '<a href='+url+'>' + url + '</a>'+ "<br><br><br><style> .div2 {width:700px;height: 400px; padding: 50px; overflow: scroll; border: 1px solid black; background: #a39a98;}</style><div class='div2'>" + str(result) + "</div><br><br><br><br>"
	
	file.write(contents)


def threaded_github():
	with ThreadPoolExecutor(max_workers =10) as pool:
		list(pool.map(github_requests, github_content_urls))


'''
def ask_data():

	url  = "https://www.ask.com/web?q=rediff+filetype%3Atxt&o=0&qo=homepageSearchBox"

	#PartialSearchResults-item-abstract

	req = requests.get()	


'''


def gitlab_parse():
	print ("\n " + crayons.yellow("[!] Now trying to find on Gitlab\n"))
	url ="https://gitlab.com/search?utf8=&search=%s&group_id=&project_id=&repository_ref=" %target	
	
	req = requests.get(url)
	
	soup = BeautifulSoup(req.content, 'html.parser')

	result = soup.find_all('li', ['d-flex project-row', 'd-flex no-description project-row'])

	if result == None:

		print ("\n "+Crayons.red("[-] Gitlab is Empty :(\n"))

	else:		

		file.write("<br><br><center><h2> Gitlab data results for %s </h2></center><br><br>"%target)

		for html in result:
			path = ""
			result2 =  html.find('span', ["project-name"]) # "d-flex align-items-center icon-wrapper stars has-tooltip"])
			anchor_tags = html.find('a', ["text-plain"])
			if anchor_tags.has_attr('href'):
				path = anchor_tags.get('href')
			project_name = result2.get_text()
			project_url = "https://gitlab.com/%s"%project_name
			print (crayons.green("Project name := ") + project_url)
			
			metadata = html.find('div', class_="description d-none d-sm-block append-right-default")
			print ("Metadata detecting :- " + str(metadata))
			if metadata != None:
				meta_data = metadata.get_text()
				print (crayons.yellow("\n\t Project's Metadata BELOW: ") )
				print (" \t ", meta_data)
				file.write("<font color='green'>Project Found </font>: <a href='{0}'>".format(project_url)+ str(project_name) +"</a><br><br><font color='Black'>Metadata-for-above-Project </font> : <font color='green' >"+ str(meta_data) +"</font><br><br><br><br>")
			else:

				file.write("<font color='green'>Project Found </font>: <a href='{0}'>".format(project_url)+ str(project_name) +"</a><br><br>")




if __name__ == '__main__':	
	
	info()
	

	print ("\n", crayons.yellow("[!] Starting from Pastebin search -----------------------------------------------\n"))
	
	pastebin_main()	 #pastebin search start here

	if pastebin_url:
		print (crayons.green("\t [+] Data found in Pastebin \n"))
		for url in pastebin_url:
			print  ("\t", url)
			file.write("<center><a href = " +url +'>'+ url + "</a></center><br>")

	else:
		print ("\n [-]Can not find in pastebin.\n")

	print ("\n "+ crayons.yellow("[!]Now looking in github for ------------------------------------------------ %s \n"%target))
	file.write("<br><br><center><h2>Github data results for "+ '"'+target+'"' + "</h2></center><br><br>")
	github_parse()

	print ("\n Grepping the contents from github code results \n")
	threaded_github()
	gitlab_parse()

	print ("\n\n All the information will be saved in file.\n\n.")
	file.close()
	




