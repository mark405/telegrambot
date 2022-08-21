//main
#include "ContentExtractor.h"
#include "DataBase.h"
#include "JSONEntrantsInformationParser.h"

/*
using json = nlohmann::json;


class DataBase
{
private:
    sqlite3* m_db;
    int m_result;
    std::string m_nameOfDataBase;
    char* errorMessage;
public:
    DataBase(const std::string& nameOfDataBase) : m_nameOfDataBase(nameOfDataBase), errorMessage(0)
    {
        m_result = sqlite3_open(m_nameOfDataBase.c_str(), &m_db);
        if (m_result)
        {
            throw std::exception("can not open databse\n");
        }
    }
    ~DataBase()
    {
        sqlite3_close(m_db);
    }
    void executeSQLCommand(const std::string& SQLCommand)
    {
        m_result = sqlite3_exec(m_db, SQLCommand.c_str(), callback, 0, &errorMessage);
        if (m_result != SQLITE_OK)
        {
            std::cout << errorMessage;
            sqlite3_free(errorMessage);

        }

    }

    static int callback(void* data, int argc, char** argv, char** azColName)
    {
        //std::cerr << (const char*)data;
        for (int i = 0; i < argc; i++) {
            std::cout << azColName[i] << " = " << (argv[i] ? argv[i] : "NULL") << std::endl;
        }
        std::cout << std::endl;

        return 0;
    }
};


class ContentExtracter
{
private:

    cpr::Url m_url;
    cpr::Response response;
public:
    ContentExtracter(const cpr::Url &url): m_url(url)
    {
    }

    std::string getContent()
    {
        cpr::Response response = cpr::Get(m_url);

        return response.text;
    }
};


class JSONEntrantsInformationParser
{
private:
    json m_data;
public:
    JSONEntrantsInformationParser(const std::string& JSONString) : m_data(json::parse(JSONString))
    {

    }
    void apostropheDelete(std::string& word)
    {

        std::string apostrophe = "'";
        int lengthOfWord = word.length();
        for (int i = 0; i < lengthOfWord; i++) {
            if (word[i] == apostrophe[0])
                word.erase(i, 1);
        }

    }
    void insertParsedData(DataBase& dataBase)
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
};

*/
int main()
{
    std::system("chcp 65001>>null");

    try
    {
        DataBase db("C:/Users/User/source/repos/sqliteexample/test2.db");

        std::string droppingSqlCommand = "DROP TABLE IF EXISTS TWO";
        db.executeSQLCommand(droppingSqlCommand);

        std::string sqlCommand = "CREATE TABLE IF NOT EXISTS TWO ("  \
            "CITY           TEXT    NOT NULL," \
            "UNIVERSITY     TEXT    NOT NULL," \
            "NAME           TEXT    NOT NULL," \
            "STATUS         TEXT    NOT NULL," \
            "NUMBER         INT     NOT NULL," \
            "PRIOITY        INT     NOT NULL," \
            "SCORE          REAL    NOT NULL," \
            "DEGREE         TEXT    NOT NULL," \
            "SPECIALITY     TEXT    NOT NULL," \
            "FACULTY        TEXT    NOT NULL," \
            "PROGRAM        TEXT    NOT NULL," \
            "YEAR           INT     NOT NULL);";

        db.executeSQLCommand(sqlCommand);

        for (size_t i = 281215; i <= 281215; ++i)
        {
            std::string specialityLink = "https://abit-help.com.ua/api/speciality/" + std::to_string(i);

            ContentExtracter entrantExtractor(specialityLink);
            std::string entrantContent = entrantExtractor.getContent();
            try
            {
                JSONEntrantsInformationParser entrantsInformationParser(entrantContent);
                entrantsInformationParser.insertParsedData(db);
            }
            catch (const std::exception& ex)
            {
                std::cout << ex.what() << "\n\n" << i;
            }
            std::cout << i << std::endl;
        }
    }
    catch (const std::exception& ex)
    {
        std::cout << ex.what() << "\n";
        return 1;
    }

    

    
    //std::system("chcp 1251");

    //std::string s = "SELECT NAME FROM ENTRANTS WHERE NAME = 'Тімощенко В.А.'";

    //std::cout << s;
    //std::system("chcp 65001>>null");

    //db.executeSQLCommand(s);
   
    return 0;
}

