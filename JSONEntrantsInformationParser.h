#pragma once

#include <iostream>
#include "nlohmann/json.hpp"
#include "DataBase.h"

class JSONEntrantsInformationParser
{
private:
    nlohmann::json m_data;
public:
    JSONEntrantsInformationParser(const std::string& JSONString);
    void apostropheDelete(std::string& word);
    void insertParsedData(DataBase& dataBase);
};

