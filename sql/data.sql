PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('awdeorio', 'Andrew DeOrio', 'awdeorio@umich.edu',
'e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e'),
('jflinn', 'Jason Flinn', 'jflinn@umich.edu',
'505083b8b56c97429a728b68f31b0b2a089e5113.jpg', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e'),
('michjc', 'Michael Cafarella', 'michjc@umich.edu',
'5ecde7677b83304132cb2871516ea50032ff7a4f.jpg', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e'),
('jag', 'H.V. Jagadish', 'jag@umich.edu',
'73ab33bd357c3fd42292487b825880958c595655.jpg', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e');

INSERT INTO posts(postid, filename, owner)
VALUES (1, '122a7d27ca1d7420a1072f695d9290fad4501a41.jpg', 'awdeorio'),
(2, 'ad7790405c539894d25ab8dcf0b79eed3341e109.jpg', 'jflinn'),
(3, '9887e06812ef434d291e4936417d125cd594b38a.jpg', 'awdeorio'),
(4, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'jag'),
(5, 'ebb78094ac05e1fc8355a9316647e5eec6dbe2c2.jpg', 'awdeorio'),
(6, 'a370e82001a533f8874f64adc18b58143004e0e4.jpg', 'jflinn'),
(7, '8ce376b4c7854caf626674434d18b56fc31265ce.jpg', 'michjc'),
(8, '805aabe8aad5cab254bdd9e14d74cd660f68e2cd.jpg', 'jflinn'),
(9, 'e261436095a14f0d5c0d39d42a01b7d4b6cd16e6.jpg', 'awdeorio'),
(10, '2ec7cf8ae158b3b1f40065abfb33e81143707842.jpg', 'jflinn');

INSERT INTO following(username1, username2)
VALUES ('awdeorio', 'jflinn'),
('awdeorio', 'michjc'),
('jflinn', 'awdeorio'),
('jflinn', 'michjc'),
('michjc', 'awdeorio'),
('michjc', 'jag'),
('jag', 'michjc');

INSERT INTO comments(commentid, owner, postid,text)
VALUES (1,'awdeorio',3,'#chickensofinstagram'),
(2,'jflinn',3,'I <3 chickens'),
(3,'michjc',3,'Cute overload!'),
(4,'awdeorio',2,'Sick #crossword'),
(5,'jflinn',1,'Walking the plank #chickensofinstagram'),
(6,'awdeorio',1,'This was after trying to teach them to do a #crossword'),
(7,'jag',4,'Saw this on the diag yesterday!');

INSERT INTO likes(owner, postid)
VALUES ('awdeorio', 1),
('michjc', 1),
('jflinn', 1),
('awdeorio', 2),
('michjc', 2),
('awdeorio', 3);