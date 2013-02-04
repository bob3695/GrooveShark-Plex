import grooveshark
TITLE = 'GrooveShark'
ART = 'art-default.png'
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
            ),
            DirectoryObject(
                key = Callback(UserFavoriteSongsMenu),
                title = "Favorites"
            ),
            DirectoryObject(
                key = Callback(SearchMenu),
                title = "Search"
            )
        ]
    )

    return oc

####################################################################################################

def UserLibrarySongsMenu():
    oc = ObjectContainer(
        title1 = "Library - Songs"
    )

    songs = grooveshark.api_call('getUserLibrarySongs', {})

    for song in songs["result"]["songs"]:
        oc.add(GetTrack(song))

    return oc

####################################################################################################

def UserFavoriteSongsMenu():
    oc = ObjectContainer(
        title1 = "Favorite Songs"
    )

    songs = grooveshark.api_call('getUserFavoriteSongs', {})

    for song in songs["result"]["songs"]:
        oc.add(GetTrack(song))

    return oc

####################################################################################################

def SearchMenu():
    oc = ObjectContainer(
        title1 = "Search"
    )

    oc.add(InputDirectoryObject(key=Callback(SearchArtists), title="Artists...", prompt="Search for Artists"))

    return oc

####################################################################################################

def SearchArtists(query):
    oc = ObjectContainer(
        title1 = "Search - Artists"
    )

    artists =  grooveshark.api_call('getArtistSearchResults', {"query": query})

    for artist in artists["result"]["artists"]:
        oc.add(DirectoryObject(
            key = Callback(SearchArtists, query = query),       #ArtistID
            title = artist["ArtistName"]
        ))

    oc.add(DirectoryObject(
        key = Callback(SearchArtists, query = query),
        title = JSON.StringFromObject(artists)
    ))

    return oc

####################################################################################################

def GetTrack(song):
    coverUrl = ''
    if song["CoverArtFilename"] != None:
        coverUrl = song["CoverArtFilename"]

    track = TrackObject(
        key=Callback(GetTrack, song=song),
        rating_key=song['SongName'] + " - " + song["ArtistName"],
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

    return track

####################################################################################################

def PlayAudio(songID):
    COUNTRY_OBJECT = grooveshark.api_call('getCountry', {})["result"]
    stream_info = grooveshark.api_call('getSubscriberStreamKey', {"songID": songID, "country": COUNTRY_OBJECT})

    return Redirect(stream_info["result"]["url"])