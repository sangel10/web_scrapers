/*
mixesdb parser

Either <ol> with or without [time], 

When tracklist is complete
<ol> with <li> elements, without number (provided by OL) but maybe with [time]

Tracklist incomplete

Div class = "list" <p> is a textblock with [time] "artist - track"

<ol> with [time]

*/

//works with [time]
regex  = /\[\d*\]?([\s\S]+)-+([\s\S]+)\[([\s\S]+)\]/
//can include or exclude [time]
/[\[\d*\]]?([\s\S]+)-+([\s\S]+)\[([\s\S]+)\]/

// works for both
regex = /[\[\d*\]]*([\s\S]+)-+([\s\S]+)\[([\s\S]+)\]/

//checks for [] at end
regex2 = /\[[\s\S]+\]$/

//starts with bracket?
regex3 = /^\[/
regex3.test(string)


processData = function(artist, title, notes){
	artist =  artist.trim();
	artist = artist.replace(/-/g, "").replace(/'/g, "");
	title = title.trim();
	title = title.replace(/-/g, "").replace(/'/g, "");
	if (notes !== undefined){
		notes.trim()
		notes = notes.replace(/-/g, "").replace(/'/g, "");
		if (artist !== undefined && title !== undefined && artist !== null && title !== null && artist !== "" && title !== "" && artist!== "-" && title !== "-" && notes !== null && notes !== "" && notes !== "-"){
            console.log("{'artist': '"+artist+"', 'title': '"+title+"', 'notes': '"+notes+"'},");
    	}
    }
    else if (artist !== undefined && title !== undefined && artist !== null && title !== null && artist !== "" && title !== "" && artist!== "-" && title !== "-"){
            console.log("{'artist': '"+artist+"', 'title': '"+title+"', 'rank':"+0+"},");
    }
}

scrape = function(line){
	regex = /[\[\d*\]]*([\s\S]+)-+([\s\S]+)\[([\s\S]+)\]/;
	//doesnt require last [match]
	regex2 = /[\[\d*\]]*([\s\S]+)-+([\s\S]+)/;
	if (regex.test(line) == true){
		var matches = regex.exec(line);
		var artist = matches[1];
		var title = matches[2];
		var notes = matches[3];
		processData(artist, title, notes);
	}
	else if (regex2.test(line) == true){
		var matches = regex2.exec(line);
		var artist = matches[1];
		var title = matches[2];
		processData(artist, title);
	}
}


unorderedScrape = function(tracklist){
	for (i=0; i< tracklist.length; i++){

		var check = tracklist[i];

		if (check !== undefined){
			tracks = tracklist[i].innerText;
			tracks = tracks.match(/[^\r\n]+/g);
			for (j = 0; j< tracks.length; j++){
				scrape(tracks[j]);
			}
		}
	}
}

orderedScrape = function(tracklist){
	for (i=0; i<tracklist.length; i++){
		track = tracklist[i].innerText;
		scrape(track);
	}

}

var tracks = $("#bodytext div.list p");
if (tracks.length !== 0){
	unorderedScrape(tracks);
}

var tracks = $("ol li");
if (tracks.length !== 0){
	orderedScrape(tracks);
}

