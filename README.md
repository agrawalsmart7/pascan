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

What data it collects?
========

From pastebin, it collects if some credentials are there?, or some mentions, it uses ask search engine for that. (Yes will improve it later but it work fine for now. :).

From github, it search for keyterms like **'EMAIL Password', 'Api', 'SMTP', 'FTP', 'SSH', 'LDAP', 'SQL', 'Connection', 'PEM', 'private'** and collects the file and the **FILE DATA** and save them into one html file. It collects 20 urls from each keywords you can change it according to your need by changin the value of `range(0, 20)` at line 113.

From gitlab, it search only by the name and collects the project name and **metadata** so that you will have an idea about what this project based on.


Environment
====

Tested on python 3.7.3

Contact
====

Twitter [@agrawalsmart7](https://twitter.com/agrawalsmart7)
