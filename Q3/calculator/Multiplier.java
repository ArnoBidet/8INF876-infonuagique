package calculator;

import java.rmi.Remote;

public interface Multiplier extends Remote {
    /**
     * @param a The first factor
     * @param b The second factor
     * @return The multiplication of a * b
     */
    int multiply(int a, int b);
}
