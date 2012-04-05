from datetime import datetime
import urllib
from BeautifulSoup import BeautifulSoup
from craigslist.models import *
import time

def notifyUser(GleanResult, query):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    strFrom = GleanResult.reply_to_address.split('?')[0]
    print strFrom
    strTo = ''
    users = query.user.all()
    for user in users:
        strTo += user.email + ','
    strTo += 'root@localhost'
    
    msgRoot = MIMEMultipart('related')
    subject = "Gleaned: " + str(GleanResult.title) + " - " + GleanResult.location
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

# Encapsulate the plain and HTML versions of the message body in an
# 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    msgText = MIMEText('This is the alternative plain text message.')
    msgAlternative.attach(msgText)

# We reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText('<html>'+str(GleanResult.description)+'</html>', 'html')
    msgAlternative.attach(msgText)


    smtp = smtplib.SMTP('localhost')
    print "send mail..."
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    print "mail sent..."
class CraigsListSearch(object):
    def __init__(self, url):
        try:
            data = urllib.URLopener().open(url).read()
        except:
            time.sleep(3)
            data = urllib.URLopener().open(url).read()
        soup = BeautifulSoup(data)
        
        p_tags = soup.findAll('p')
        self.listings = p_tags
        
class GleanCraig(object):
    def __init__(self, QuerySet):
        self.query = QuerySet
        self.query.last_execution = datetime.now()
        self.urls = []
        for site in self.query.cl_Sites.all():
            search_cats = self.query.cl_Categories.all()
            for cat in search_cats:
                 self.urls.append(site.url + 'search/'+ cat.slug.replace('/', '?') + 'query=' + self.query.search_term.replace(" ",'+'))
        self.query.save()
    
    def glean(self):
        for url in self.urls:
            print url
            GleanSearch = CraigsListSearch(url)
            for result in GleanSearch.listings:
                try:
                    print result.a
                    GleanResult = cl_GleanResult.objects.get(url=result.a['href'])
                    print "found this already no new results breaking loop..."
                    #check here if the user should be notified of any new listings since the last execution
                    if self.query.notification_frequency:
                        #notifyUser(GleanResult, self.query)
                        pass
                    break
                except:
                    newGleanResult = cl_GleanResult(title=result.a.contents[0], url=result.a['href'], gleaned_time=datetime.now(), cl_GleanQuery=self.query)
                    #print result.a
                    if result.font:
                        location = result.font.contents[0][2:-1]
                        newGleanResult.location = location
                    
                    try:
                        data = urllib.URLopener().open(result.a['href']).read()
                    except:
                        time.sleep(3)
                        data = urllib.URLopener().open(result.a['href']).read()
                    soup = BeautifulSoup(data)
                    user_body = soup.find(attrs={'id':'userbody'})
                    try:
                        newGleanResult.reply_to_address = soup.find('hr').nextSibling.nextSibling.nextSibling.nextSibling['href'].replace('mailto:', '')
                    except:
                        pass
                    list_desc = user_body.contents
                    description = ''
                    for item in list_desc:
                        line = str(item).strip()
                        try:
                            if line.startswith('START') or line.startswith('END'):
                                continue
                            description += line
                        except:
                            description += item
                    date_posted = soup.find('hr').nextSibling.replace("Date: ", '').replace('-', ' ').replace(',',' ').strip()
                    date_posted = date_posted[:-4]
                    date_posted = datetime.strptime(date_posted, '%Y %m %d  %I:%M%p')
                    newGleanResult.description = description
                    newGleanResult.posted = date_posted
                    print 'Saving GleanResult...'
                    try:
                        newGleanResult.save()
                    except:
                        pass
                    #A new listing has been found, let's check to see if we should send an email notifying the user
                    #If notification value == 0 the user wants to be notified immideately that a new listing has been posted
                    if not self.query.notification_frequency:
                        notifyUser(newGleanResult, self.query)
                    else:
                        pass
                        #Add the Result to a list once for loop ends check to see if we should notify the user if not
                    
