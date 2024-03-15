
IF EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'news_source_src' AND TABLE_SCHEMA = 'news'
    )
BEGIN
    DROP TABLE news.news_source_src;
END;        
GO

CREATE TABLE news.news_source_src
	(
    id int IDENTITY(1,1) PRIMARY KEY,
	source_id varchar(max) NULL,
	name varchar(max) NULL,
	url varchar(max) NULL,
	description varchar(max) NULL,
	language varchar(max) NULL,
    country varchar(max) NULL,
	date_extracted datetime DEFAULT GETDATE(),
	source_file_name varchar(max) NULL,
	batch_no int NULL,
	loaded bit DEFAULT '0'
	);
GO
