import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        for(int i=0;i<10;i++)
	{
		int x=Integer.parseInt(br.readLine());	
		System.out.println(++x);
	}
    }
}
