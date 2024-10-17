CREATE TABLE Keywords (
    keyword_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    keyword VARCHAR(155) NOT NULL,
    PRIMARY KEY (keyword_id)
);

CREATE TABLE Data_Storage (
	storage_id BIGINT(20) NOT NULL AUTO_INCREMENT,
  storage_original_filename VARCHAR(255) NOT NULL,
	storage_modified_filename VARCHAR(255) NOT NULL,
	storage_filepath VARCHAR(255) NOT NULL,
  PRIMARY KEY (storage_id)
);

CREATE TABLE Users (
    user_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    storage_id BIGINT(20) NOT NULL,
    user_email VARCHAR(200) NOT NULL,
    user_password VARCHAR(200) NOT NULL,
    user_name VARCHAR(200) NOT NULL,
    user_number VARCHAR(200) NOT NULL,
    user_nickname VARCHAR(200) NOT NULL,
    user_age INT(20),
    PRIMARY KEY (user_id),
    FOREIGN KEY (storage_id) REFERENCES Data_Storage(storage_id),
    UNIQUE(user_email)
);

CREATE TABLE Article (
    article_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    article_title VARCHAR(200) NOT NULL,
    article_content TEXT DEFAULT NULL,
    article_url VARCHAR(200) NOT NULL,
    article_views INT DEFAULT 0,
    article_createat DATE NOT NULL,
    article_like INT DEFAULT 0,
    article_image VARCHAR(200) DEFAULT NULL,
    article_scrap INT DEFAULT 0,
    article_summary TEXT DEFAULT NULL,
    PRIMARY KEY (article_id)
);

CREATE TABLE Community (
    community_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    user_id BIGINT(20) NOT NULL,
    community_title VARCHAR(200) NOT NULL,
    community_content TEXT NOT NULL,
    community_createat DATE NOT NULL,
    community_search INT DEFAULT 0,
    community_like INT DEFAULT 0,
    PRIMARY KEY (community_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE User_Article (
		user_article_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    article_id BIGINT(20) NOT NULL,
    user_id BIGINT(20) NOT NULL,
    user_article_like TINYINT(1) DEFAULT 0,
    user_article_scrap TINYINT(1) DEFAULT 0,
    PRIMARY KEY (user_article_id),
    FOREIGN KEY (article_id) REFERENCES Article(article_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Article_Keyword (
		article_keyword_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    keyword_id BIGINT(20) NOT NULL,
    article_id BIGINT(20) NOT NULL,
    PRIMARY KEY (article_keyword_id),
    FOREIGN KEY (keyword_id) REFERENCES Keywords(keyword_id),
    FOREIGN KEY (article_id) REFERENCES Article(article_id)
);

CREATE TABLE Article_Comments (
    comment_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    user_id BIGINT(20) NOT NULL,
    article_id BIGINT(20) NOT NULL,
    comment_content VARCHAR(200) NOT NULL,
    comment_createat DATE,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (article_id) REFERENCES Article(article_id)
);

CREATE TABLE Community_Comments (
    comment_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    community_id BIGINT(20) NOT NULL,
    user_id BIGINT(20) NOT NULL,
    comment_content VARCHAR(200) NOT NULL,
    comment_createat DATE NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (community_id) REFERENCES Community(community_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

CREATE TABLE Deleted_Users (
    deleted_user_id BIGINT(20) NOT NULL AUTO_INCREMENT,
    storage_id BIGINT(20) NOT NULL,
    deleted_user_email VARCHAR(200) NOT NULL,
    deleted_user_password VARCHAR(200) NOT NULL,
    deleted_user_name VARCHAR(200) NOT NULL,
    deleted_user_number VARCHAR(200) NOT NULL,
    deleted_user_nickname VARCHAR(200) NOT NULL,
    deleted_user_age INT(20),
    PRIMARY KEY (deleted_user_id),
    FOREIGN KEY (storage_id) REFERENCES Data_Storage(storage_id),
    UNIQUE(deleted_user_email)
);

CREATE TABLE Community_Data(
		community_data_id BIGINT(20) NOT NULL AUTO_INCREMENT,
		storage_id BIGINT(20) NOT NULL,
		community_id BIGINT(20) NOT NULL,
    PRIMARY KEY (community_data_id),
    FOREIGN KEY (storage_id) REFERENCES Data_Storage(storage_id),
    FOREIGN KEY (community_id) REFERENCES Community(community_id)
);

INSERT INTO Keywords (keyword) VALUES ('정치'); 
INSERT INTO Keywords (keyword) VALUES ('경제'); 
INSERT INTO Keywords (keyword) VALUES ('사회'); 
INSERT INTO Keywords (keyword) VALUES ('과학'); 
INSERT INTO Keywords (keyword) VALUES ('연예'); 
INSERT INTO Keywords (keyword) VALUES ('스포츠'); 