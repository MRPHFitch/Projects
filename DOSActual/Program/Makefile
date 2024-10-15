#	Run all input cases
# 	Run test before processing input files
run: clean
	$(MAKE) test  
	python program1.py input.txt output.txt
	python program1.py input1.txt output1.txt
	python program1.py input2.txt output2.txt

#	Tests functions
test:
	pytest test_graph.py

#	Clean previous files generated
clean:
	rm -f output.txt
	rm -f output1.txt
	rm -f output2.txt
	rm -f input.txt_throughput.csv
	rm -f input1.txt_throughput.csv
	rm -f input2.txt_throughput.csv
	rm -f input.txt_benchmark.csv
	rm -f input1.txt_benchmark.csv
	rm -f input2.txt_benchmark.csv
	

