from flask import Flask
from .routes import devices 

app = Flask(__name__, static_url_path='/static')
# 注册
app.register_blueprint(devices.devices_bp)
