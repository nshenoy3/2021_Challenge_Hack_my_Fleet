from flask import Flask, render_template
import pandas as pd
from Fuel import getFuelInsights,showFuelInsightsFor
from asset import showBestAsset
from maps import showAssetTracking
app = Flask(__name__)

part1 = pd.read_csv("./Dataset/hack_illinois_part1.csv", sep = ",", header = 0, engine='python')
print("Loaded part1")
part2 = pd.read_csv("./Dataset/hack_illinois_part2.csv", sep = ",", header = 0, engine='python')
print("Loaded part 2")
dataset = part1.append(part2)
fuelData = getFuelInsights(dataset)

print("Hello Hackathon!!!")
@app.route('/')
def upload_file():
    print("In upload file")
    return render_template('index.html')

@app.route('/fuelInsights')
def showFuelfile():
    showFuelInsightsFor(fuelData, "1022017", "Excavator")

@app.route('/bestAsset')
def showBestAssets():
    showBestAsset(dataset)

@app.route('/assetTracking')
def assetTracking():
    showAssetTracking(dataset)

if __name__ == '__main__':
    app.run(debug=False)


