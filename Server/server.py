from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

raspberry_pi_data = {
    'disk_usage': 'N/A',
    'core_status': 'N/A',
    'wifi_state': 'N/A',
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('refresh', broadcast=True)

@socketio.on('refresh')
def handle_refresh():
    emit('refresh', broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('pi_data')
def handle_pi_data(data):
    raspberry_pi_data.update(data)
    emit('update', raspberry_pi_data, broadcast=True)

@socketio.on('pi_data_result')
def handle_pi_data_result(data):
    emit('pi_data_result', data, broadcast=True)

@socketio.on('network_state')
def handle_network_state(data):
    emit('network_state', data, broadcast=True)

@socketio.on('request_network_state')
def handle_network_request(data):
    emit('request_network_state', data, broadcast=True)

@socketio.on('request_wifi_clients')
def handle_request_wifi_clients():
    emit('request_wifi_clients', broadcast=True)

@socketio.on('request_wifi')
def handle_request_wifi():
    emit('request_wifi', broadcast=True)
    
@socketio.on('request_connect_wifi')
def handle_connect_wifi(data):
    emit('request_connect_wifi', data, broadcast=True)

@socketio.on('request_reboot')
def handle_request_reboot():
    emit('request_reboot', broadcast=True)

@socketio.on('request_shutdown')
def handle_request_shutdown():
    emit('request_shutdown', broadcast=True)

@socketio.on('request_send_command')
def handle_request_send_command(data):
    emit('request_send_command', data, broadcast=True)

@socketio.on('cmd_result')
def handle_cmd_result(data):
    emit('cmd_result', data, broadcast=True)

@socketio.on('request_ssh_interrupt')
def handle_request_ssh_interrupt():
    emit('request_ssh_interrupt', broadcast=True)

if __name__ == '__main__':
    import eventlet
    from eventlet import wsgi
    wsgi.server(eventlet.listen(('0.0.0.0', 12667)), app)
