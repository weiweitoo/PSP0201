# Methods Module, add all the general methods here
import os
import json
import Tkinter
import urllib2
import urllib


def loopList(items):
	for i in items:
		print i

def centerWindow(root):
	root.withdraw()
	root.update_idletasks()  # Update "requested size" from geometry manager

	x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
	y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
	root.geometry("+%d+%d" % (x, y))
	root.deiconify()

def locateFile(filename):
        DATA_DIR = "data/" + filename
        current_dir = os.path.dirname(__file__)
        temp_path = os.path.dirname(current_dir) + '/'
        
        return temp_path + DATA_DIR


def readData(filename):
        requestedFile = locateFile(filename)
        if requestedFile.endswith(".json"):
            print "hi"
            with open(requestedFile, "r") as jsonFile:
                try:
                    data = json.load(jsonFile)
                except ValueError:
                    data = {}
            return data
        else:
            return requestedFile

def writeData(data, filename):
        json_file = locateFile(filename)
        with open(json_file, "w") as outfile:
                json.dump(data, outfile)

def defineWindow(title = "AskTrivia", geometry = "640x480"):
        window = Tkinter.Tk()
        window.title(title)
        window.update_idletasks()
        coordinates = geometry.split("x")
        width = int(coordinates[0])
        height = int(coordinates[1])
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        geometry = ("{}+{}+{}".format(geometry,x,y))
        window.geometry(geometry)
        return window

def backupQuestions():
        categorynum = {"Random":9,"Books":10,"Film":11,"Music":12,"Musicals & Theatres":13,"Television":14,"Video Games":15,"Board Games":16,
               "Science & Nature":17,"Computers":18,"Mathematics":19,"Mythology":20,"Sports":21,"Geography":22,"History":23,"Politics":24,"Art":25,
               "Celebrities":26,"Animals":27,"Vehicles":28,"Comics":29,"Gadgets":30,"Japanese Anime & Manga":31,"Cartoon & Animations":32}

        quantities = [5, 10, 15, 20]

        obj = {}

        for i in categorynum:
                category = categorynum[i]
                obj[category] = {}

                for quantity in quantities: 
                        url = "https://opentdb.com/api.php?amount="+ str(quantity) +"&category=" + str(category)
                        response = urllib.urlopen(url)
                        jsonData = json.loads(response.read())
                        results = jsonData["results"]
                        obj[category][quantity] = results
                        print "added", category, quantity

        with open('data/backup.json', 'w') as outfile:
                json.dump(obj, outfile)

def readRemoteJson(url):
    url = "http://52.36.70.190:5002/" + str(url)
    error = 0;

    print "Trying"

    try:
     # Send a HTTP request to url
     response = urllib.urlopen(url)
     try:
        # If the request did not fail, load the JSON data returned from the url
        data = json.loads(response.read())
        # Check if there are errors ( most likely caused if there are no data at all in database )
        if ( "error" in data and data["error"] ):
            # If there are errors, return None instead of False so we can differentiate the failure when calling this function
            return None;
     except:
        # If there was any sort of error, set error = 1
        error = 1;
    except:
     # If there was any sort of error, set error = 1
     error = 1;


    if ( error == 1 ) :
        return False;
    else:
        return data;

def postRemote(path, params):
    url = "http://52.36.70.190:5002/" + path + "/"
    # Converts parms{} into a series of key=value pairs to create a sucessful POST request. Eg: {key1: value1, key2:value2} => "key1=value1&key2=value2"
    data = urllib.urlencode(params)
    try:
        # Create an URL request
        req = urllib2.Request(url, data)
        # Opens the URL, the output is a file-like object
        response = urllib2.urlopen(req)
        # Calling the .read() method of urlopen returns the content of requested URL ( most likely a string )
        return response.read()
    except:
        return None;

def getUserData(session_id):
    # If sending a POST request to user/ with session_id succeeded:
    if (postRemote("user", {"id" : session_id}) != None) :
        # Send a POST request to grab user's data
        data = postRemote("user", {"id" : session_id})
        # Return a Dictionary from JSON object
        return json.loads(data);
    else:
        # If failed, just read the local users.json file
        data = readData("users.json");
        return data[str(session_id)];

#URLRequest("http://localhost:5002/adduser/", { "name" : "prevwong", "password" : "imgeneva", "description" : "Hello world!" })

#print URLRequest("http://localhost:5002/usernames/", {})
