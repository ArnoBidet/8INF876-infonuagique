package calculator;

import java.rmi.Remote;

public interface Substractor extends Remote {
    /**
     * @param a The substracted
     * @param b The substractor
     * @return The subtraction of a - b
     */
    int subtract(int a, int b);
}
