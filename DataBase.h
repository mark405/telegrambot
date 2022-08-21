#pragma once

#include <sqlite3.h>
#include <string>
#include <iostream>

class DataBase
{
private:
    sqlite3* m_db;
    int m_result;
    std::string m_nameOfDataBase;
    char* errorMessage;
public:
    DataBase(const std::string& nameOfDataBase);
    ~DataBase();
    void executeSQLCommand(const std::string& SQLCommand);
    static int callback(void* data, int argc, char** argv, char** azColName);
  
};

