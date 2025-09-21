package calculator;

import java.rmi.Remote;

public interface Divider extends Remote {
    /**
     * @param a The numerator
     * @param b The denumerator
     * @return The quotient
     */
    double divide(int a, int b) throws ZeroDivisionException;
}
