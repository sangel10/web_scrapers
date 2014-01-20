
# from pyquery import PyQuery as pq

import inspect
from bs4 import BeautifulSoup
import urllib2
import pprint
import datetime
url = "http://www.residentadvisor.net/event.aspx?539451"
import json

def make_soup(url):
    #prints function name
    print inspect.stack()[0][3]
    data = urllib2.urlopen(url)
    soup = BeautifulSoup(data)
    return soup


def RA_event(url):

	# ## using pyquery
	# d = pq(url=url)
	# # title = d(".pt1.b.white").text()
	# # details = d("td.pb4.pr8")
	# # date = pq(details[0]).text()
	# # time = pq(details[1]).text()
	# # location = pq(details[2]).text()
	# # if " / " in location:
	# # 	venue, address = location.split(" / ",1)
	# # price = pq(details[3]).text()

	# descriptions = d(".grey.pb1")
	# for desc in descriptions:
	# 	# if d(desc).text() == 'Line-up /':
	# 	# 	lineUp = d(desc).parent().text()
	# 	# 	removed, lineUp = lineUp.split("/",1)

	# 	if d(desc).text() == 'Promoter /':
	# 		promoter = d(desc).parent().text()
	# 		removed, promoter = promoter.split("/",1)

	# 	if d(desc).text() == 'Promotional links /':
	# 		links = d(desc).parent().text()
	# 		removed, links = links.split("/",1)


	##using beautiful soup



	soup = make_soup(url)

	title = soup.find(class_= "pt1 b white").getText()


	details = soup.select("td.pb4.pr8")
	date = details[0].getText()
	
	from urlparse import urlparse
	from urlparse import parse_qs

	date_links = details[0].find_all("a")
	for date_link in date_links:
		link = date_link.attrs['href']
		parsed = urlparse(link)
		arguments = parse_qs(parsed.query)
		month = arguments['mn'][0]
		year = arguments['yr'][0]
		day = arguments['dy'][0]
		if date_links.index(date_link) == 0:
			start_date = {
				'year':year,
				'month':month,
				'day':day,
			}
			print "start_date", start_date
		elif date_links.index(date_link) == 1:
			end_date = {
				'year':year,
				'month':month,
				'day':day,
			}
			print "end_date", end_date

	


	time = details[1].getText()
	if "-" in time:
		start_time, end_time = time.split("-",1)
		start_time = start_time.strip()
		end_time = end_time.strip()
	location = details[2].getText()
	if "/ " in location:
		venue, address = location.split("/ ",1)

	price = details[3].getText()



	info = soup.find_all(class_= "pb1")
	for section in info:
		if section.getText() == 'Line-up /':
			parents = section.parent()
			lineUp = parents[1].getText()
			artists =lineUp.splitlines()
		if section.getText() == "Promoter /":
			promoter = section.find_parent().getText()
			removed, promoter = promoter.split("/",1)
		if section.getText() == 'Promotional links / ':
			# links = section.find_parent().getText()
			# removed, links = links.split("/",1)
			links = []
			anchors = section.find_parent().find_all("a")
			for a in anchors:
				link = a.attrs['href']
				links.append(link)





	tds = soup.find_all("td")
	main = tds[33]
	if main.has_attr("id") and main.attrs['id'] == "_contentmain_ucAddTicket_Quantity":
		ticketed = True
		main = tds[36]

	else:
		ticketed = False
	images = main.find_all("img")
	image_srcs = []
	for img in images:	
		src = img.attrs['src']
		src = 'http://www.residentadvisor.net' + src
		image_srcs.append(src)

	try:
		description = soup.find(class_="pt8 pb8").getText()
		# description = soup.select("div.pt8.pb8")[0].getText()
	except Exception, e:
		print e
		description =""
		print "no description"


	event_info = {
		'title':title,
		'date':date,
		'time':time,
		'location':location,
		'price':price,
		'artists':artists,
		'image_srcs':image_srcs,
		'description': description,
		'RA_ticketed':ticketed,
	}

	try:
		event_info['promoter'] = promoter
	except:
		print "no Promoter"
	try:
		event_info['links'] = links
	except:
		print "no links"
	try:
		event_info['venue'] = venue
	except:
		print "no venue"
	try: 
		event_info['address'] = address
	except:
		print "no address"
	try:
		event_info['start_date'] = start_date
	except:
		print "no start date"
	try:
		event_info['end_date'] = end_date
	except NameError:
		if start_time and end_time:
			end_time_float = float(end_time.replace(":","."))
			start_time_float = float(start_time.replace(":","."))
			# end_time = float(end_time)
			# start_time = float(start_time)

			#if the end time is the same or earlier as the start time, 
			#and there is no end-date given, assume it ends the next day
			if end_time <= start_time:
				month = event_info['start_date']['month']
				year = event_info['start_date']['year']
				day = event_info['start_date']['day']
				start_date = datetime.datetime(int(year), int(month), int(day))
				end_date = start_date + datetime.timedelta(days=1)
				end_date = {
					'day': end_date.day,
					'month':end_date.month,
					'year': end_date.year,
				}
				event_info['end_date'] = end_date


			# if the endtime is later than the start time and only one date is give, assume the event takes placae
			# over the course of one day
			elif end_time > start_time:
				end_date = start_date

	except:
		print "no end_date"
	try:
		event_info['start_time'] = start_time
	except:
		print "no start time"
	try:
		event_info['end_time'] = end_time

	except:
		print "no end time"	

	# pprint.pprint(event_info)
	# return json.dumps(event_info)
	return event_info


