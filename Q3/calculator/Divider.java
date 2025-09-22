package calculator;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class Divider extends UnicastRemoteObject implements DividerRemote {
    public Divider() throws RemoteException {
        super();
    }

    public double divide(int a, int b) throws ZeroDivisionException {
        try {
            return a / b;
        } catch (Exception e) {
            throw new ZeroDivisionException();
        }
    }
}
