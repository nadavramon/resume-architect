#!/bin/bash

# 1. Start the Java Backend in the background (&)
# We hide the logs > /dev/null so they don't mess up your UI, 
# or you can remove '> /dev/null' to see Java logs.
echo "☕️ Booting up Java Pub/Sub Server..."
java -jar server.jar &

# Capture the Process ID (PID) so we can kill it later
JAVA_PID=$!
sleep 2  # Give Java a second to initialize

# 2. Start the Frontend
echo "🚀 Launching Streamlit Frontend..."
streamlit run app.py

# 3. Cleanup: When you close Streamlit, kill the Java server
echo "🛑 Shutting down Java Server (PID: $JAVA_PID)..."
kill $JAVA_PID