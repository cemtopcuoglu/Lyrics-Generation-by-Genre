from bs4 import BeautifulSoup
import urllib.request
import os
import re
from difflib import SequenceMatcher
from random import randint


BASE_URL = 'http://www.lyrics.com/'
PATH = 'custom.txt'

SONG_CAP = 100                            #The maximum number of songs that can be fetched from any artist

def SetSongCap(newSongCap):					#Sets the song cap
	global SONG_CAP
	
	SONG_CAP=newSongCap

	print("The song cap has been set to", SONG_CAP)


def SetPath(path):						#Sets the path where the data will be saved
	global PATH 

	PATH=path

	print("The file path has been set to", PATH)



def GetLyrics(*args):					#Fetches the lyrics of artists using search tags provided in *args

	totalSongCounter=0

	for searchTag in args:
		searchID = searchTag.replace(' ', '%20')
		
		searchURL=BASE_URL+'lyrics/' + searchID
		searchPage = urllib.request.urlopen(searchURL).read()
		searchSoup = BeautifulSoup(searchPage, 'html.parser')

		column = searchSoup.findAll('a')[80]

		artistName=column.text
		

		intermediateID=column['href']

		intermediateURL=BASE_URL+intermediateID
		intermediatePage = urllib.request.urlopen(intermediateURL).read()
		intermediateSoup = BeautifulSoup(intermediatePage, 'html.parser')

		column = intermediateSoup.findAll('a', string='A - Z')

		if (len(column)>0):
			artistID= column[0]['href']

		else:
			print("Failed to find artist using search tag:", searchTag)
			continue

		artistURL=BASE_URL+artistID
		artistPage = urllib.request.urlopen(artistURL).read()
		artistSoup = BeautifulSoup(artistPage, 'html.parser')

		column = artistSoup.findAll('tr')

		numOfSongs=len(column)

		print("Found artist,", artistName, ", using search tag,", searchTag, ". Number of songs:", numOfSongs-1)

		prevSong=''

		artistSongCounter=0

		upperLimit=randint(1, numOfSongs-1)          #Starting the fetching from a random position in the list

		for i in range(upperLimit, upperLimit+numOfSongs-1) :
			if (i==numOfSongs):
				continue
			currentSong=column[i%numOfSongs].findAll('a')[0].text
			print('Fetching song no.', totalSongCounter+1, 'titled,', currentSong, ', by artist,', artistName)
			if (SequenceMatcher(None, currentSong, prevSong).find_longest_match(0, len(currentSong), 0, len(prevSong)).size>5) and (i!=upperLimit):
				print('Song similar to previous song! Skipping....')   #this tries to minimise duplicates in the datasets, since there are
																		#multiple links with the same song titles/lyrics.
				prevSong=currentSong
				continue

			prevSong=currentSong
			songURL=BASE_URL+column[i%numOfSongs].findAll('a')[0]['href']

			songPage = urllib.request.urlopen(songURL).read()
			songSoup = BeautifulSoup(songPage, 'html.parser')

			textSoup = songSoup.findAll('pre')

			if (len(textSoup) > 0):
				lyrics=textSoup[0].get_text().strip()

				lyrics1=lyrics.replace('\r\n\r\n', '65')
				lyrics2=lyrics1.replace('\r\n', '\n')
				lyricsCleaned=lyrics2.replace('65', '\r\n')

				if len(lyricsCleaned) > 10:
					with open(PATH, 'a') as w:

						if not any(ord(char)>126 for char in lyricsCleaned):       #Rejecting a song if it contains any non-ASCII characters, to prevent
																					#undue complications in training
	
							w.write(lyricsCleaned+'\r\n')

							totalSongCounter=totalSongCounter+1
							artistSongCounter=artistSongCounter + 1
						
						else: 
							print('Song contains non-ASCII characters! Skipping....')  

			if (artistSongCounter>=SONG_CAP):
				break;



	print("Fetched a total of", totalSongCounter, "songs belonging to a total of", len(args), "artists (SONG_CAP =", SONG_CAP,")")


