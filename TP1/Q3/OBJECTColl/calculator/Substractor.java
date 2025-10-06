package calculator;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Substractor extends UnicastRemoteObject implements SubstractorRemote {
    public Substractor() throws RemoteException {
        super();
    }

    @Override
    public int substract(int a, int b) {
        System.out.println("Calculation of " + a + " - "+ b );
        return a - b;
    }
}
