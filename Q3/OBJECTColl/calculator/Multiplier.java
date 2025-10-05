package calculator;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Multiplier extends UnicastRemoteObject implements MultiplierRemote {
    public Multiplier() throws RemoteException {
        super();
    }

    public int multiply(int a, int b) {
        System.out.println("Calculation of " + a + " * "+ b );
        return a * b;

    }
}
