import java.rmi.Naming;

import calculator.*;

public class Server implements AgentInterface {
    @Override
    public void start() {
        System.out.println("You have started a server.");
        System.setProperty("java.security.policy","./security.policy");
        System.setSecurityManager(new SecurityManager());

        try {
            Naming.rebind("adder", new Adder());
            Naming.rebind("substractor", new Substractor());
            Naming.rebind("multiplier", new Multiplier());
            Naming.rebind("divider", new Divider());
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
    }
}
