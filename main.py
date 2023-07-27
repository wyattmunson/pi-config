import subprocess
import re
import time

# INTRO MESSAGE
def introMessage():
    print("WELCOME TO WAS")
    print("")
    print("           .---.   ,---,       .--.--.    ")
    print("          /. ./|  '  .' \     /  /    '.  ")
    print("      .--'.  ' ; /  ;    '.  |  :  /`. /  ")
    print("     /__./ \ : |:  :       \ ;  |  |--`   ")
    print(" .--'.  '   \' .:  |   /\   \|  :  ;_     ")
    print("/___/ \ |    ' '|  :  ' ;.   :\  \    `.  ")
    print(";   \  \;      :|  |  ;/  \   \`----.   \ ")
    print(" \   ;  `      |'  :  | \  \ ,'__ \  \  | ")
    print("  .   \    .\  ;|  |  '  '--' /  /`--'  / ")
    print("   \   \   ' \ ||  :  :      '--'.     /  ")
    print("    :   '  |--' |  | ,'        `--'---'   ")
    print("     \   \ ;    `--''                     ")
    print("      '---'                               ")
    print("")
                                          


    print("AUTO STARTER LOADING IN 5 SECONDS...")
    print("Interrupt the Auto Starter with [CTRL] + [C]")
    print("")
    time.sleep(5)

# introMessage()

fullConfigMap = {
    "deps/git/check": {
        "topic": "install/verify/git",
        "command": ["git --version"],
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    },
    "deps/git/install": {
        "command": "sudo apt-get install git -y",
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    },
    "deps/docker/check": {
        "topic": "install/verify/docker",
        "command": ["docker --version"],
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    },
    "deps/docker/install": {
        "command": ["sudo sh install-docker.sh"],
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    },
    "deps/tiki/check": {
        "topic": "install/verify/docker",
        "command": ["tiki --version"],
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    }
}

fullTopicList = [
    "deps/git/check",
    "deps/git/install",
    "deps/git/upgrade",
    "deps/docker/check",
    "deps/tiki/check"
]

# installHeadlines = []

class Warden:
    def __init__(self, fullTopicList):
        self.fullTopicList = fullTopicList
        self.deps = None
    
    def splitCommandString(self, string):
        # split into array if not already array type
        # certain commands have combined strings
        if type(string) == list:
            commandArray = string
        else:
            commandArray = string.split(" ")

            for x in range(len(commandArray)):
                commandArray[x] = commandArray[x].strip()
    
        return commandArray


    def runCommand(self, commandArray):
        print("Running command:", commandArray)
        command = subprocess.run(commandArray, capture_output=True, text=True, shell=True)
        print("Got command response:", command)
        return command


    def runCommandWithCheck(self, obj):
        commandArray = self.splitCommandString(obj["command"])
        command = self.runCommand(commandArray)

        # Check for failure
        if obj["failure"] == "returncode":
            if obj["failureValue"] == "nonzero" and command.returncode > 0:
                print("FAILED: ", obj["topic"])
                return False

        # Check for true, warn when failure or success not detected
        if obj["success"] == "returncode":
            if obj["successValue"] == 0 and command.returncode == 0:
                print("SUCCESS: ", obj["topic"])
                return True

        # success not detected, returning True for now
        print("WARN: did not meet success or failure criteria for:", obj["topic"])

    # START OF INSTALL SCRIPTS
    def installGithubCli():
        pass
    # END OF INSTALL SCRIPTS

    # CHECK PACKAGE
    def checkPackage(self, headline):
        # Check to see if a package was installed
        config = fullConfigMap[headline]
        return self.runCommandWithCheck(config)

    def installPackage(self, headline):
        print("Package installing...")
        config = fullConfigMap[headline]
        return self.runCommandWithCheck(config)
    

    def aptGetUpdate(self):
        print("INFO", "Updating apt-get")
        subprocess.run(["sudo", "apt-get", "update"])

    def processDeps(self):
        print("Processing deps...")
        uniqueTopics = []
        for topic in self.fullTopicList:
            match = re.match(r"deps/\w+/check$", topic)
            if match:
                if topic not in uniqueTopics:
                    uniqueTopics.append(topic)
        print("ALL TOPICS", uniqueTopics)
        self.deps = uniqueTopics

        for x in uniqueTopics:
            print("\n=== CHECKING ===", x)
            isInstalled = self.checkPackage(x)
            print("Is installed:", isInstalled)
            if not isInstalled:
                # Get install headline
                splitHeadline = x.split("/")[0:2]
                installHeadline = "/".join(splitHeadline)

                installSuccessful = self.installPackage(installHeadline)
                if installSuccessful:
                    print("Installed succesfully")
                else:
                    print("Failed to install")
    


warden = Warden(fullTopicList)
warden.processDeps()


def mainRunner():
    print("HELLO")


# returnCode = subprocess.call(["git", "--version"])
# print(returnCode)
# oldeste = subprocess.run(["gitt", "--version"], shell=True)
# print("OD", oldeste)
# print("DOING SUBPROCESS")
# returnCode2 = subprocess.run(["git", "--version"], capture_output=True, text=True)
# print("SUBPROCESS RAN, OUTPUT BELOW")
# print(returnCode2)
# print("ARGS     :", returnCode2.args)
# print("RES CODE :", returnCode2.returncode)

def splitCommandString(string):
    # split into array if not already array type
    # certain commands have combined strings
    if type(string) == list:
        commandArray = string
    else:
        commandArray = string.split(" ")
    
        for x in range(len(commandArray)):
            commandArray[x] = commandArray[x].strip()
    
    return commandArray

def runCommand(commandArray):
    # command = splitCommandString(string)
    # print("COMMAND ARRAY", command)
    # subprocess.run(command)
    print("Running command:", commandArray)
    command = subprocess.run(commandArray, capture_output=True, text=True, shell=True)
    print("Got command response:", command)
    return command


cmdList = [
    {
        "topic": "install/verify/git",
        "command": ["git --version"],
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    },
    {
        "topic": "install/verify/docker",
        "command": ["docker --version"],
        "success": "returncode",
        "successValue": 0,
        "failure": "returncode",
        "failureValue": "nonzero"
    }
]

def extractVersionNumber(versionString): 
    # returns version number for n.n.n format
    match = re.match(r"^(\d+)(\.\d+)(\.\d+)?$", versionString)
    if match:
        return match.group(0)
    else:
        return None

def runCommandWithCheck(obj):
    commandArray = splitCommandString(obj["command"])
    command = runCommand(commandArray)
    
    # Check for failure
    if obj["failure"] == "returncode":
        if obj["failureValue"] == 0 and command.returncode > 0:
            print("Command response:", command)
            print("FAILED: Command returned failure condition. More output above.")
            return False
    
    # Check for true, warn when failure or success not detected
    if obj["success"] == "returncode":
        if obj["successValue"] == 0 and command.returncode == 0:
            print("SUCCESS: ", "Command returned success response")
            return True
    
    # success not detected, returning True for now
    print("WARN: did not meet success or failure criteria for:", obj["topic"])

# runCommandWithCheck(cmdList[0])
# runCommandWithCheck(cmdList[1])

def getVersion(commandArray):
    commandArray = splitCommandString(obj["command"])
    command = runCommand(commandArray)




def testCommands():
    print("Testing Commands...")


def installDocker():
    # subprocess.run(["sudo", "apt-get", "update"])
    commandList = { 
        "cmd1": "ls /",
        "cmd2": "ls ~"
    }

    for x in commandList:
        print(commandList[x])

    aptUpdate = "sudo apt-get update"
    installNetwork = "sudo apt-get install ca-certificates curl gnupg"

    installKeyrings = "sudo install -m 0755 -d /etc/apt/keyrings"
    getImage = "curl -fsSL https://download.docker.com/linux/raspbian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
    runChmod = "sudo chmod a+r /etc/apt/keyrings/docker.gpg"


    setupRepo = """echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/raspbian \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"""
    # runCommand("ls -la /")

# mainRunner()
# installDocker()

returnCode = subprocess.run(["git --version"], shell=True)
# returnCode = subprocess.run(["git", "-v"], shell=True)
print(returnCode)

subscript = subprocess.run(["sh ./script.sh"], shell=True)
print(subscript)
