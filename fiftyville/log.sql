-- Keep a log of any SQL queries you execute as you solve the mystery.

-- This query is to get the id of the crime scene report and a description of the theft
SELECT
    id, description
FROM
    crime_scene_reports
WHERE
    year = 2024 AND month = 7 AND day = 28
        AND street = 'Humphrey Street';
-- Theft time: 10:15 am
-- 3 witnesses mention the bakery


-- This query is to get the interviews of the witnesses
SELECT
    name, transcript
FROM
    interviews
WHERE
    year = 2024 AND month = 7 AND day = 28;
-- Ruth: Security footage of the bakery parking lot of cars that was there by the time of 10:25am
-- Eugene: ATM transactions at Leggett Street before the theft
-- Raymond: Purchasing of the ticket for the earliest flight out oh fiftyville on the next day (07/29/2024)


-- This query is to get the license plate of everyone who exited the parking lot during that period of time (10 min within the theft)
SELECT
    license_plate
FROM
    bakery_security_logs
WHERE
    year = 2024 AND month = 7 AND day = 28
        AND hour = 10
        AND minute BETWEEN 15 AND 25
        AND activity = 'exit';
-- Quite a lot...


-- This query is to see the account number and amount of everyone who withdrew money that day
SELECT
    account_number, amount
FROM
    atm_transactions
WHERE
    year = 2024 AND month = 07 AND day = 28
        AND atm_location = 'Leggett Street'
        AND transaction_type = 'withdraw';
-- There's a lot again...


-- This query is to get the IDs of all the bank accounts of the previous list
SELECT
    person_id
FROM
    bank_accounts
WHERE
    account_number IN (SELECT
            account_number
        FROM
            atm_transactions
        WHERE
            year = 2024 AND month = 07 AND day = 28
                AND atm_location = 'Leggett Street'
                AND transaction_type = 'withdraw');
-- This is ID list of suspects


-- This query is to see which is the earliest flight out of Fiftyville
SELECT
    id, hour, minute
FROM
    flights
WHERE
    year = 2024 AND month = 7 AND day = 29
        AND origin_airport_id = (SELECT
            id
        FROM
            airports
        WHERE
            city = 'Fiftyville');
-- The earliest flight is 8:20am and its ID is 36


-- This query is to get the destination airport and city to where the thief ran
SELECT
    full_name, city
FROM
    airports
        JOIN
    flights ON airports.id = flights.destination_airport_id
WHERE
    flights.id = 36;
-- LaGuardia Airport, New York City


-- Query to get the list of passports on that flight
SELECT
    passport_number
FROM
    passengers
WHERE
    flight_id = 36;


-- This query is to get the list of all the callers of that day with a call duration less than a minute
SELECT
    caller
FROM
    phone_calls
WHERE
    year = 2024 AND month = 07 AND day = 28
        AND duration < 60;
-- Quite a lot again...
-- I need to take the four list that I have (person_id, passport numbers, phone numbers and license plates) and see them in the people table


-- This query is to get the name of thief by using all of the queries that generated my lists
SELECT
    name
FROM
    people
WHERE
    id IN (SELECT
            person_id
        FROM
            bank_accounts
        WHERE
            account_number IN (SELECT
                    account_number
                FROM
                    atm_transactions
                WHERE
                    year = 2024 AND month = 07 AND day = 28
                        AND atm_location = 'Leggett Street'
                        AND transaction_type = 'withdraw'))
            AND phone_number IN (SELECT
                    caller
                FROM
                    phone_calls
                WHERE
                    year = 2024 AND month = 07 AND day = 28
                        AND duration < 60)
            AND passport_number IN (SELECT
                    passport_number
                FROM
                    passengers
                WHERE
                    flight_id = 36)
            AND license_plate IN (SELECT
                    license_plate
                FROM
                    bakery_security_logs
                WHERE
                    year = 2024 AND month = 7 AND day = 28
                        AND hour = 10
                        AND minute BETWEEN 15 AND 25
                        AND activity = 'exit');
-- Bruce's the name

-- This query is to get Bruce's number, so I can get the accomplice using the phone call register
SELECT
    phone_number
FROM
    people
WHERE
    name = 'Bruce';
-- Bruce's number: (367) 555-5533

-- Query to get the accomplice's number
SELECT
    receiver
FROM
    phone_calls
WHERE
    caller = '(367) 555-5533'
        AND year = 2024
        AND month = 07
        AND day = 28
        AND duration < 60;
-- Accomplice's number: (375) 555-8161

-- Query to get the accomplice's name
SELECT
    name
FROM
    people
WHERE
    phone_number = '(375) 555-8161';
-- Accomplice's name: Robin
-- Bruce and Robin? Smart
