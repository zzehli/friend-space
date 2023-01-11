PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password)
VALUES ('awd', 'Andrew Wasseman', 'awd@aol.com',
'avatar-m1.png', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e'),
('jrl', 'Jeremy Lynn', 'rly@aol.com',
'avatar-m2.png', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e'),
('micc', 'Michel Cafferry', 'mcf@aol.com',
'avatar-f2.png', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e'),
('wed', 'Wednesday', 'wed@aol.com',
'avatar-f1.png', 'sha512$46412293bb8745dd8ac8e3c0a06e9b0b$6a35e53dea1332930fb3e119353d9ef76061f5992dfedad9dd97ed275e373d6a5a8b14df87c9f9ec15bdc54a0c9922301d6668b8a4945e55debd4523ff1c521e');

INSERT INTO posts(postid, filename, owner)
VALUES (1, 'cameron-webber-ElS12fggAjs-unsplash.jpg', 'awd'),
(2, 'documerica-28sD7FV-8Ug-unsplash.jpg', 'jrl'),
(3, 'mat-napo-nRaEy1IHHWk-unsplash.jpg', 'awd'),
(4, 'marek-piwnicki-UKE05Ty97xE-unsplash.jpg', 'wed'),
(5, 'krisjanis-kazaks-KFA2Ex2JGfQ-unsplash.jpg', 'micc'),
(6, 'sam-goodgame-yZaUaEE8psQ-unsplash.jpg', 'jrl'),
(7, 'documerica-FIA9Nz0y3qo-unsplash.jpg', 'jrl');


INSERT INTO following(username1, username2)
VALUES ('awd', 'jrl'),
('awd', 'micc'),
('jrl', 'awd'),
('jrl', 'micc'),
('micc', 'awd'),
('micc', 'wed'),
('wed', 'micc');

INSERT INTO comments(commentid, owner, postid,text)
VALUES (1,'awd',3,'#québec'),
(2,'jrl',3,'majestic!'),
(3,'micc',3,'want to go!'),
(4,'awd',2,'flea market yesterday'),
(5,'jrl',1,'ready to move.'),
(6,'awd',1,'good luck!'),
(7,'wed',4,'Saw this on the diag yesterday!');

INSERT INTO likes(owner, postid)
VALUES ('awd', 1),
('micc', 1),
('jrl', 1),
('awd', 2),
('micc', 2),
('awd', 3);