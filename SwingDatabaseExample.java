import javax.swing.*;
import java.awt.event.*;
import java.sql.*;

public class SwingDatabaseExample {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Database Connectivity Example");
        JLabel label = new JLabel("Enter Name:");
        JTextField textField = new JTextField(20);
        JButton button = new JButton("Save");

        label.setBounds(20, 20, 100, 30);
        textField.setBounds(130, 20, 200, 30);
        button.setBounds(130, 60, 100, 30);

        frame.add(label);
        frame.add(textField);
        frame.add(button);
        frame.setSize(400, 200);
        frame.setLayout(null);
        frame.setVisible(true);

        button.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                String name = textField.getText();

                // الاتصال بقاعدة البيانات وإدخال البيانات
                String url = "C:/Users/Lenovo/OneDrive - Alexandria University/Documents/SQL Server Management Studio" ;
                String user = "YourUsername";
                String password = "YourPassword";

                try (Connection connection = DriverManager.getConnection(url, user, password)) {
                    String query = "INSERT INTO YourTableName (ColumnName) VALUES (?)";
                    try (PreparedStatement preparedStatement = connection.prepareStatement(query)) {
                        preparedStatement.setString(1, name);
                        preparedStatement.executeUpdate();
                        JOptionPane.showMessageDialog(frame, "Data Saved Successfully!");
                    }
                } catch (SQLException ex) {
                    JOptionPane.showMessageDialog(frame, "Error: " + ex.getMessage());
                    ex.printStackTrace();
                }
            }
        });
    }
}
