from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException

from app.business import cf_data
from app.model.news_article import NewsArticle
from app.business.news_rules_engine import NewsRuleEngine
from app.business.keyword_matcher import KeywordMatcher
from app.model.news_topics import NewsTopics
from app.model.user_preferences import UserPreferences
from app.model.countries import Countries
from datetime import datetime, date
from typing import Dict
from pytrends.request import TrendReq

class ProcessNewsArticles:
    def __init__(self):
        self.__userProfilesDB = {}
        self.__keywordMatcher = None
        self.__newsapiKey = 'fd9342e6dd8e4a0b97bab8e760382743' #'7580ffe71bec47f7acfe7ea22d3520cc'

    def calculateAgeOfNews(self, currentHeadlines):
        publishedAt = currentHeadlines["publishedAt"].split('T')[0]
        publishedYear = int(publishedAt.split('-')[0])
        publishedMonth = int(publishedAt.split('-')[1])
        publishedDate = int(publishedAt.split('-')[2])
        publishedFullDate = date(publishedYear, publishedMonth, publishedDate)
        today = datetime.utcnow().date()
        delta = today - publishedFullDate
        return delta.days

    def createNewsArticleObjects(self, headlines, topic_name, isLocalNews, isTrendingNews):
        articles = []
        for i in range(len(headlines)):
            currentHeadlines = headlines[i]
            daysOld = self.calculateAgeOfNews(currentHeadlines)
            article = NewsArticle(i, currentHeadlines["url"], currentHeadlines["title"], currentHeadlines["description"], currentHeadlines["source"]["name"],
                                  topic_name, daysOld, isTrendingNews, isLocalNews, currentHeadlines["content"])
            article.processArticle()

            # shifted this to rankNewsArticles() so that only the top 10 articles will be downloaded,
            # this improves speed but its traded off with articles tagged using truncated content
            # ------------------------------------------------------------------------------------------
            matchScore = self.__keywordMatcher.computeMatchingScore(article.content)
            article.isLocalNews = (matchScore > 0.002)
            # ------------------------------------------------------------------------------------------

            articles.append(article)
        return articles

    def fetchTrendingStories(self):
        newsapi = NewsApiClient(api_key = self.__newsapiKey)
        articles=[]
        pytrend = TrendReq()
        df = pytrend.trending_searches()
        latestTrends = df[0].values.tolist()
        for trend in latestTrends[:5]:
            trending_news = newsapi.get_everything(q=trend,
                                                   page_size=1)
            articles.extend(self.createNewsArticleObjects(trending_news["articles"], "Trending", False, True))
        return articles

    # download articles from websites base on user's profile
    def fetchNewsArticles(self, user_preferences: UserPreferences, aProcessArticles: bool = True) -> [NewsArticle]:
        # this is sample to download from one source
        articles = []
        self.__keywordMatcher = KeywordMatcher(Countries.getCountries()[user_preferences.country])
        newsapi = NewsApiClient(api_key = self.__newsapiKey)
        print(user_preferences.topics[0].topic_name)

        try:
            for index, topic in enumerate(user_preferences.topics):
                topic_name = topic.topic_name
                country = user_preferences.country
                topic_type = topic.topic_type
                if (topic_type == 'Profession'):
                    top_headlines = newsapi.get_top_headlines(category=topic_name.lower(),
                                                              country='us',
                                                              page_size=2)

                    articles.extend(self.createNewsArticleObjects(top_headlines["articles"], topic_name, False, False))

                    top_local_headlines = newsapi.get_top_headlines(category=topic_name.lower(),
                                                                    country=country,
                                                                    page_size=2)
                    for headline in top_local_headlines["articles"]: # remove duplicated articles
                        duplicate = False
                        for article in articles:
                            if article.title == headline['title']:
                                duplicate = True
                                break
                        if not duplicate:
                            articles.extend(self.createNewsArticleObjects([headline], topic_name, True, False))

            articles.extend(self.fetchTrendingStories())
        except (ValueError, TypeError, NewsAPIException) as e:
            content = e.args[0] if isinstance(e, ValueError) or isinstance(e, TypeError) else e.get_message()
            article = NewsArticle(0, "", "API Error", "Error", "NewsAPI", NewsTopics.GENERAL.name, 0, False, False)
            article.keywords = [content]
            articles = [article]
        return articles

    def rankNewsArticles(self, aUserprofile: UserPreferences, aNewsArticles: [NewsArticle]) -> [str]:
        for i in range(len(aNewsArticles)):
            article = aNewsArticles[i]
            NewsRuleEngine.fireAllRules(aUserprofile, article)

        aNewsArticles.sort(key=lambda x: x.cf, reverse=True)

        articlesJson = []
        for i in range(0, min(10, len(aNewsArticles))):
            #aNewsArticles[i].processArticle()
            articlesJson.append(aNewsArticles[i].getJsonStr())

        return articlesJson

    def getUserprofile(self, aUserId: int) -> UserPreferences:
        return self.__userProfilesDB[aUserId]

    def getFirstProfile(self) -> UserPreferences:

        if len(self.__userProfilesDB) > 0:
            userprofile = self.__userProfilesDB[next(iter(self.__userProfilesDB))]
        else:
            userprofile = None

        return userprofile

    @property
    def userprofileDB(self) -> Dict[int, UserPreferences]: return self.__userProfilesDB