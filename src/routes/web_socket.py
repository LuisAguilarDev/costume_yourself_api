from flask import Flask, Response
import time

app = Flask(__name__)

# Function to generate the Server-Sent Events
def generate_sse():
    for i in range(1, 11):  # Send 10 events
        time.sleep(2)  # Simulate a long-running process
        yield f"data: Event {i}\n\n"  # SSE format requires 'data:' for each message

# Endpoint that returns the SSE stream
@app.route('/events')
def stream():
    return Response(generate_sse(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
