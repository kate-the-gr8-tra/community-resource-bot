

CREATE TABLE IF NOT EXISTS Servers(
	server_id TEXT PRIMARY KEY,
	server_name TEXT,
	join_date datetime DEFAULT CURRENT_TIMESTAMP	
);


CREATE TABLE IF NOT EXISTS Users(
	user_id TEXT PRIMARY KEY,
	username TEXT NOT NULL,
	server_id TEXT NOT NULL,
	name TEXT,
	pronouns TEXT,
	age INTEGER,
	registration_date datetime DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (server_id) REFERENCES Servers(server_id)
);
