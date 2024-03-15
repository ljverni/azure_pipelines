
USE CaratacoDW;
GO

--DROP TABLE audit.source;
--GO

CREATE TABLE audit.source
	(
  id int IDENTITY(1, 1) PRIMARY KEY,
  name varchar(256) NOT NULL,
  active bit DEFAULT '0',
  date_added datetime DEFAULT GETDATE()
	);	
GO

