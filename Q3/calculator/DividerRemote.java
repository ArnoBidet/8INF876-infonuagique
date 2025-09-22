package calculator;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface DividerRemote extends Remote {
    /**
     * @param a The numerator
     * @param b The denumerator
     * @return The quotient
     */
    double divide(int a, int b) throws ZeroDivisionException, RemoteException ;
}
