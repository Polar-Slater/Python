import urllib.request
import json    
    
def main():
    uid = input("Please enter the UID: ")
    urlData = "http://api.bilibili.com/x/relation/stat?vmid=" + str(uid)
    webUrl = urllib.request.urlopen(urlData)
#    print("result code: " + str(webUrl.getcode()))
    if (webUrl.getcode() == 200):
        data = webUrl.read().decode("utf-8")
        theJson = json.loads(data)
        if "follower" in theJson["data"]:
            print("UID " + uid + " has %d followers " % theJson["data"]["follower"] + "and is following %d people" % theJson["data"]["following"])

    else:
        print("Received an error from the server, cannot retrive rasules " + str(webUrl.getcode()))
    input("Press Enter to exit.")

if __name__ == "__main__":
    main()