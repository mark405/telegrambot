#pragma once

#include "cpr/cpr.h"
#include <string>

class ContentExtracter
{
private:

    cpr::Url m_url;
    cpr::Response response;
public:
    ContentExtracter(const cpr::Url& url);

    std::string getContent();
};

