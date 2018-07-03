import scrapy

# let's study the python syntax for defining a class
# it is interesing that it has a colon
# there are no curly braces, just indenting
# the name is JobsSpider
# the scrapy.Spider is the base class
# note that we are inheriting from some class called scrapy.Spider
class JobsSpider(scrapy.Spider):
    name = 'jobs3'#attribute reference
    allowed_domains = ['newyork.craigslist.org'] # the bracket is necessary because we are sending a string list, not just a string
    start_urls = ['https://newyork.craigslist.org/d/architect-engineer-cad/search/egr']

    #the main function of the spider
    def parse(self, response):
        #the wrapper from which we will extract other html nodes
        #we use the response to extract the wrapper
        #the '//' means to start from the beginning (<html>) and go until you get to <p> whose class name is result-info
        jobs = response.xpath('//p[@class="result-info"]')
        #a refers to the first <a> tag inside the <p> tag
        #text() refers to the text inside the <a> tag
        #we use extract_first() because in each iteration of the loop we are in a wrapper with only one job
        for job in jobs:
            title = job.xpath('a/text()').extract_first()

            #look for the <span> with class=result-meta then the <span> with the class
            #"result-hood" and grab the text from that
            #
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]

            relative_url = job.xpath('a/@href').extract_first()

            #below is the fancy version of this code: absolute_url = "https://newyork.craigslist.org" + relative_url
            absolute_url = response.urljoin(relative_url)

            # calls our other function, parse_page
            # callback and meta are parameters in the Request object
            yield scrapy.Request(absolute_url, callback=self.parse_page, meta={'URL': absolute_url, 'Title': title, 'Address':address})
            # yield{'URL':absolute_url, 'Title':title, 'Address':address}

        # Get the URL of the next button so that our program can "click it"
        # note the @href syntax. Guess that is kinda cool...
        # remember the '//' tells it to start at <html> and go until it finds an <a> with
        # the class "button next"
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        # basically concatenates the domain url to the relative url
        absolute_next_url = response.urljoin(relative_next_url)

        # click on the next page
        yield scrapy.Request(absolute_next_url, callback=self.parse)

    def parse_page(self, response):
        # response object is storing the three meta pieces of data in a
        # dictionary. Grab these and put them in local variables
        url = response.meta.get('URL')#dictionary get() method is used for grabbing data out of dictionary
        title = response.meta.get('Title')
        address = response.meta.get('Address')

        # look for where ID is description. Grab that and put it into 'Description'
        # because job description could be more than one paragraph we use join() to merge them, initially to an empty string
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        # looking at the HTML of this page shows that there are two <span> inside of the <p class="attrgroup"
        # so when we extract() we actually get two objects in a list. Access these using [0] and [1] indexes
        compensation = response.xpath('//p[@class="attrgroup"]/span/b/text()')[0].extract()
        employment_type = response.xpath('//p[@class="attrgroup"]/span/b/text()')[1].extract()

        # Write everything using this yield function and dictionary
        yield{'Title':title, 'Address':address, 'Compensation':compensation, 'EmploymentType':employment_type, 'Description':description, 'URL':url}

