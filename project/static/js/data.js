function plot_test() {

    const toTimestamp = (strDate) => {
        const dt = Date.parse(strDate);
        return dt / 1000;
    }

    const getActivityData = async () => {
        const request = await fetch("http://wasgehtup.com/app_users");
        const data = await request.json();
        return data;
    };

    var activity = [];

    getActivityData().then(activityData => {
        for (let i = 0; i < activityData.length; i++) {
            activity.push([toTimestamp(activityData[i].date), activityData[i].users]);
        }
        $.plot("#activity", [activity], { xaxis: { mode: 'time', timeformat: '%Y-%m-%d' } });
    });
    console.log("activity", activity);

    const getScrapedData = async () => {
        const request = await fetch("http://wasgehtup.com/events_scraped?city=0");
        const data = await request.json();
        return data;
    };

    var scrape_count = [];

    getScrapedData().then(scrapeData => {
        orga = scrapeData[0].orga_id;
        i = 0
        while (true) {
            temp = [];
            while (scrapeData[i].orga_id == orga) {
                temp.push([toTimestamp(scrapeData[i].date), scrapeData[i].number]);
                i++;
                if (i >= scrapeData.length) break;
            }
            scrape_count.push(temp);
            if (i >= scrapeData.length) break;
            orga = scrapeData[i].orga_id
        }
        console.log("scrape_count", scrape_count);
        $.plot("#scrape_count", scrape_count, { xaxis: { mode: 'time', timeformat: '%Y-%m-%d' } });
    });


}

// Add the Flot version string to the footer

// $("#footer").prepend("Flot " + $.plot.version + " &ndash; "); 