clean:
	find . -name "*.class" -delete

start-instance:
	java Main

compile:
	javac -d . util/ByteStream.java &&\
	javac -d . calculator/ZeroDivisionException.java &&\
	javac -d . calculator/Adder.java &&\
	javac -d . calculator/Substractor.java &&\
	javac -d . calculator/Multiplier.java &&\
	javac -d . calculator/Divider.java &&\
	javac -cp . Main.java &&\
	javac -cp . Server.java &&\
	javac -cp . Client.java

start-server:
	java -cp . Main server

start-client:
	java -cp . Main client

