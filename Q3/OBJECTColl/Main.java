import java.util.Scanner;

public class Main {
    static Scanner scanner = new Scanner(System.in);


    public static void main(String[] args) {
        //
        int result = 0;
        do {
            result = getUserInput();
            if (result != 1 && result != 2) {
                System.out.println("Wrong input, you typed :" + result);
                result = 0;
            }
        } while (result == 0);
        // We can now determine the instance the user wanted, then start it
        AgentInterface agent = result == 1 ? new Server() : new Client();
        agent.start();
    }

    public static void printQuestion() {
        System.out.println("Select what you want to launch :        ");
        System.out.println("1. Server");
        System.out.println("2. Client");
    }

    public static int getUserInput() {
        printQuestion();
        int answer = 0;
        try {
            answer = scanner.nextInt();
            scanner.nextLine(); // Consume the newline left by nextInt()
        } catch (Exception e) {
            System.err.println(e);
            scanner.nextLine(); // Clear invalid input
        }
        return answer;
    }
}
