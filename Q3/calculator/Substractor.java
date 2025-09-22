package calculator;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface Substractor extends Remote {
    /**
     * @param a The substracted
     * @param b The substractor
     * @return The subtraction of a - b
     */
    int subtract(int a, int b) throws RemoteException ;
}
