import java.io.*;
import java.net.*;
import java.util.Scanner;
import util.ByteStream;

public class Client implements AgentInterface {
    static Scanner scanner = new Scanner(System.in);
    private static final String SERVER_HOST = "localhost";
    private static final int SERVER_PORT = 12345;

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
                    result = sendByteCodeRequest("add", "Adder", values[0], values[1]);
                } else if (input.equals("2")) {
                    result = sendByteCodeRequest("substract", "Substractor", values[0], values[1]);
                } else if (input.equals("3")) {
                    result = sendByteCodeRequest("multiply", "Multiplier", values[0], values[1]);
                } else if (input.equals("4")) {
                    result = sendByteCodeRequest("divide", "Divider", values[0], values[1]);
                } else if (!input.matches("1|2|3|4|q")) {
                    System.out.println("Please, type a valid number or 'q' to quit.");
                    continue;
                }
                System.out.println("Result : " + result);
            } catch (Exception e) {
                System.err.println("Error calling server: " + e.getMessage());
                e.printStackTrace();
            }
        } while (!input.equals("q"));
        System.out.println("goodbye !");
        scanner.close();
    }

    private int sendByteCodeRequest(String operation, String className, int param1, int param2) throws Exception {
        System.out.println("Sending ByteColl request for " + operation + " with class " + className);

        try (Socket socket = new Socket(SERVER_HOST, SERVER_PORT);
                DataOutputStream output = new DataOutputStream(socket.getOutputStream());
                DataInputStream input = new DataInputStream(socket.getInputStream())) {

            // Send the operation name
            ByteStream.toStream(output, operation);
            System.out.println("Operation sent: " + operation);

            // Send the class name
            ByteStream.toStream(output, className);
            System.out.println("Class name sent: " + className);

            // Send the class bytecode
            File classFile = new File("calculator" + File.separator + className + ".class");
            if (!classFile.exists()) {
                throw new FileNotFoundException("Class file not found: " + classFile.getAbsolutePath());
            }

            ByteStream.toStream(output, classFile);
            System.out.println("Bytecode sent for class: " + className);

            // Send the parameters
            ByteStream.toStream(output, param1);
            ByteStream.toStream(output, param2);
            System.out.println("Parameters sent: " + param1 + ", " + param2);

            // Read the response
            String status = ByteStream.toString(input);
            System.out.println("Response status: " + status);

            if ("SUCCESS".equals(status)) {
                int result = ByteStream.toInt(input);
                System.out.println("Result received: " + result);
                return result;
            } else {
                String errorMessage = ByteStream.toString(input);
                throw new RuntimeException("Server error: " + errorMessage);
            }

        } catch (IOException e) {
            throw new RuntimeException("Communication error with server", e);
        }
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
            System.out.print("Please enter a valid integer for " + valueName + ": ");
            scanner.next();
        }
        return scanner.nextInt();
    }
}
