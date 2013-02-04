import grooveshark
TITLE = 'GrooveShark'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler('/music/grooveshark', Menu, TITLE, ICON, ART)
    #Plugin.AddViewGroup("InfoList", viewMode = "InfoList", mediaType = "items")
    Plugin.AddViewGroup("List", viewMode = "List", mediaType = "items")

    ObjectContainer.title1 = TITLE
    ObjectContainer.art = R(ART)
    ObjectContainer.view_group = 'List'

    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)
    #VideoClipObject.thumb = R(ICON)

    grooveshark.init()
    grooveshark.authenticate_user(Prefs["Username"], Prefs["Password"])

####################################################################################################

def Menu():
    oc = ObjectContainer(
        objects = [
            DirectoryObject(
                key = Callback(UserLibrarySongsMenu),
                title = "Library"
            )
        ]
    )

    return oc



    #stream_info = grooveshark.api_call('getSubscriberStreamKey', {"songID": 1826242, "country": COUNTRY_OBJECT})
    #test_string = JSON.StringFromObject(stream_info)
    #json_data = {'method': 'startSession', 'parameters': {}, 'header': {'wsKey': 'plex_richard', 'sessionID': ''}}

    #test_string = JSON.ObjectFromURL(URL_BASE + sig, json_data)
    #log.Info(JSON.StringFromObject(test_string))
    #test_string = "Hello"

    #track = TrackObject(
    #    url = "http://groovshark.com",
    #    title = "Test Song",
    #    artist = "Test Artist",
    #    thumb = "http://images.gs-cdn.net/static/albums/120_2467142.jpg"# + songInfo["result"]["songs"][0]["CoverArtFilename"]
    #)

    #media = MediaObject(
    #    container = "mp3",
    #    audio_codec = "mp3"
    #)

    #media.add(PartObject(key=Callback(PlayAudio, url=stream_info["result"]["url"], ext='mp3')))

    #track.add(media)

    #oc = ObjectContainer(
    #    objects = [
    #        DirectoryObject(
    #            key = Callback(TestMenu),
    #            title = Prefs["Username"]
    #        ),
    #        track
    #,
    #TrackObject(
    #    url = "http://stream79b.grooveshark.com/stream.php?streamKey=f627168c08b88485ef896024f2da14b0afc802a6_510879ff_1bddc2_160d8ea_b491dd49_8_0",
    #    title = "Test Video"
    #)
    #    ]
    #)

    #return oc

####################################################################################################

def UserLibrarySongsMenu():
    oc = ObjectContainer(
        title1 = "Songs"
    )

    songs = grooveshark.api_call('getUserLibrarySongs', {})
    i = 0
    for song in songs["result"]["songs"]:
        coverUrl = ''
        if song["CoverArtFilename"] != None:
            coverUrl = song["CoverArtFilename"]

        oc.add(
            TrackObject(
                url = "http://groovshark.com/" + str(i),
                title = song["SongName"],
                artist = song["ArtistName"],
                thumb = "http://images.gs-cdn.net/static/albums/" + coverUrl,
                items = [
                    MediaObject(
                        container = "mp3",
                        audio_codec = "mp3",
                        parts = [
                            PartObject(
                                key=Callback(PlayAudio, songID=song["SongID"], ext='mp3')
                            )
                        ]
                    )
                ]
            )
        )
        Log.Info(i)
        i += 1

        #track = TrackObject(
        #    url = "http://groovshark.com",
        #    title = song["SongName"],
        #    artist = song["ArtistName"],
        #    thumb = "http://images.gs-cdn.net/static/albums/120_2467142.jpg"# + songInfo["result"]["songs"][0]["CoverArtFilename"]
        #)

        #media = MediaObject(
        #    container = "mp3",
        #    audio_codec = "mp3"
        #)

        #media.add(PartObject(key=Callback(PlayAudio, songID=song["SongID"], ext='mp3')))
        #track.add(media)

        #oc.add(track)
        #oc.add(DirectoryObject(
        #    key = Callback(PlaySong, songID = song["SongID"]),
        #    title = song["SongName"] + " - " + song["ArtistName"]
        #))

    return oc

def PlaySong(songID):
    return ''
#    track = TrackObject(
#        url = "http://groovshark.com",
#        title = "Test Song",
#        artist = "Test Artist",
#        thumb = "http://images.gs-cdn.net/static/albums/120_2467142.jpg"# + songInfo["result"]["songs"][0]["CoverArtFilename"]
#    )

#    media = MediaObject(
#        container = "mp3",
#        audio_codec = "mp3"
#    )

#    media.add(PartObject(key=Callback(PlayAudio, songID=songID, ext='mp3')))

#    track.add(media)
#    return track

def PlayAudio(songID):
    COUNTRY_OBJECT = grooveshark.api_call('getCountry', {})["result"]
    stream_info = grooveshark.api_call('getSubscriberStreamKey', {"songID": songID, "country": COUNTRY_OBJECT})

    return Redirect(stream_info["result"]["url"])