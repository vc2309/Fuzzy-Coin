var scraperjs = require('scraperjs');
var mysql     = require('mysql');
var async     = require('async');

var connection = mysql.createConnection({
  host     : 'ece457project.chwjf5irbz2p.us-east-2.rds.amazonaws.com',
  user     : 'aiproject2018',
  password : 'aiproject2018',
  database : 'bitcoinproject'
});
 
connection.connect();

// Getting ititial list of articles
scraperjs.StaticScraper.create('https://www.coindesk.com/price/')
    .scrape(function($) {
        return $(".bpi-lower-section a").map(function() {
            return $(this).attr("href");
        }).get();
    })
    .then(function(news) {
        // Getting all of the article information
        startTreck(news[0])
    })

// Scrape all the newest articles on the site
var startTreck = async function(startingArticleLink) {
    var latestArticleTitle;
    var currentScrapedArticleTitle;
    var previousArticleLink;
    var started = false;
    
    // Get the title of the latest article we have in the database
    var latestArticleTitle = await connection.query('SELECT * FROM bitcoinproject.coindesk_articles order by id desc limit 1;', function(err, results) {
         return results[0] ? results[0].title : "No Article";
    })

    async.until(function() {return (currentScrapedArticleTitle == latestArticleTitle) || (!previousArticleLink && started)}, function(callback) {
        started = true;
        console.log("Querying link: " + previousArticleLink || startingArticleLink)
        // Continue scraping the articles until we hit the latest one we have in the database
        scraperjs.StaticScraper.create(previousArticleLink || startingArticleLink)
        .scrape(function($) {
            currentScrapedArticleTitle = $(".article-top-title").text();
            previousArticleLink = $(".previous a").attr("href");
            var articleBody = $(".article-content-container.noskimwords").text().replace(/["']/g, "").replace(/[^\w\s]/gi, '');
            var articleDate = new Date($(".article-container-left-timestamp").text().substring(0, $(".article-container-left-timestamp").text().indexOf('C') + 1).replace(/[^\w\s]/gi, '').replace("at", "")).toISOString().slice(0, 19).replace('T', ' ');

            connection.query('INSERT INTO `bitcoinproject`.`coindesk_articles` (`title`, `body`, `date`) VALUES ("' + currentScrapedArticleTitle + '", "' + articleBody + '", "' + articleDate + '");', function (error, results, fields) {
                if (error) throw error;
                console.log('Article info stored titled: ' + currentScrapedArticleTitle);
            });
    
            return [currentScrapedArticleTitle == latestArticleTitle, previousArticleLink];
        }).then(function(data) {
            callback()
        })
    }, function() {
        console.log("Deleting duplicates");
        connection.query('ALTER IGNORE TABLE `coindesk_articles` ADD UNIQUE (title)', function (error, results, fields) {
            if (error) throw error;
            console.log('Deleted duplicate ');
        });
        console.log('done')
    })
}

