#include <iostream>
#include "cpr/cpr.h"
#include "gumbo.h"


std::string extract_html_page()
{
    cpr::Url url = cpr::Url{ "https://en.wikipedia.org/wiki/Poppy_seed_defence" };
    cpr::Response response = cpr::Get(url);
    return response.text;
}





int main()
{
    std::string page_content = extract_html_page();

    std::cout << page_content;

    return 0;
}

