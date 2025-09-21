package calculator;

import java.rmi.RemoteException;
import java.rmi.server.*;

public class AdderImpl extends UnicastRemoteObject implements Adder {
    public AdderImpl() throws RemoteException {
        super();
    }

    @Override
    public int add(int a, int b) {
        return a + b;
    }
}
