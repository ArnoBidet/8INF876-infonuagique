import java.io.*;
import java.net.*;
import java.lang.reflect.*;
import util.ByteStream;

public class Server implements AgentInterface {
    private ServerSocket serverSocket;
    private static final int PORT = 12345;
    
    @Override
    public void start() {
        System.out.println("You have started a ByteColl server on port " + PORT);
        System.setProperty("java.security.policy","./security.policy");
        System.setSecurityManager(new SecurityManager());

        try {
            serverSocket = new ServerSocket(PORT);
            System.out.println("Server listening on port " + PORT);
            
            while (true) {
                Socket clientSocket = serverSocket.accept();
                System.out.println("New client connection accepted");
                
                // Handle each client in a separate thread
                new Thread(() -> handleClient(clientSocket)).start();
            }
        } catch (IOException e) {
            System.err.println("Server error: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private void handleClient(Socket clientSocket) {
        try (DataInputStream input = new DataInputStream(clientSocket.getInputStream());
             DataOutputStream output = new DataOutputStream(clientSocket.getOutputStream())) {
            
            // Read the requested operation name
            String operation = ByteStream.toString(input);
            System.out.println("Requested operation: " + operation);
            
            // Read the class name
            String className = ByteStream.toString(input);
            System.out.println("Requested class: " + className);
            
            // Read the class bytecode
            File tempClassFile = new File(className + ".class");
            ByteStream.toFile(input, tempClassFile);
            System.out.println("Bytecode received for class: " + className);
            
            // Read the parameters
            int param1 = ByteStream.toInt(input);
            int param2 = ByteStream.toInt(input);
            System.out.println("Parameters received: " + param1 + ", " + param2);
            
            // Load and execute the class
            try {
                Object result = loadAndExecute(className, operation, param1, param2, tempClassFile);
                
                // Send the result
                if (result instanceof Integer) {
                    ByteStream.toStream(output, "SUCCESS");
                    ByteStream.toStream(output, (Integer) result);
                } else {
                    ByteStream.toStream(output, "ERROR");
                    ByteStream.toStream(output, result.toString());
                }
                
            } catch (Exception e) {
                System.err.println("Error during execution: " + e.getMessage());
                e.printStackTrace();
                ByteStream.toStream(output, "ERROR");
                ByteStream.toStream(output, e.getMessage());
            } finally {
                // Clean up temporary file
                if (tempClassFile.exists()) {
                    tempClassFile.delete();
                }
            }
            
        } catch (IOException e) {
            System.err.println("Communication error with client: " + e.getMessage());
            e.printStackTrace();
        }
    }
    
    private Object loadAndExecute(String className, String operation, int param1, int param2, File classFile) 
            throws Exception {
        
        // Read bytecode from temporary file created from received data
        byte[] classData;
        try (FileInputStream fis = new FileInputStream(classFile)) {
            classData = new byte[(int) classFile.length()];
            fis.read(classData);
        }
        
        // Create a custom ClassLoader to load the received bytecode
        ClassLoader classLoader = new ByteCodeClassLoader(classData, className);
        
        // Load the class from received bytecode
        Class<?> clazz = classLoader.loadClass("calculator." + className);
        System.out.println("Class loaded from received bytecode: " + clazz.getName());
        
        // Create an instance
        Constructor<?> constructor = clazz.getConstructor();
        Object instance = constructor.newInstance();
        System.out.println("Instance created for: " + className);
        
        // Execute the appropriate method
        Method method = null;
        switch (operation.toLowerCase()) {
            case "add":
                method = clazz.getMethod("add", int.class, int.class);
                break;
            case "substract":
                method = clazz.getMethod("substract", int.class, int.class);
                break;
            case "multiply":
                method = clazz.getMethod("multiply", int.class, int.class);
                break;
            case "divide":
                method = clazz.getMethod("divide", int.class, int.class);
                break;
            default:
                throw new NoSuchMethodException("Unsupported operation: " + operation);
        }
        
        System.out.println("Executing method: " + method.getName() + "(" + param1 + ", " + param2 + ")");
        return method.invoke(instance, param1, param2);
    }
    
    // Custom ClassLoader to load classes from received bytecode
    private static class ByteCodeClassLoader extends ClassLoader {
        private byte[] classData;
        private String className;
        
        public ByteCodeClassLoader(byte[] classData, String className) {
            this.classData = classData;
            this.className = className;
        }
        
        @Override
        protected Class<?> findClass(String name) throws ClassNotFoundException {
            if (name.equals("calculator." + className)) {
                // Define the class from received bytecode
                return defineClass(name, classData, 0, classData.length);
            }
            return super.findClass(name);
        }
    }
}
