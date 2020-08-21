function convertJson() {
    event.preventDefault();
    var userProfileObject = Object();
    userProfileObject.userCountry = $('select[name="country"]').children("option:selected").val();
    userProfileObject.userName = "chandra";
    userProfileObject.userEmail = document.getElementsByClassName('form-control email')[0].value;
    userProfileObject.userPassword = "test";
    userProfileObject.topicsRelatedToProfession = populateProfessionalTopicsObject();
    userProfileObject.topicsRelatedToLeisure = populateLeisureTopicsObject();
    userProfileObject.timeToRead = document.getElementsByClassName('form-control readingTime')[0].value;
    userProfileObject.age = document.getElementsByClassName('form-control age')[0].value;
    userProfileObject.oldNewsInterest = document.getElementsByClassName('form-control general')[0].value;
    userProfileObject.localNewsInterest = document.getElementsByClassName('form-control general')[1].value;
    userProfileObject.popularTweetsInterest = document.getElementsByClassName('form-control general')[2].value;
    userProfileObject.newsSourcePreferences = populateNewsSourcePreferences();
    var userProfileObjectJson = JSON.stringify(userProfileObject);
    console.log(userProfileObjectJson);
    var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
    xmlhttp.open("POST", "/userPreferences");
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.send(userProfileObjectJson);
    xmlhttp.onreadystatechange = function()
    {
        console.log("Entered");
        if (xmlhttp.readyState == 4)
        {
            var obj = JSON.parse(xmlhttp.responseText);
            console.log('userid=' + obj['userId']);
            //getArticleApi = "http://localhost:5000/newsarticles?id="+ obj['userId'];
            getArticleApi = "https://mr-ay2021-newscurator.herokuapp.com/newsarticles?id="+ obj['userId'];
            console.log(getArticleApi);
            window.location.href = getArticleApi;
        }
    };
}

function populateProfessionalTopicsObject() {
    var topicsLength = document.getElementsByClassName('form-control topics').length;
    var topicsRelatedToProfession = []
    for (var i = 0; i < topicsLength; i++) {
        if (document.getElementsByClassName('form-control topics')[i].name.includes('work_')) {
            var topicDetails = Object();
            topicDetails.topicName = document.getElementsByClassName('form-control topics')[i].name.replace('work_','');
            topicDetails.userInterestLevels = document.getElementsByClassName('form-control topics')[i].value;
            topicsRelatedToProfession.push(topicDetails)
        }
    }
    return topicsRelatedToProfession;
}

function populateLeisureTopicsObject() {
    var topicsLength = document.getElementsByClassName('form-control topics').length;
    var topicsRelatedToLeisure = []
    for (var i = 0; i < topicsLength; i++) {
        if (document.getElementsByClassName('form-control topics')[i].name.includes('leis_')) {
            var topicDetails = Object();
            topicDetails.topicName = document.getElementsByClassName('form-control topics')[i].name.replace('leis_','');
            topicDetails.userInterestLevels = document.getElementsByClassName('form-control topics')[i].value;
            topicsRelatedToLeisure.push(topicDetails)
        }
    }
    return topicsRelatedToLeisure;
}

function populateNewsSourcePreferences() {
    var newsSourceLength = document.getElementsByClassName('form-control source').length;
    var newsSourcePreferences = []
    for (var i = 0; i < newsSourceLength; i++) {
        var newsSource = Object();
        newsSource.newsSourceName = document.getElementsByClassName('form-control source')[i].name.replace('src_','');
        newsSource.userInterestLevels = document.getElementsByClassName('form-control source')[i].value;
        newsSourcePreferences.push(newsSource)
        
    }
    return newsSourcePreferences;
}

function setUserprofile(aUserProfileJSON)
{
    if(aUserProfileJSON != null)
    {
//        "id": 6245014289670372232,
//        "leisureTopics":
//        {
//            "Business": "NotSure",
//            "Science": "NotSure",
//            ...
//        },
//        "workTopics":
//        {
//            "Business": "NotSure",
//            "Science": "NotSure",
//            ...
//        },
//        "readingTimePref": 5,
//        "age": 18,
//        "pastNewsPref": "NoPreference",
//        "LocalNewsPref": "NoPreference",
//        "TrendingPref": "NoPreference",
//        "sourcePref":
//        {
//            "CNA": "NoPreference",
//            "The Straits Times": "NoPreference",
//            ...
//        }

        var profile = aUserProfileJSON;

        // set user email
        $(".form-control.email").val(profile.userEmail);

        // set user age
        $(".form-control.age").val(profile.age);

        // set work topic preferences
        for(var topic in profile.workTopics)
        {
            $('select[name="work_' + topic + '"]').val(profile.workTopics[topic]);
        }

        // set leisure topic preferences
        for(var topic in profile.leisureTopics)
        {
            $('select[name="leis_' + topic + '"]').val(profile.leisureTopics[topic]);
        }

        // set reading time
        $(".form-control.readingTime").val(profile.readingTimePref);

        // set see past news pref
        $('select[name="pastNewsPref"]').val(profile.pastNewsPref);

        // set see local news pref
        $('select[name="localNewsPref"]').val(profile.LocalNewsPref);

        // set see trending news pref
        $('select[name="trendingNewsPref"]').val(profile.TrendingPref);

        // set user country
        $('select[name="country"]').children("option:selected").val(profile.country);

        // set news source preferences
        for(var source in profile.sourcePref)
        {
            $('select[name="src_' + source + '"]').val(profile.sourcePref[source]);
        }
    }
}

