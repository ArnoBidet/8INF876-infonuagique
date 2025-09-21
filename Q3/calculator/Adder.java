package calculator;

import java.rmi.Remote;

public interface Adder extends Remote {
    /**
     * @param a The first value
     * @param b The second
     * @return The value of a + b
     */
    int add(int a, int b);
}
