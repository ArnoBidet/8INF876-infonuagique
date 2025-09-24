package calculator;

import java.rmi.RemoteException;
import java.rmi.server.*;

public class Adder extends UnicastRemoteObject implements AdderRemote {
    public Adder() throws RemoteException {
        super();
    }

    @Override
    public int add(int a, int b) {
        System.out.println("Calculation of " + a + " + "+ b );
        return a + b;
    }
}
