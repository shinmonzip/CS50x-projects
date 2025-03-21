-- Find incidents that occurred on Humphrey Street
SELECT * FROM crime_scene_reports
WHERE street = 'Humphrey Street'
AND year = 2023 AND month = 7 AND day = 28;

-- Find interviews mentioning the bakery
SELECT * FROM interviews WHERE transcript LIKE '%bakery%'
AND year = 2023 AND month = 7 AND day = 28;

-- Find who exited the bakery within 10 minutes after the crime
SELECT * FROM bakery_security_logs
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- Checking the license plate activity on bakery security logs at the given time.
SELECT p.name, bsl.activity, bsl.license_plate, bsl.year, bsl.month, bsl.day, bsl.hour, bsl.minute
FROM bakery_security_logs bsl
JOIN people p ON p.license_plate = bsl.license_plate
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute BETWEEN 15 AND 25;

-- Checking suspects ATM transactions at Leggett Street (w/ name)
SELECT a.*, p.name FROM atm_transactions a
JOIN bank_accounts b ON a.account_number = b.account_number JOIN people p ON b.person_id = p.id
WHERE a.atm_location = 'Leggett Street' AND a.year = 2023 AND a.month = 7 AND a.day = 28 AND a.transaction_type = 'withdraw';

-- Checking suspect calls lasting up to 1 minute (w/ name)
SELECT p.name, pc.caller, pc.receiver, pc.year, pc.month, pc.day, pc.duration FROM phone_calls pc
JOIN people p ON pc.caller = p.phone_number
WHERE pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration < 60;

-- Finding Fiftyville airport id
SELECT * FROM airports;

-- Checking the flights to determine the flight one day after the crime, as per the witness statement
SELECT f.*, origin.full_name AS origin_airport, destination.full_name AS destination_airport
FROM flights f JOIN airports origin ON f.origin_airport_id = origin.id JOIN airports destination ON f.destination_airport_id = destination.id
WHERE origin.id = 8 AND f.year = 2023 AND f.month = 7 AND f.day = 29 ORDER BY f.hour, f.minute;

-- Checking info from all three witnesses
-- Checking the connections between people, ATM transactions, and phone calls on the day of the crime
SELECT p.name FROM bakery_security_logs bsl JOIN people p ON p.license_plate = bsl.license_plate
JOIN bank_accounts ba ON ba.person_id = p.id JOIN atm_transactions at ON at.account_number = ba.account_number
JOIN phone_calls pc ON pc.caller = p.phone_number
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28 AND bsl.hour = 10 AND bsl.minute BETWEEN 15 AND 25
AND at.atm_location = 'Leggett Street' AND at.year = 2023 AND at.month = 7 AND at.day = 28 AND at.transaction_type IS NOT NULL
AND pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration < 60;

-- Check who is on the earliest flight (Bruce or Diana)
SELECT p.name FROM people p
JOIN passengers ps ON p.passport_number = ps.passport_number
WHERE ps.flight_id = 36
AND p.name IN ('Bruce', 'Diana');

-- Who was the person that Bruce called
SELECT p2.name AS receiver FROM phone_calls pc
JOIN people p1 ON pc.caller = p1.phone_number JOIN people p2 ON pc.receiver = p2.phone_number
WHERE p1.name = 'Bruce' AND pc.year = 2023 AND pc.month = 7 AND pc.day = 28 AND pc.duration < 60;
