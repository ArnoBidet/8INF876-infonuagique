import java.rmi.Naming;

import calculator.*;

public class Server implements AgentInterface {
    @Override
    public void start() {
        System.out.println("Vous avez lancé un serveur.");
        System.setProperty("java.security.policy","./security.policy");
        System.setSecurityManager(new SecurityManager());

        try {
            AdderRemote ai = new Adder();
            SubstractorRemote si = new Substractor();
            MultiplierRemote mi = new Multiplier();
            DividerRemote di = new Divider();
            Naming.rebind("adder", ai);
            Naming.rebind("substractor", si);
            Naming.rebind("multiplier", mi);
            Naming.rebind("divider", di);
        }catch(Exception e){
            System.out.println(e.getMessage());
        }
    }
}
