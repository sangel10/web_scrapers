beatsinspace.net parser

//var matches = arrayOfLines[3].match(/<strong>([\s\S]+)<\/strong>\s*-*([\s\S]+)-+\s*<em>*/)


// there are multiple div.tracks
//for each set of divs

//var tracklist = $("div.tracks")[0].innerHTML


//break up lines into array
//var arrayOfLines = tracklist.match(/[^\r\n]+/g)




        

    //gets artist
var GetData = function(line){
    artist = "";
    title = "";
    re1 = /<strong>([\s\S]+)<\/strong>/;
    if (re1.test(line)){
        matches = re1.exec(line);
        artist = matches[1];
    }
    else{
        return;
    }
    // checks for em
    re2 = /-+\s*<em>*/;

    // everything between </strong> and "- <em>"
    re3 = /<\/strong>\s*-*([\s\S]+)-+\s*<em>*/;

    // everything after </strong> and before <br>
    re4 = /<\/strong>\s*-*([\s\S]+)<br>*/;
    
    //re5 = /<\/strong>\s*-*([\s\S]+)/

    // has an <em>
    if (re3.test(line)){
        matches = re3.exec(line);
        title = matches[1];
    }
    // has no <em>
    else{
        if (re4.test(line)){
            matches = re4.exec(line);
            title = matches[1];
        }
    }
    // else{
    //     matches = re5.exec(line)
    //     title = matches[1]
    // }
    
//    scrapedtracks[artist] = title;
    artist = artist.trim();
    artist = artist.replace(/-/g, "").replace(/'/g, "");
    title = title.trim();
    title = title.replace(/-/g, "").replace(/'/g, "");
    if (artist !== undefined && title !== undefined && artist !== null && title !== null && artist !== "" && title !== "" && artist!== "-" && title !== "-"){
            console.log("{'artist': '"+artist+"', 'title': '"+title+"', 'rank':"+0+"},");
    }
}


var tracklists = $("div.tracks");
//var scrapedtracks = [];


for (var i =0; i< tracklists.length; i++){
    var list = tracklists[i].innerHTML;
    //splits lines into array
    list = list.match(/[^\r\n]+/g);
    
    for (var j=0; j< list.length; j++){
        GetData(list[j]);
    }
}

