# Variables for the server and client scripts
SERVER=python3 graphserver.py
CLIENT=python3 graphclient.py
INPUT=input.txt

# Target to run both server and client
run:
	python3 graphserver.py &
	sleep 1
	python3 graphclient.py input.txt

	killall python3 || true

	python3 graphserver.py &
	sleep 1
	python3 graphclient.py input1.txt

	killall python3 || true

	python3 graphserver.py &
	sleep 1
	python3 graphclient.py input2.txt

	killall python3 || true

# Clean target to kill any Python processes (if necessary)
clean:
	@echo "Cleaning up..."
	killall python3 || true  # Kill any running python3 processes
