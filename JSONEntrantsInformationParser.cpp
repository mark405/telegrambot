#include "JSONEntrantsInformationParser.h"


JSONEntrantsInformationParser::JSONEntrantsInformationParser(const std::string& JSONString) : m_data(nlohmann::json::parse(JSONString))
{

}


void JSONEntrantsInformationParser::apostropheDelete(std::string& word)
{
    /*
            if (word.find("'") != std::string::npos)
    {
        word.erase(word.find("'"), 1);
    }
    */
    std::string apostrophe = "'";
    int lengthOfWord = word.length();
    for (int i = 0; i < lengthOfWord; i++) {
        if (word[i] == apostrophe[0])
            word.erase(i, 1);
    }

}


void JSONEntrantsInformationParser::insertParsedData(DataBase& dataBase)
{
    std::string city = "";
    std::string university = "";
    size_t numberOfEntrants = m_data["entrants"].size();
    if (numberOfEntrants < 1)
    {
        std::cout << "SKIP";
        return;
    }
    if (m_data["university"]["region"]["name"].is_null() && m_data["university"]["name"].is_null())
    {
        city = "Невідомо";
        university = "Невідомо";
    }

    city = m_data["university"]["region"]["name"];
    apostropheDelete(city);
    university = m_data["university"]["name"];
    apostropheDelete(university);
    std::string degree = m_data["studyDegree"];
    apostropheDelete(degree);
    std::string speciality = m_data["name"];
    apostropheDelete(speciality);
    std::string faculty = m_data["facultyName"];
    apostropheDelete(faculty);
    std::string program = m_data["educationalProgram"];
    apostropheDelete(program);
    std::string specialityNumber = m_data["specialityNumber"];
    speciality = specialityNumber + " " + speciality;

    std::cout << speciality << " " << university << "";

    for (size_t i = 0; i < numberOfEntrants; i++)
    {
        std::string name = m_data["entrants"][i]["name"];
        apostropheDelete(name);

        std::string status = m_data["entrants"][i]["status"];
        apostropheDelete(program);

        int number = m_data["entrants"][i]["number"];

        int prioity = m_data["entrants"][i]["prioity"];

        double score = m_data["entrants"][i]["score"];

        int year = m_data["entrants"][i]["year"];

        std::string insertionCommand = "INSERT INTO TWO (CITY,UNIVERSITY,NAME,STATUS,NUMBER,PRIOITY,SCORE,DEGREE, SPECIALITY, FACULTY, PROGRAM, YEAR) "  \
            "VALUES ('" + city + "','" + university + "','" + name + "', '" + status +
            "'," + std::to_string(number) + ", " + std::to_string(prioity) +
            "," + std::to_string(score) + ", '" + degree + "', '" + speciality +
            "', '" + faculty + "', '" + program + "'," + std::to_string(year) + " ); ";


        dataBase.executeSQLCommand(insertionCommand);

    }
}