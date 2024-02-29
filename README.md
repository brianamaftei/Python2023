# Python2023

### Advanced RSync Project

This Python script is designed to keep two different file locations synchronized. Each location is specified in a particular format:

- **FTP**: `ftp:user:password@URL/a.b.c`
- **ZIP Archive**: `zip:C:\abc\d.zip`
- **Local Folder**: `folder:C:\aaa`

### Operation

The script runs continuously and keeps the two locations synchronized in the following ways:

- If a file is created in one location, it is duplicated in the other location.
- If a file is deleted from one location, it is also deleted from the other location.
- If a file is modified in one location, the modification is copied to the other location.

### Initial Synchronization

Upon initial startup, synchronization occurs as follows:

- If a file exists only in one location, it is copied to the other location.
- If the same file exists in both locations but there are differences, the most recent file (based on the last modified time) from one location is copied to the other.
