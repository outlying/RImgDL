#!./.env/bin/python3.7

import getopt, sys
import feedparser
import re
import datetime
import time
import urllib.request

# read commandline arguments, first
fullCmdArguments = sys.argv
# - further arguments
argumentList = fullCmdArguments[1:]

unixOptions = "r:l"
gnuOptions = ["reddit=", "loop"]

try:
	arguments, values = getopt.getopt(argumentList, unixOptions, gnuOptions)
except getopt.error as err:
	# output error, and return with an error code
	print (str(err))
	sys.exit(2)

loopMode = False

for currentArgument, currentValue in arguments:
	if currentArgument in ("-r", "--reddit"):
		redditRss = currentValue
	elif currentArgument in ("-l", "--loop"):
		loopMode = True

assert(redditRss is not None), "Reddit URL is missing"

print(redditRss)


while True:
	feed = feedparser.parse(redditRss)

	for item in feed.entries:
		id = re.split('/', item.id)[-1]
		dateTimeObject = datetime.datetime.strptime(item.updated, '%Y-%m-%dT%H:%M:%S%z')
		timestamp = '{0:%Y%m%d%H%M%S}'.format(dateTimeObject)
		content = item.content[0].value
		match = re.search('href="(http[^>]+?\.jpg)"', content)

		if match:
			url = match.group(1)
			print("ID: " + id + "\t\t" + timestamp + "\t\t" + url)
			urllib.request.urlretrieve(url, timestamp + "_" + id + ".jpg")

	if loopMode:
		time.sleep(60 * 60 * 6) # Every 6 hours
	else:
		break
