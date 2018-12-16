LyricsFetcher.py
	1) Type -> python 
	2) import LyricsFetch as If 
	3) If.GetLyrics(‘artist1 ’,’artist2 ‘)
	   a) You can provide as many artist as you want
	   b)But there is fixed upper limit for each artist. You can change it with 		     SetSongCap(newSongCap)  function.
      	4) This will create a “custom.txt“ which has the lyrics of the artists.
	
generator.py 
	1) Type -> python generator.py  genre  temperature  starting-sentence
	    a) genre : 
		i)  Genre can be chosen one of the given genres by us      				   (blues,rap,metal,rock,rb,country)
		ii) Or you can put “custom” one
	    b) temperature :
		i) You can change temperature
	    c) starting-sentence :
		i) You can change starting-sentence in the model but this should be length of 40 char.
