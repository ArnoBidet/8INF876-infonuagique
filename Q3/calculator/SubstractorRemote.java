package calculator;

import java.rmi.Remote;
import java.rmi.RemoteException;

public interface SubstractorRemote extends Remote {
    /**
     * @param a The substracted
     * @param b The substractor
     * @return The substraction of a - b
     */
    int substract(int a, int b) throws RemoteException ;
}
