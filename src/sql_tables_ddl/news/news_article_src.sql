
IF EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'news_article_src' AND TABLE_SCHEMA = 'news'
    )
BEGIN
    DROP TABLE news.news_article_src;
END;        
GO

CREATE TABLE news.news_article_src
	(
    id int IDENTITY(1,1) PRIMARY KEY,
	article_id varchar(max) NULL,
	title varchar(max) NULL,
	link varchar(max) NULL,
	content varchar(max) NULL,
	publication_date datetime NULL,
    source_id varchar(max) NULL,
    source_country varchar(max) NULL,
    article_language varchar(max) NULL,
	date_extracted datetime DEFAULT GETDATE(),
	source_file_name VARCHAR(256) NULL,
	batch_no int NULL,
	loaded bit DEFAULT '0'
	);
GO
