#include "ContentExtractor.h"

ContentExtracter::ContentExtracter(const cpr::Url& url) : m_url(url)
{
}

std::string ContentExtracter::getContent()
{
    cpr::Response response = cpr::Get(m_url);

    return response.text;
}