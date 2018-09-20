USE [BHBackupRestore]
GO

SELECT [class_name]
      ,[attr_name]
      ,[attr_descript]
  FROM [dbo].[DICTIONARY]
  WHERE 
  class
  attr_descript IS NOT NULL 
  AND attr_descript NOT LIKE 'Internal identifier for %'
  AND attr_descript NOT LIKE 'Row timestamp'
  AND attr_descript NOT LIKE 'Set of %'
  AND attr_descript NOT LIKE 'Date/time row was updated'
  AND attr_descript NOT LIKE 'Name of user who updated row'
  AND attr_descript NOT LIKE 'Autotrak specific data'
GO


