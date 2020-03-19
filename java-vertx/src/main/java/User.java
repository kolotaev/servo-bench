package com.kolotaev;

import java.util.List;
import java.util.Map;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;

public class User {
    public String name;
    public String surname;
    public String street;
    public String school;
    public String bank;
    public int a;
    public double b;
    public int c;
    public List<User> friends;

    public User(String name, String surname, String street,
                String school, String bank, int a, double b, int c) {
        this.name = name;
        this.surname = surname;
        this.street = street;
        this.school = school;
        this.bank = bank;
        this.a = a;
        this.b = b;
        this.c = c;
        this.friends = new ArrayList<User>();
    }

    public static User create(boolean withFriend) {
        User u = new User(
            randomString(10),
            randomString(3),
            randomString(15),
            randomString(9),
            randomString(4),
            new Random().nextInt(100),
            new Random().nextDouble(),
            new Random().nextInt(100)
        );
        if (withFriend) u.friends.add(create(false));
        return u;
    }

    private static String randomString(int len) {
        return new Random().ints(97, 123)
          .limit(len)
          .collect(StringBuilder::new, StringBuilder::appendCodePoint, StringBuilder::append)
          .toString();
    }
}
