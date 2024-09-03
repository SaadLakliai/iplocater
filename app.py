from flask import Flask, request, render_template
import folium, geocoder

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        input_value = request.form['input_value']
        ip = geocoder.ip(input_value)
        if not ip.latlng:
            return "Unable to locate IP address.", 400
        
        address = ip.latlng

        map = folium.Map(location=address, zoom_start=12)
        marker = folium.Marker(location=address, popup="This is an approximation of where this IP lives")
        circle = folium.Circle(location=address, radius=200, color="blue", fill=True, fill_color="blue")

        marker.add_to(map)
        circle.add_to(map)

        map.save("templates/location.html")
        return render_template("location.html")
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
