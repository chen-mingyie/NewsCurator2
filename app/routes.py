from app import app
from flask import request, Markup, render_template, jsonify, session
from app.business import cf_data
from app.model.user_preferences import UserPreferences, UserPreferencesSchema
from app.model.topics import Topics
from app.model.news_topics import NewsTopics
from app.model.interest_levels import InterestLevels
from app.model.countries import Countries
from app import db
from app.business.process_news_articles import ProcessNewsArticles

users = []

@app.route('/userPreferences', methods = ['POST'])
def createUserPreferences():
    user_id = UserPreferencesSchema().load(request.get_json())
    print(user_id)
    #showNewsArticles()
    return jsonify(userId = user_id), 200

@app.route("/userProfile", methods=["GET"])
def showUserProfile():
    news_topics = [i.value for i in NewsTopics]
    general_preferences = [i.generalPreferences for i in InterestLevels]
    topic_preferences = [i.topicPreferences for i in InterestLevels]
    source_preferences = [i.sourcePreferences for i in InterestLevels]

    #Need to modify this once we retrieve record from database using username
    userprofile = None
    userprofileJson = "null" if userprofile == None else userprofile.getJsonStr()

    return render_template("user_profile.html", newsTopics=Markup(news_topics),
                           topicPref=Markup(topic_preferences), generalPref=Markup(general_preferences),
                           srcPref=Markup(source_preferences), countries=Markup(Countries.getCountries()),
                           userprofile=Markup(userprofileJson), userEmail=app.newsapp_active_user)

@app.route("/newsarticles", methods = ["GET", "POST"])
def showNewsArticles():
        user_id = request.args.get('id')
        user_profile = UserPreferences.query.filter_by(id=user_id).first()
        print(user_profile.user_name)
        if user_profile != None:
            newsArticles = ProcessNewsArticles().fetchNewsArticles(user_profile)
            articlesJson = ProcessNewsArticles().rankNewsArticles(user_profile, newsArticles)
        else:
            articlesJson = "null"

        return render_template("newsarticles.html", articles=Markup(articlesJson), userEmail=app.newsapp_active_user)

@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def showLogin():
    if request.method == "POST":
        if request.form["submitBtn"] == "signIn":
            session["USEREMAIL"] = request.form["email"]
            app.newsapp_active_user = session["USEREMAIL"]
        elif request.form["submitBtn"] == "signOut":
            session.pop("USEREMAIL", None)
            app.newsapp_active_user = ""

    return render_template("login.html", userEmail=app.newsapp_active_user)