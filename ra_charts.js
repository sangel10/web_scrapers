//RA DJ Charts Parser


<script src="http://code.jquery.com/jquery-latest.min.js" type="text/javascript"></script>

<script> 

var rows = $("table #tracks tr");

var FirstTrack = function(rows){
	var artist = rows[3].children[0].children[0].innerText;
	artist = artist.replace(/(\r\n|\n|\r)/gm," ");
	artist = $.trim(artist);
	var title = rows[3].children[1].innerText;
	title = title.replace(/(\r\n|\n|\r)/gm," ")
	title = $.trim(title);
	if (artist !== undefined && title !== undefined && artist !== null && title !== null && artist !== "" && title !== "" && artist!== "-" && title !== "-"){
            console.log("{'artist': '"+artist+"', 'title': '"+title+"', 'rank':"+0+"},");
    }
}

var OtherTracks = function(rows){
	for (i=5; i < rows.length; i++){
		if (rows[i].children[3] !== undefined){
			artist = rows[i].children[2].children[0].innerText;
			artist = artist.replace(/(\r\n|\n|\r)/gm," ");
			artist = $.trim(artist);
			title = rows[i].children[3].innerText;
			title = title.replace(/(\r\n|\n|\r)/gm," ")
			title = $.trim(title);
			if (artist !== undefined && title !== undefined && artist !== null && title !== null && artist !== "" && title !== "" && artist!== "-" && title !== "-"){
	        	console.log("{'artist': '"+artist+"', 'title': '"+title+"', 'rank':"+0+"},");
        }
        }
	}
}

FirstTrack(rows);
OtherTracks(rows);
