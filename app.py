from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Driver:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.deliveries = 0

drivers = [
    Driver(1, "Alice"),
    Driver(2, "Bob"),
    Driver(3, "Charlie"),
]

def assign_delivery():
    driver = min(drivers, key=lambda d: d.deliveries)
    driver.deliveries += 1
    return driver

@app.route('/')
def index():
    return render_template('index.html', drivers=drivers)

@app.route('/assign_delivery', methods=['POST'])
def assign_delivery_route():
    assign_delivery()
    return redirect(url_for('index'))

@app.route('/complete_delivery/<int:driver_id>', methods=['POST'])
def complete_delivery(driver_id):
    for driver in drivers:
        if driver.id == driver_id and driver.deliveries > 0:
            driver.deliveries -= 1
            break
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
