# Importing re module
import re
import sys
import os.path

filename = "shader"
if len(sys.argv)>1:
    filename=sys.argv[1]
filename = filename + ".webgl"

if not os.path.exists(filename):
    print("Could not find file "+filename)
    quit()

def replaceword(text, searchword, replaceword):
    return re.sub("\\b"+searchword+"\\b", replaceword, text)
  
def replacebegin(text, searchword, replaceword):
    return re.sub("\\b"+searchword, replaceword, text)

def removeline(text, search):
    return re.sub(search+".*\\n", "", text)

def mround(match):
    return str(round(float(match.group()),4))

def roundfloats(file):
    floatmatch = re.compile(r"\d*\.\d+")
    file = re.sub(floatmatch, mround, file)
    return file

texnames = ["texFFT", "texFFTSmoothed", "texFFTIntegrated", "texPreviousFrame", "texChecker", "texNoise", "texTex1", "texTex2", "texTex3", "texTex4"]
def replacetextures(file):
    texrepindex = 0
    reftext=""
    for t in texnames:
        channame = "iChannel"+str(texrepindex%4)
        result = re.subn("\\b"+t+"\\b", channame, file)
        if result[1] > 0:
            file = result[0]
            reftext += "// " + t + " -> " + channame + "\n"
            texrepindex += 1
    if texrepindex > 4:
        reftext += "// Warning, more than 4 textures used\n"
    file = reftext + file
    return file

with open(filename,'r+') as f:
  
    # Reading the file data and store
    # it in a file variable
    file = f.read()
        
    # Replacing the pattern with the string
    # in the file data
    file = replacebegin(file, "main\(\)", "mainImage( out vec4 out_color, in vec2 fragCoord )")
    file = replaceword(file, "gl_FragCoord", "fragCoord")
    file = replaceword(file, "fGlobalTime", "iTime")
    file = replaceword(file, "fFrameTime", "iTimeDelta")
    file = replaceword(file, "v2Resolution", "iResolution.xy")
            
    file = removeline(file, "\\blayout\\(")
    file = removeline(file, "#version")
    file = removeline(file, "\\bprecision mediump float")
    file = removeline(file, "\\bprecision highp int")

    file = replaceword(file, "highp ", "")

    # rounding float numbers
    file = roundfloats(file)

    file = replacetextures(file)

    # Setting the position to the top
    # of the page to insert data
    f.seek(0)
        
    # Writing replaced data in the file
    f.write(file)

    # Truncating the file size
    f.truncate()

    print("Output file: "+filename)
