import datetime
import urllib2
import json

today.strftime('%Y-%m-%d')
last_month.strftime('%Y-%m-%d')



releases_query = "https://musicbrainz.org/search?query=date%3A%5B2013-05-14+TO+2013-05-21%5D&type=release&limit=25&method=advanced"

lucine_query = "date:[2013-05-21 TO 2013-05-21]"

def check_musicbrainz():
	today = datetime.date.today()
	last_month = today - datetime.timedelta(days=30)
	end_date = today.strftime('%Y-%m-%d')
	start_date = last_month.strftime('%Y-%m-%d')
	offset = 0
	url = "http://www.musicbrainz.org/ws/2/release?&query=date:["+start_date+"%20TO%20"+end_date+"]&limit=100&fmt=json&offset="+str(offset)
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	return api_results


def get_musicbrainz_album_info(release):
	if release["id"]:
		mb_release_id = release["id"]
	if release["title"]:
		album_name = release["title"]
	if release["date"]:
		release_date = release["date"]
	album_artists = []
	if release["artist-credit"]:
		for entry in release["artist-credit"]:
			if entry["artist"]["name"]:
				artist = entry["artist"]["name"]
				album_artists.append(artist)
	labels = []
	catalog_ids = []
	if release["label-info"]:
		for entry in release["label-info"]:
			if entry["label"]["name"]:
				label = entry["label"]["name"]
				labels.append(label)
			if entry["catalog-number"]:
				catalog_id = entry["catalog-number"]
				catalog_ids.append(catalog_id)
	tracks = get_musicbrainz_album_tracks(mb_release_id)
	return {"mb_release_id":mb_release_id, "album_name":album_name, "album_artists":album_artists, 
	"release_date":release_date, "labels":labels, "catalog_ids":catalog_ids, "tracks":tracks}


def get_musicbrainz_album_tracks(mbid):
	url = "http://www.musicbrainz.org/ws/2/release/"+mbid+"?fmt=json&inc=recordings"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	tracks = []
	#return api_results
	for entry in api_results["media"][0]["tracks"]:
		length = entry["length"]
		title = entry["title"]
		mb_song_id = entry["recording"]["id"]
		track_number = entry["number"]
		track_artist = get_musicbrainz_track_artist(mb_song_id)
		tracks.append({"title":title, "length":length, "mb_song_id":mb_song_id, "track_number":track_number})
	return tracks

def get_musicbrainz_track_artist(mbid):
	url = "http://www.musicbrainz.org/ws/2/recording/"+mbid+"?fmt=json&inc=artists"
	data = urllib2.urlopen(url)
	api_results = json.load(data)
	artist = api_results["artist-credit"][0]["artist"]["name"]
	return artist 


release = "e3563aa1-7570-4d2d-9aa7-d1f18562b782"

