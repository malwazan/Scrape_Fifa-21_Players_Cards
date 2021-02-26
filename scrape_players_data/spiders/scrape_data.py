import scrapy
import requests
import json
import urllib3

#### messi id: data-player-resource="117598535"
"""
good = response.xpath("//div[@id='page-info']")
g2 = good.xpath("//@data-player-resource").get()
import requests
resp = requests.get("https://www.futbin.com/21/playerPrices?player=" + g2)
import json
aa = json.loads(resp.text)
aa['117598535']['prices']['xbox']['LCPrice']     // xbox latest
aa['117598535']['prices']['pc']['LCPrice']       // PC latest
aa['117598535']['prices']['ps']['LCPrice']       // PS latest
"""

class ScrapeDataSpider(scrapy.Spider):
    name = 'scrape_data'
    page_number = 2

    urls = ["https://www.futbin.com/players?page={}".format(x) for x in range(1,637)]

    start_urls = urls
    #"https://www.futbin.com/players?page=2"

    def parse(self, response):

        links = response.xpath("//a[@class='player_name_players_table']/@href").extract()
        complete_links = [response.urljoin(link) for link in links]
        
        print(len(complete_links))

        for link in complete_links:
            yield response.follow(url=link, callback = self.parse_player_data, meta = {"link" : link})
        
        """
        # go to next page
        next_page = ["https://www.futbin.com/players?page={0}".format(ScrapeDataSpider.page_number)] 
        if ScrapeDataSpider.page_number <= 636:
            ScrapeDataSpider.page_number += 1
            yield response.follow(next_page, callbacks=self.parse)
        """


    def parse_player_data(self, response):
        
        # get link from meta
        link = response.request.meta['link']

        #######################
        #PRICES WILL GO HERE
        player_info = response.xpath("//div[@id='page-info']")
        player_id = player_info.xpath("//@data-player-resource").get()
        prices_link = "https://www.futbin.com/21/playerPrices?player=" + player_id
        #######################

        # attributes columns
        cols = response.xpath("//td[@class='table-row-text']")

        Name = cols[0].xpath("text()").get()
        Name = Name.encode('UTF-8')

        Club = cols[1].xpath(".//a/text()").get()
        Club = Club.encode('UTF-8')

        Nation = cols[2].xpath(".//a/text()").get()

        League = cols[3].xpath(".//a/text()").get()
        League = League.encode('UTF-8')

        Skills = cols[4].xpath("text()").get()

        Weak_Foot = cols[5].xpath("text()").get()

        Intl_Rep = cols[6].xpath("text()").get()

        Foot = cols[7].xpath("text()").get()

        Height = cols[8].xpath("text()").get()

        Weight = cols[9].xpath("text()").get()

        Revision = cols[10].xpath("text()").get()

        Def_WR = cols[11].xpath("text()").get()

        Att_WR = cols[12].xpath("text()").get()

        Added_on = cols[13].xpath("text()").get()
        
        Origin = cols[14].xpath('normalize-space(.//a/text())').get()

        R_Face_temp = cols[15].xpath(".//i/@class").get()
        if "icon-checkmark" in R_Face_temp:
            R_Face = "true"
        elif "icon-cross" in R_Face_temp:
            R_Face = "false"
        else:
            R_Face = None

        B_Type = cols[16].xpath("normalize-space(text())").get()

        #DOB = cols[17].xpath('normalize-space(.//a/text())').get()
        DOB_temp = cols[17].css("a::attr(title)").get()
        DOB = '-'.join(DOB_temp.split("-")[1:]).strip()

        
        full_data = {
            "player_id" : player_id,
            "Link" : link,
            "Name" : Name,
            "Club" : Club,
            "Nation" : Nation,
            "League" : League,
            "Skills" : Skills,
            "Weak Foot" : Weak_Foot,
            "Intl. Rep" : Intl_Rep,
            "Foot" : Foot,
            "Height" : Height,
            "Weight" : Weight,
            "Revision" : Revision,
            "Def. WR" : Def_WR,
            "Att. WR" : Att_WR,
            "Added on" : Added_on,
            "Origin" : Origin,
            "R.Face" : R_Face,
            "B.Type" : B_Type,
            "DOB" : DOB
        }
        yield response.follow(prices_link, callback = self.parse_prices, meta = full_data)

    def parse_prices(self, response):

        # get player_id
        player_id = response.request.meta['player_id']
        # get full_data from meta
        link = response.request.meta['Link']
        Name = response.request.meta['Name']
        Club = response.request.meta['Club']
        Nation = response.request.meta['Nation']
        League = response.request.meta['League']
        Skills = response.request.meta['Skills']
        Weak_Foot = response.request.meta['Weak Foot']
        Intl_Rep = response.request.meta['Intl. Rep']
        Foot = response.request.meta['Foot']
        Height = response.request.meta['Height']
        Weight = response.request.meta['Weight']
        Revision = response.request.meta['Revision']
        Def_WR = response.request.meta['Def. WR']
        Att_WR = response.request.meta['Att. WR']
        Added_on = response.request.meta['Added on']
        Origin = response.request.meta['Origin']
        R_Face = response.request.meta['R.Face']
        B_Type = response.request.meta['B.Type']
        DOB = response.request.meta['DOB']

        prices = json.loads(response.text)
        ps4_latest = prices[player_id]['prices']['ps']['LCPrice']
        xbox_latest = prices[player_id]['prices']['xbox']['LCPrice']
        pc_latest = prices[player_id]['prices']['pc']['LCPrice']

        yield {
            "Link" : link,
            "Name" : Name,
            "PS4 Price" : ps4_latest,
            "XBox Price" : xbox_latest,
            "PC Price" : pc_latest,
            "Club" : Club,
            "Nation" : Nation,
            "League" : League,
            "Skills" : Skills,
            "Weak Foot" : Weak_Foot,
            "Intl. Rep" : Intl_Rep,
            "Foot" : Foot,
            "Height" : Height,
            "Weight" : Weight,
            "Revision" : Revision,
            "Def. WR" : Def_WR,
            "Att. WR" : Att_WR,
            "Added on" : Added_on,
            "Origin" : Origin,
            "R.Face" : R_Face,
            "B.Type" : B_Type,
            "DOB" : DOB
        }
