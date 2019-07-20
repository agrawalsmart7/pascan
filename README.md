# pascan

This script will retrieve the data from the sources like pastebin, github, gitlab and gives you the results in html file. This script tries to give you the github interface. This script is for automating the passive scan for your target, and gather all the data in one HTML file so that you can easily find the data by just searching the target name..

Note: This is in **development** mode. I will update it with more resources, but for now it works fine with these 3 resources. You should check. Its really make easy for finding and **searching** things.

 Requirement
===

* For retrieving the contents from Github, you need an access token and place that token to the variable "**github_access_token**". You can get the access token by sign up to github. 

* You need to download some libraries.<br>
`pip3 install -r requirement.txt`<br>
`pascan.py -t target -f file`

You must only give file name, by default it will give you the HTML file. 

Note: **You must change the file name in each run, if not did, then it will delete that file and create a new one by that name.**

Environment
====

Tested on python 3.7.3

Contact
====

Twitter [@agrawalsmart7](https://twitter.com/agrawalsmart7)
