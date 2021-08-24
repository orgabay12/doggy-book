import smtplib
from email import encoders

from email.utils import formatdate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import datetime

TEMPLATE = """BEGIN:VCALENDAR
CALSCALE:GREGORIAN
METHOD:REQUEST
VERSION:2.0
X-WR-CALNAME:Interview
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:Asia/Calcutta
BEGIN:STANDARD
TZOFFSETFROM:+0630
DTSTART:19420515T000000
TZNAME:GMT+5:30
TZOFFSETTO:+0530
RDATE:19420515T000000
RDATE:19451015T000000
END:STANDARD
BEGIN:DAYLIGHT
TZOFFSETFROM:+0530
DTSTART:19420901T000000
TZNAME:GMT+5:30
TZOFFSETTO:+0630
RDATE:19420901T000000
END:DAYLIGHT
END:VTIMEZONE
BEGIN:VEVENT
TZID:Asia/Calcutta
DTSTART:startDate
DTEND:endDate
DTSTAMP:now
ORGANIZER;CN=Satish Havannavar:mailto:satish.havannavar@gmail.com
UID:enl9s8h4124pcr7ectskg63jf8@google.com
attend
CREATED:20150507T205645Z
LAST-MODIFIED:now
LOCATION:telephonic
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:subject
DESCRIPTION:describe
TRANSP:OPAQUE
END:VEVENT
END:VCALENDAR"""


def send_event(login_address, password, attendees, sender_name, subject, start_datetime):
    CRLF = "\r\n"
    sender = f"{sender_name} <{login_address}>"
    organizer = f"ORGANIZER;CN=organiser:mailto:{login_address}"

    dur = datetime.timedelta(hours=1)
    dtend = start_datetime + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = start_datetime.strftime("%Y%m%dT%H%M%SZ")
    dtend = dtend.strftime("%Y%m%dT%H%M%SZ")

    description = "DESCRIPTION: test invitation from pyICSParser" + CRLF
    attendee = ""
    for att in attendees:
        attendee += "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE" + CRLF + " ;CN=" + att + ";X-NUM-GUESTS=0:" + CRLF + " mailto:" + att + CRLF
    ical = "BEGIN:VCALENDAR" + CRLF + "PRODID:pyICSParser" + CRLF + "VERSION:2.0" + CRLF + "CALSCALE:GREGORIAN" + CRLF
    ical += "METHOD:REQUEST" + CRLF + "BEGIN:VEVENT" + CRLF + "DTSTART:" + dtstart + CRLF + "DTEND:" + dtend + CRLF + "DTSTAMP:" + dtstamp + CRLF + organizer + CRLF
    ical += "UID:FIXMEUID" + dtstamp + CRLF
    ical += attendee + "CREATED:" + dtstamp + CRLF + description + "LAST-MODIFIED:" + dtstamp + CRLF + "LOCATION:" + CRLF + "SEQUENCE:0" + CRLF + "STATUS:CONFIRMED" + CRLF
    ical += "SUMMARY:test " + start_datetime.strftime(
        "%Y%m%d @ %H:%M") + CRLF + "TRANSP:OPAQUE" + CRLF + "END:VEVENT" + CRLF + "END:VCALENDAR" + CRLF

    msg = MIMEMultipart('mixed')
    msg['Reply-To'] = sender
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ",".join(attendees)

    part_cal = MIMEText(ical, 'calendar;method=REQUEST')

    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)

    ical_atch = MIMEBase('application/ics', ' ;name="%s"' % ("invite.ics"))
    ical_atch.set_payload(ical)
    encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="%s"' % ("invite.ics"))

    msgAlternative.attach(part_cal)

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(login_address, password)
    mailServer.sendmail(sender, attendees, msg.as_string())
    mailServer.close()