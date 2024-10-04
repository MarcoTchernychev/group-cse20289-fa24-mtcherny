#Marco Tchernychev
#mtcherny@nd.edu
from flask import Flask, send_from_directory, Response
import os
app = Flask(__name__) #creates instance of app (webpage)
@app.route('/HW04WebpageFor/<interface>/<month>/<year>/', methods=['GET'])
def getPDF(interface, month, year):
    PDFpath = f"RPI01-{year}-{month}-{interface}.pdf"
    if not os.path.exists(PDFpath):
        return Response("PDF doesn't exist")

    else:
        return send_from_directory('.',PDFpath)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=54020)

