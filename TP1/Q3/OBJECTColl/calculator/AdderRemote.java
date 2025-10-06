package calculator;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface AdderRemote extends Remote {
    /**
     * @param a The first value
     * @param b The second
     * @return The value of a + b
     */
    int add(int a, int b) throws RemoteException;
}
