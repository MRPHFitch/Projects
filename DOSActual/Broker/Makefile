# Variables for the server and client scripts
SERVER=python3 server.py
client=python3 client.py
INPUT=input.txt

# Target to run both server and client
run:
	python3 server.py &
	python3 broker.py &
	sleep 1
	python3 client.py input.txt

	killall python3 || true

	python3 server.py &
	python3 broker.py &
	sleep 1
	python3 client.py input1.txt

	killall python3 || true

	python3 server.py &
	python3 broker.py &
	sleep 1
	python3 client.py input2.txt

	killall python3 || true

# Clean target to kill any Python processes (if necessary)
clean:
	@echo "Cleaning up..."
	killall python3 || true  # Kill any running python3 processes
