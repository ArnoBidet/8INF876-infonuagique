package calculator;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Divider extends UnicastRemoteObject implements DividerRemote {
    public Divider() throws RemoteException {
        super();
    }

    public double divide(int a, int b) throws ZeroDivisionException {
        try {
            System.out.println("Calculation of " + a + " / "+ b );
            return a / b;
        } catch (Exception e) {
            throw new ZeroDivisionException();
        }
    }
}
