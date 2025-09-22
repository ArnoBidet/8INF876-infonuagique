import java.rmi.Naming;

import calculator.*;

public class Server implements AgentInterface {
    @Override
    public void start() {
        System.out.println("Vous avez lancé un serveur.");
        System.setSecurityManager(new SecurityManager());
        try {
            Adder ai = new AdderImpl();
            Substractor si = new SubstractorImpl();
            Multiplier mi = new MultiplierImpl();
            Divider di = new DividerImpl();
            Naming.rebind("adder", ai);
            Naming.rebind("substractor", si);
            Naming.rebind("multiplier", mi);
            Naming.rebind("divider", di);
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
    }
}
