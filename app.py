from flask import Flask, render_template, request, redirect, url_for
from threading import Thread
import time

app = Flask(__name__)

# Driver data structure
class Driver:
    def __init__(self, name, deliveries=0):
        self.name = name
        self.deliveries = deliveries
        self.active = True

drivers = []

# Background thread for auto-assigning deliveries every 3 seconds
def auto_add_deliveries():
    while True:
        time.sleep(3)
        active_drivers = [d for d in drivers if d.active]
        if active_drivers:
            driver = min(active_drivers, key=lambda d: d.deliveries)
            driver.deliveries += 1
            print(f"[+] Assigned delivery to {driver.name} (Total Deliveries: {driver.deliveries})")

# Start the delivery assignment thread
Thread(target=auto_add_deliveries, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', drivers=drivers)

@app.route('/add_driver_page')
def add_driver_page():
    return render_template('add_driver.html')

@app.route('/add_driver', methods=['POST'])
def add_driver():
    name = request.form.get('name')
    deliveries = request.form.get('deliveries')

    if not name or deliveries is None:
        return "Missing driver name or delivery count", 400

    try:
        deliveries = int(deliveries)
    except ValueError:
        return "Deliveries must be a number", 400

    new_driver = Driver(name, deliveries)
    drivers.append(new_driver)
    return redirect(url_for('index'))

@app.route('/toggle_driver/<int:index>', methods=['POST'])
def toggle_driver(index):
    if 0 <= index < len(drivers):
        drivers[index].active = not drivers[index].active
    return redirect(url_for('index'))

@app.route('/complete_delivery/<int:index>', methods=['POST'])
def complete_delivery(index):
    if 0 <= index < len(drivers):
        driver = drivers[index]
        if driver.deliveries > 0:
            driver.deliveries -= 1
            print(f"[✓] {driver.name} completed a delivery. Total Deliveries: {driver.deliveries}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
