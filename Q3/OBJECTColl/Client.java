import java.rmi.RemoteException;
import java.net.MalformedURLException;
import java.rmi.Naming;
import java.rmi.NotBoundException;
import java.util.Scanner;

import calculator.AdderRemote;
import calculator.SubstractorRemote;
import calculator.ZeroDivisionException;
import calculator.MultiplierRemote;
import calculator.DividerRemote;

public class Client implements AgentInterface {
    static Scanner scanner = new Scanner(System.in);

    @Override
    public void start() {
        String input = "";
        do {
            System.setProperty("java.security.policy", "./security.policy");
            System.out.println("=========================");
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
            if (input.matches("q"))
                break;
            int[] values = askForTwoValues();
            try {
                int result = 0;
                if (input.equals("1")) {
                    AdderRemote adder = serviceGetter("adder");
                    result = adder.add(values[0], values[1]);
                } else if (input.equals("2")) {
                    SubstractorRemote substractor = serviceGetter("substractor");
                    result = substractor.substract(values[0], values[1]);
                } else if (input.equals("3")) {
                    MultiplierRemote multiplier = serviceGetter("multiplier");
                    result = multiplier.multiply(values[0], values[1]);
                } else if (input.equals("4")) {
                    DividerRemote divider = serviceGetter("divider");
                    result = (int) divider.divide(values[0], values[1]);
                } else if (!input.matches("1|2|3|4|q")) {
                    System.out.println("Please, type a valid number or 'q' to quit.");
                }
                System.out.println("Result : " + result);
            } catch (RemoteException e) {
                System.err.println("RemoteException occurred: " + e.getMessage());
                e.printStackTrace();
            } catch (ZeroDivisionException e) {
                System.err.println("ZeroDivisionException occurred: " + e.getMessage());
                e.printStackTrace();
            }
        } while (!input.equals("q"));
        System.out.println("goodbye !");
        scanner.close();
    }

    private <T> T serviceGetter(String serviceName) {
        System.setSecurityManager(new SecurityManager());
        T result = null;
        try {
            String url = new String("rmi://localhost/" + serviceName);
            result = (T) Naming.lookup(url);
            System.out.println(result.toString());
        } catch (MalformedURLException | NotBoundException | RemoteException e) {
            System.out.println("Erreur a l'accès du gest. banc." + e);
        }
        return result;
    }

    private int[] askForTwoValues() {
        int[] values = new int[2];
        values[0] = askValue("a");
        values[1] = askValue("b");
        scanner.nextLine();
        return values;
    }

    private int askValue(String valueName) {
        System.out.print("Enter value for " + valueName + " : ");
        while (!scanner.hasNextInt()) {
            System.out.print("Please enter a valid integer for b: ");
            scanner.next();
        }
        return scanner.nextInt();
    }
}
