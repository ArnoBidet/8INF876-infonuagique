package calculator;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;

public class SubstractorImpl extends UnicastRemoteObject implements Substractor {
    public SubstractorImpl() throws RemoteException {
        super();
    }

    @Override
    public int subtract(int a, int b) {
        return a - b;
    }
}
