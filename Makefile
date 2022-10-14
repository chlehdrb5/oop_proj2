a.out: main.o inf_int.o
	g++ -std=c++14 -o app.out main.o inf_int.o

main.o: inf_int.h main.cpp
	g++ -std=c++14 -c -o main.o main.cpp

inf_int.o: inf_int.h inf_int.cpp
	g++ -std=c++14 -c -o inf_int.o inf_int.cpp