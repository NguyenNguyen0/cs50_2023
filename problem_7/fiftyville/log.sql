-- Keep a log of any SQL queries you execute as you solve the mystery.
-- the theft took place on July 28, 2021 and that it took place on Humphrey Street.
SELECT description FROM crime_scene_reports
WHERE month = 7
AND day = 28
AND street = "Humphrey Street";

/*
 Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
 Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
 Littering took place at 16:36. No known witnesses.
*/

 SELECT transcript FROM interviews
 WHERE month = 7
 AND day = 28;

/*
 I don't know the thief's name, but it was someone I recognized. Earlier this morning,
 before I arrived at Emma's bakery,
 I was walking by the ATM on //Leggett Street// and saw the thief there withdrawing some money.
*/

/*
 As the thief was leaving the bakery, they called someone who talked to them for //less than a minute//.
 In the call, I heard the thief say that they were planning to take the //earliest flight out of Fiftyville tomorrow //.
 The thief then asked the person on the other end of the phone to purchase the flight ticket.
*/

/*
 Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
 If you have security footage from the bakery parking lot,
 you might want to look for cars that left the parking lot in that time frame.
*/

-- phone_number
SELECT people.name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60;

-- license_plate
SELECT people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 10
AND bakery_security_logs.minute <= 25
AND bakery_security_logs.activity = "exit";

-- account_number
SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw";

-- passport_number
SELECT people.name FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.day = 29
AND flights.month = 7
AND flights.origin_airport_id = (SELECT airports.id FROM airports WHERE airports.city = "Fiftyville")
AND flights.hour = (SELECT MIN(flights.hour) FROM flights WHERE flights.day = 29 AND flights.month = 7);


-- THIEF
SELECT * FROM people
-- phone_number
WHERE people.name IN (SELECT people.name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60)
-- license_plate
AND people.name IN (SELECT people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 10
AND bakery_security_logs.minute <= 25
AND bakery_security_logs.activity = "exit")
-- account_number
AND people.name IN (SELECT people.name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = "Leggett Street"
AND atm_transactions.transaction_type = "withdraw")
-- passport_number
AND people.name IN (SELECT people.name FROM people
JOIN passengers ON passengers.passport_number = people.passport_number
JOIN flights ON flights.id = passengers.flight_id
JOIN airports ON flights.origin_airport_id = airports.id
WHERE flights.day = 29
AND flights.month = 7
AND flights.origin_airport_id = (SELECT airports.id FROM airports WHERE airports.city = "Fiftyville")
AND flights.hour = (SELECT MIN(flights.hour) FROM flights WHERE flights.day = 29 AND flights.month = 7));


/*
    The THIEF is:
    id: 686048
    name: Bruce
    phone_number: (367) 555-5533
    passport_number: 5773159633
    license_plate: 94KL13X
*/

-- ACCOMPLICE
SELECT * FROM people
JOIN phone_calls ON phone_calls.receiver = people.phone_number
WHERE phone_calls.caller = "(367) 555-5533"
AND phone_calls.month = 7
AND phone_calls.day = 28
AND phone_calls.duration < 60;


/*
    The ACCOMPLICE is:
    id: 864400
    name: Robin
    phone_number: (375) 555-8161
    passport_number: NULL
    license_plate: 4V16VO0
*/

-- The city the thief ESCAPED TO
SELECT airports.city FROM airports
JOIN flights ON flights.destination_airport_id = airports.id
WHERE flights.day = 29
AND flights.month = 7
AND flights.origin_airport_id = (SELECT airports.id FROM airports WHERE airports.city = "Fiftyville")
AND flights.hour = (SELECT MIN(flights.hour) FROM flights WHERE flights.day = 29 AND flights.month = 7);

/*
    city is:
    New York City
*/