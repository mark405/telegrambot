#include "DataBase.h"

DataBase::DataBase(const std::string& nameOfDataBase) : m_nameOfDataBase(nameOfDataBase), errorMessage(0)
{
    m_result = sqlite3_open(m_nameOfDataBase.c_str(), &m_db);
    if (m_result)
    {
        throw std::exception("can not open databse\n");
    }
}
DataBase::~DataBase()
{
    sqlite3_close(m_db);
}
void DataBase::executeSQLCommand(const std::string& SQLCommand)
{
    m_result = sqlite3_exec(m_db, SQLCommand.c_str(), callback, 0, &errorMessage);
    if (m_result != SQLITE_OK)
    {
        std::cout << errorMessage;
        sqlite3_free(errorMessage);

    }

}

int DataBase::callback(void* data, int argc, char** argv, char** azColName)
{
    //std::cerr << (const char*)data;
    for (int i = 0; i < argc; i++) {
        std::cout << azColName[i] << " = " << (argv[i] ? argv[i] : "NULL") << std::endl;
    }
    std::cout << std::endl;

    return 0;
}
