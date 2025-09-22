import java.rmi.Naming;
import java.rmi.RemoteException;

import calculator.AdderRemote;
import java.util.Scanner;

public class Client implements AgentInterface {
    static Scanner scanner = new Scanner(System.in);

    @Override
    public void start() {
        String input = "";
        do {
            System.out.println("Choose a functionnality :");
            System.out.println("1 - Adder");
            System.out.println("2 - Substractor");
            System.out.println("3 - Multiplier");
            System.out.println("4 - Divider");
            System.out.println("q - Quit");
            System.out.print("Your choice : ");
            if (scanner.hasNextLine())
                input = scanner.nextLine();
            input = input.trim();
            if (input.equals("1")) {
                AdderRemote adder = calculatorFunctionnalty("");
                try {
                    System.out.print("Result : " + adder.add(1, 2));
                } catch (RemoteException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            } else if (!input.matches("1|q")){
                System.out.println("Please, type a valid number or 'q' to quit.");
            }
        } while (!input.equals("q"));
        System.out.println("goodbye !");
        scanner.close();
    }

    public <T> T calculatorFunctionnalty(String serviceName) {
        System.out.println("Calculator selected.");
        System.setSecurityManager(new SecurityManager());
        T result = null;
        try {
            String url = new String("rmi://localhost/" + serviceName);
            result = (T) Naming.lookup(url);
        } catch (Exception e) {
            System.out.println("Erreur a l'accès du gest. banc." + e);
        }
        return result;
    }
}
