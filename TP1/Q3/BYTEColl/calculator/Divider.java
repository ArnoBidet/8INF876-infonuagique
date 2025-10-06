package calculator;

public class Divider {
    public int divide(int a, int b) throws ZeroDivisionException {
        if (b == 0) {
            throw new ZeroDivisionException();
        }
        System.out.println("Calculation of " + a + " / "+ b );
        return a / b;
    }
}
