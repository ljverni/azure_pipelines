
USE CaratacoDW;
GO

IF EXISTS (
    SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'etl_log' AND TABLE_SCHEMA = 'audit'
    )
    BEGIN
        DROP TABLE audit.etl_log;
END;
GO


CREATE TABLE audit.etl_log 
	(
  execution_date datetime NOT NULL,
  elapsed_time float NOT NULL,
  script_path varchar(256) NOT NULL,
  log_level varchar(20) NOT NULL,
  msg varchar(256) NOT NULL,
  row_count int NOT NULL,
  batch_no int NOT NULL,
  PRIMARY KEY (execution_date, script_path)
	);	
GO

