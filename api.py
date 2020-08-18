import flask,os,subprocess,codecs
app = flask.Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = (1024 * 1024) / 2
goosList = ["android","darwin","dragonfly","freebsd","linux","naci","netbsd","openbsd","plan9","solaris","windows","zos"]
goarchList = ["386","amd64","amd64p32","arm","armbe","arm64","arm64be","ppc64","ppc64le","mips","mipsle","mips64","mips64le","mips64p32","mips64p32le","ppc","s390","s390x","sparc","sparc64"]

def okfalse(why):
    return '{"ok":"false","why":"'+why+'"}'

def createResp(veri="",status=200):
    return flask.Response(response=veri,status=status,mimetype="application/json")


@app.route("/")
def home():
    return flask.render_template("home.html")

@app.route("/api")
def api():
    return createResp(okfalse("Go /api/go"),404)

@app.route("/api/go",methods=["GET","POST"])
def apiGo():
    
    data = flask.request.args.get("data")
    if not data:
        data = flask.request.form.get("data")

    goarch = flask.request.args.get("goarch")
    if not goarch:
        goarch = flask.request.form.get("goarch")
    
    goos = flask.request.args.get("goos")
    if not goos:
        goos = flask.request.form.get("goos")


    # Acemice olmasına rağmen iş görecektir.


    if not data:
        if "data" in flask.request.files and flask.request.files["data"].filename != '':
            data = flask.request.files["data"].filename
            flask.request.files["data"].save("onbellek/"+data)
            try:
                with open("onbellek/"+data) as oku:
                    os.remove("onbellek/"+data)
                    data_ = oku.read()
                    #print(data_)

                    data = data_
            except:
                return createResp(okfalse("{}is not readable !".format(data)))

        else:
            return createResp(okfalse("data is empty ."),502)
    elif not goos:
        return createResp(okfalse("goos is empty ."),502)
    elif not goarch:
        return createResp(okfalse("goarch is empty ."),502)


    if len(data.splitlines()) > 500:
        return createResp(okfalse("more than 500 lines of data !"),502)

    if goos not in goosList:
        return createResp(okfalse("{} not in GOOS List".format(goos)),502)    

    if goarch not in goarchList:
        return createResp(okfalse("{} not in GOARCH List".format(goarch)),502)

    while 1:
        date = os.popen("LANG=en date").read().strip("\n").replace(" ","_")
        date = "files/GoCompiler/"+date
        #print(date)
        if not os.path.exists(date):
            os.mkdir(date)
        else:break
    
    data = data+"\n\n// @BetikSonu - BetikSonu.org | GoCompiler"


    with open(date+"/main.go","w") as yaz:
        yaz.write(data)
    try:
        cmd = ["bash","comp.sh",date,goos,goarch]
        ou = subprocess.check_output(cmd,stderr=subprocess.STDOUT,timeout=30)

    except subprocess.TimeoutExpired as hata:
        os.system("rm -rf {}".format(date))
        return createResp(okfalse("Your compile canceled by timeout ! (30)"),502)
    
    except subprocess.CalledProcessError as e:
        os.system("rm -rf {}".format(date))
        return flask.jsonify({"ok":"false","why":"Your compile canceled by GoCompiler : {}".format(codecs.decode(str(e.output).lstrip("b"),"unicode_escape"))})
    
    except Exception as hata:
        os.system("rm -rf {}".format(date))
        print("\033[31mHATA\033[0m",str(hata))
        return flask.jsonify({"ok":"false","why":"Damn it ! Err : {}".format(str(hata))})
    else:
        files = os.listdir("./"+date)
        print("\033[32m",files,"\033[0m")
        files.remove("main.go")
        files = files[0]
        
        return flask.jsonify({"ok":"true","url":"https://BetikSonu.org/gocompiler/files/"+date.strip("files/")+"/"+files})
    #return okfalse(str(data))

app.run(debug=False,port=1010)
