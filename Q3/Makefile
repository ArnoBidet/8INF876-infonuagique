clean:
	find . -name "*.class" -delete

start-instance:
	java Main

compile:
	javac -d . calculator/Adder.java && rmic calculator.Adder &&\
	javac -d . calculator/Substractor.java && rmic calculator.Substractor &&\
	javac -d . calculator/Multiplier.java && rmic calculator.Multiplier &&\
	javac -d . calculator/Divider.java && rmic calculator.Divider &&\
	javac Main.java

start-rmi:
	rmiregistry 1099 &

stop-rmi:
	pkill -f 'rmiregistry 1099' || true

