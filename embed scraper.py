import urllib2
import lxml 
from bs4 import BeautifulSoup
import json
from pprint import pprint

url = 'http://www.factmag.com/2013/04/05/download-major-lazers-fourth-lazer-strikes-back-ep/'
client_id = "a0b4638bae6d50a9296f7fc3f35442eb"

# last.fm
last_fm_api_key = "c43db4e93f7608bb10d96fa5f69a74a1"
# Secret: is e93504ee9bad8ec5966d1db1f26a4cd0

echo_nest_API_key = "FBHCMLQRHBCWD8GVA"

def make_soup(url):
	data = urllib2.urlopen(url)
	soup = BeautifulSoup(data)
	return soup

def find_soundcloud(soup):
	results = []
	iframes = soup.find_all("iframe")
	for frame in iframes:
		src = frame.get("src")
		if src.find("soundcloud") != -1:
			src = src.split("?")[1]
			if src.find("playlists")!= -1:
				src = src.split("playlists%2F")[1]
				src = src.split("&")[0]
				src = src.split("%3F")[0]
				results.append({"type":"playlist", "link":src})
			if src.find("tracks")!= -1:
				src = src.split("tracks%2F")[1]
				src = src.split("&")[0]
				src = src.split("%3F")[0]
				results.append({"type":"track", "link":src})
	return results

def find_youtube(soup):
	results = []
	iframes = soup.find_all("iframe")
	for frame in iframes:
		src = frame.get("src")
		if src.find("youtube") != -1:
			if src.find("list") != -1:
				src = src.split("list=")[1]
				src = src.split("&amp")[0]
				src = src.split("&")[0]
				results.append({"type":"playlist", "link":src})
			else:
				src =src.split("embed/")[1]
				src = src.split("?")[0]
				results.append({"type":"track","link":src})
	objs = soup.find_all("object")
	for o in objs:
		src = o.get("src")
		if src.find("youtube") != -1:
			src =src.split("/v/")[1]
			src = src.split("?")[0]
			results.append({"type": track, "link":src})
	return results

def find_vimeo(soup):
	results = []
	iframes = soup.find_all("iframe")
	for frame in iframes:
		src = frame.get("src")
		if src.find("player.vimeo") != -1:
			src = src.split("video/")[1]
			src = src.split("?")[0]
			results.append({"type":"track", "link":src})
	return results

def get_vimeo_track(track_id):
	track_id = str(track_id)
	vimeo_url = "http://vimeo.com/api/v2/video/"+track_id+".json"
	track_data = urllib2.urlopen(vimeo_url)
	track_data = json.load(track_data)
	track_dict = process_vimeo_track(track_data)
	return track_dict
	#return track_data

def process_vimeo_track(track_data):
	title = track_data[0]["title"]
	user_name = track_data[0]["user_name"]
	track_id = track_data[0]["id"]
	track_dict = {"title":title, "user_name":user_name, "track_id":track_id}
	return track_dict


def get_SC_track(track_id):
	track_id = str(track_id)
	#client_id = "a0b4638bae6d50a9296f7fc3f35442eb"
	SC_track_url = "http://api.soundcloud.com/tracks/"+track_id+".json?client_id="+client_id
	track_data = urllib2.urlopen(SC_track_url)
	track_data = json.load(track_data)
	track_dict = process_SC_track(track_data)
	return track_dict

#separated retrieving data from the API and processing the data in order to 
#have data processing form a single track and from multiple playlist entries all in one function

def process_SC_track(track_data):
	title = track_data["title"]
	user_id = track_data["user"]["id"]
	track_id = track_data["id"]
	track_dict = {"title": title, "track_id": track_id}
	user_data = get_SC_user(user_id)
	track_dict.update(user_data)
	return track_dict

def get_SC_user(user_id):
	user_id = str(user_id)	
	#client_id = "a0b4638bae6d50a9296f7fc3f35442eb"
	SC_user_url = "http://api.soundcloud.com/users/"+user_id+".json?client_id="+client_id
	user_data = urllib2.urlopen(SC_user_url)
	user_data = json.load(user_data)
	username = user_data["username"]
	full_name = user_data["full_name"]
	return {"username": username, "full_name": full_name}

def get_SC_playlist(playlist_id):
	playlist_id = str(playlist_id)
	#client_id = "a0b4638bae6d50a9296f7fc3f35442eb"
	SC_playlist_url = "http://api.soundcloud.com/playlists/"+playlist_id+".json?client_id="+client_id
	playlist_data = urllib2.urlopen(SC_playlist_url)
	playlist_data = json.load(playlist_data)
	SCtracks =[]
	#return playlist_data
	for track in playlist_data["tracks"]:
		track_dict = process_SC_track(track)
		SCtracks.append(track_dict)
	return SCtracks


def get_YT_track(track_id):
	url = "https://gdata.youtube.com/feeds/api/videos/"+track_id+"?v=2&alt=json"
	track_data = urllib2.urlopen(url)
	track_data = json.load(track_data)
	entry = track_data["entry"]
	title = get_YT_title(entry)
	return title

#separated retrieving data from the API and processing the data in order to 
#have data processing form a single track and from multiple playlist entries all in one function

def get_YT_title(entry):
	title = entry["title"]["$t"]
	return title

def get_YT_playlist(playlist_id):
	url = "https://gdata.youtube.com/feeds/api/playlists/"+playlist_id+"?v=2&alt=json"
	playlist_data = urllib2.urlopen(url)
	playlist_data = json.load(playlist_data)
	entries = playlist_data["feed"]["entry"]
	tracks = []
	for entry in entries:
		title = entry["title"]["$t"]
		tracks.append(title)
	return tracks

def scrape(url):
	YT = []
	SC = []	
	soup = make_soup(url)
	SC = find_soundcloud(soup)
	YT = find_youtube(soup)
	vimeo = find_vimeo(soup)
	SCresults = []
	YTresults = []
	Vresults = []
	results = []
	for track in vimeo:
		if track["type"] == "track":
			data = get_vimeo_track(track["link"])
			Vresults.append(data)
	for track in SC:
		if track["type"] == "playlist":
			data = get_SC_playlist(track["link"])
			SCresults.append(data)
		if track["type"] == "track":
			data = get_SC_track(track["link"])
			SCresults.append(data)
	for track in YT:
		if track["type"] == "playlist":
			data = get_YT_playlist(track["link"])
			YTresults.append(data)
		if track["type"] == "track":
			data = get_YT_track(track["link"])
			YTresults.append(data)
	results.append({"Vimeo Tracks":Vresults})
	results.append({"SC Tracks":SCresults})
	results.append({"YT Tracks":YTresults})
	return results
	#return {"SC Links":SC,"YT Links": YT}

def check_lastfm(slug):
	slug = slug.encode("utf8")
	slug = urllib2.quote(slug) 
	url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track="+slug+"&api_key="+last_fm_api_key+"&format=json"
	data = urllib2.urlopen(url)
	data = json.load(data)
	return data

def extract(slug):
	slug = slug.encode("utf8")
	slug = urllib2.quote(slug)
	url = "http://developer.echonest.com/api/v4/artist/extract?api_key="+echo_nest_API_key+"&format=json&text="+slug+"&results=10"
	data = urllib2.urlopen(url)
	data = json.load(data)
	return data

soup = make_soup(url)
scrape(url)



<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F82195284"></iframe>


<iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Fplaylists%2F639839"></iframe>


https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Fplaylists%2F4681384%3Fsecret_token%3Ds-NZVkr
<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F87172296&secret_token=s-NZVkr"></iframe>

<embed id="video-player" height="100%" width="100%" tabindex="0" type="application/x-shockwave-flash" src="http://s.ytimg.com/yts/swfbin/watch_as3-vfl5qlEPI.swf" allowscriptaccess="always" bgcolor="#000000" allowfullscreen="true" flashvars="list=PLIOK0_bYXe1qcB3QATgC5pwAZccRXbFZq&amp;sendtmp=1&amp;is_html5_mobile_device=false&amp;playlist_module=http%3A%2F%2Fs.ytimg.com%2Fyts%2Fswfbin%2Fplaylist_module-vflzGeMnk.swf&amp;eurl=http%3A%2F%2Fsheblogsaboutmusic.wordpress.com%2F2013%2F02%2F28%2Fctm-saul-yum%2F&amp;probably_logged_in=1&amp;rel=1&amp;length_seconds=95&amp;enablejsapi=1&amp;iurl=http%3A%2F%2Fi3.ytimg.com%2Fvi%2FJp6KpQBUaNw%2Fhqdefault.jpg&amp;video_id=Jp6KpQBUaNw&amp;el=embedded&amp;allow_ratings=1&amp;title=CTM%20-%20Variations&amp;hl=en_US&amp;avg_rating=5&amp;share_icons=http%3A%2F%2Fs.ytimg.com%2Fyts%2Fswfbin%2Fsharing-vflsBOuhL.swf&amp;iurlsd=http%3A%2F%2Fi3.ytimg.com%2Fvi%2FJp6KpQBUaNw%2Fsddefault.jpg&amp;playlist_length=3&amp;user_display_name=santiagoangel10&amp;playlist_title=CTM&amp;user_display_image=https%3A%2F%2Fs.ytimg.com%2Fyts%2Fimg%2Fsilhouette32-vflu0yzhs.png&amp;cr=AU&amp;fexp=930900%2C932000%2C932004%2C906383%2C916910%2C902000%2C901208%2C919512%2C929903%2C925714%2C931202%2C900821%2C900823%2C931203%2C906090%2C909419%2C908529%2C930807%2C919373%2C930803%2C906836%2C920201%2C929602%2C930101%2C926403%2C900824%2C910223&amp;allow_embed=1&amp;view_count=4277&amp;sk=KzzRcNBG6ZLCHZCupVWHRJPBXx1FEoYMC&amp;jsapicallback=ytPlayerOnYouTubePlayerReady&amp;playerapiid=player1&amp;framer=http%3A%2F%2Fsheblogsaboutmusic.wordpress.com%2F2013%2F02%2F28%2Fctm-saul-yum%2F">


def showNext(i, scripts):
	i = i
	i+=1
	return scripts[i]



