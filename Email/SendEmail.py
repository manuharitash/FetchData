import yagmail
from WebScraping.Analysis import readCSV

filename = "Shubham_DEC.pdf"

yag = yagmail.SMTP('shubhamharitash23@gmail.com','topx vhoz emjx qtra')

def sendEmail(receiver,header,body):
    yag.send(
    to=receiver,
    subject=header,
    contents=body,
    attachments=filename,
)


def generateHeader():
    title="SDE 2 Application | Immediate Joiner | Java+SpringBoot+MongoDB+Python"
    return title


def generateBody():
    hrBody="Hi ,\n\nMyself Shubham Sharma...\n\nI'm immediate Joiner as of now!\n\nI am  working @Airtel X Labs as software Engineer \nI HAD GONE TILL FINAL ROUND INTERVIEW FOR Atlasian,AMAZON ,PAYU, ADOBE .\n I'm Skilled at  : java,Spring boot framework,juints,mongodb, Apache Kafka,Solace, microservices ,Audit Logging \nI have Qualified : Relevel backend test,TCS NQT\nEmail : shubhamsharma231705@gmail.com\nMob : +918171452119\nDo consider refering for SDE Role at Your Company.\nI would be thankfull for you.\nWaiting for your positive response.\n\nCheers,\nShubham Sharma"
    return hrBody

def main():
    emailList=readCSV("EmailList.csv")
    for recieverEmail in emailList:
        header=generateHeader()
        body=generateBody()
        sendEmail(recieverEmail,header,body)


if __name__=="__main__":
    main()
