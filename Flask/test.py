from flask import Flask, send_file, jsonify, render_template
import os, sys, glob, random, sqlite3

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template("home.html")

@app.route('/art')
@app.route('/art/<int:index>')
def art(index = None):
    if index is None:
        pathtext = open(os.path.join(sys.path[0], "path.txt"), "r")
        paths = pathtext.readlines()
        folder = glob.glob(os.path.join(paths[0].rstrip(), "*"))
        num = random.randint(0, len(folder)-1)
        file = folder[num]
        return send_file(file)
    else:
        pathtext = open(os.path.join(sys.path[0], "path.txt"), "r")
        paths = pathtext.readlines()
        folder = glob.glob(os.path.join(paths[0].rstrip(), "*"))
        if index > len(folder)-1:
            raise IndexError
        else:
            file = folder[index]
            return send_file(file)

def checkReg(discID: int):
    pathtext = open(os.path.join(sys.path[0], "path.txt"), "r")
    paths = pathtext.readlines()
    if os.path.exists(os.path.join(paths[1], "econ.db")):
        x = 0
        conn = sqlite3.connect(os.path.join(paths[1], "econ.db"))
        cursor = conn.cursor()
        cursor.execute('''SELECT id FROM economy''')
        results = cursor.fetchall()
        print(results)
        for x in range(len(results)):
            if discID == results[x][0]: 
                return True
        return False

@app.route('/economy/')
@app.route('/economy/<int:id>')
def eco(id=None):
    if id is None:
        pathtext = open(os.path.join(sys.path[0], "path.txt"), "r")
        paths = pathtext.readlines()
        if os.path.exists(os.path.join(paths[1], "econ.db")):
                conn = sqlite3.connect(os.path.join(paths[1], "econ.db"))
                cursor = conn.cursor()
                cursor.execute(f'''SELECT id FROM economy ORDER BY id''')
                idresult = cursor.fetchall()
                cursor.execute(f'''SELECT pekos FROM economy ORDER BY id''')
                pekosresult = cursor.fetchall()
                return jsonify({"ID": idresult, "Pekos": pekosresult}) # this technically does what I want but it could be done better LOL
    else:
        if checkReg(discID=id):
            pathtext = open(os.path.join(sys.path[0], "path.txt"), "r")
            paths = pathtext.readlines()
            if os.path.exists(os.path.join(paths[1], "econ.db")):
                conn = sqlite3.connect(os.path.join(paths[1], "econ.db"))
                cursor = conn.cursor()
                cursor.execute(f'''SELECT pekos FROM economy WHERE id = {id}''')
                result = cursor.fetchall()
                return jsonify({"ID": id, "Pekos": result[0][0]})
            else:
                return jsonify({"response": "Missing Database"})
        else:
            return jsonify({"response": "Not registered"})
        

app.run(debug=True, host="0.0.0.0")