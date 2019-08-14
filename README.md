# SVN History database reader
 Small tool to read the **SVN** database to see the commit history.
 
 if you wanted to edit the output data, just change the select query
 
```sql
select local_relpath,kind, changed_author, checksum from NODES

```
**sqlite3** module must be installed, and you'll be good to go.

[![svn](https://raw.githubusercontent.com/Alaa-abdulridha/SVN-reader/master/svnreader.png "svn")](https://raw.githubusercontent.com/Alaa-abdulridha/SVN-reader/master/svnreader.png "svn")
