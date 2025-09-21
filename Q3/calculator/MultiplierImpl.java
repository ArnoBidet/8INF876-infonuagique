package calculator;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class MultiplierImpl extends UnicastRemoteObject implements Multiplier {
    public MultiplierImpl() throws RemoteException {
        super();
    }

    public int multiply(int a, int b) {
        return a * b;

    }
}
