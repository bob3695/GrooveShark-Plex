import grooveshark
TITLE = 'GrooveShark'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

URL_BASE = 'http://api.grooveshark.com/ws3.php?sig='

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

####################################################################################################

def Menu():
    grooveshark.init()
    grooveshark.authenticate_user('USERNAME', 'PASSWORD')
    test_string = JSON.StringFromObject(grooveshark.api_call('startAutoplayTag', {"tagID": 29}))
    #json_data = {'method': 'startSession', 'parameters': {}, 'header': {'wsKey': 'plex_richard', 'sessionID': ''}}


    #test_string = JSON.ObjectFromURL(URL_BASE + sig, json_data)
    #log.Info(JSON.StringFromObject(test_string))
    #test_string = "Hello"
    oc = ObjectContainer(
        objects = [
            DirectoryObject(
                key = Callback(TestMenu),
                title = test_string
            )#,
            #TrackObject(
            #    url = "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
            #    title = "Test Video"
            #)
        ]
    )

    return oc

####################################################################################################

def TestMenu():
    oc = ObjectContainer()

    return oc