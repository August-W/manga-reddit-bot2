# manga-reddit-bot2
A reworking of the old manga-reddit-bot, which will run remotely rather than on the user's local machine
__________________________________________________________________________________


This bot allows you to "subscribe" to your favorite manga on /r/manga. You can send a message to the bot account with the manga you want to subscribe to or unsubscribe from. 
The bot runs everyday, and will message you with a links to each new chapter posted on /r/manga for all the manga you are subscribed to, so that you receive a notification. It looks for new chapters by checking any new posts containing the manga title and "[DISC]" in the post title.
__________________________________________________________________________________


# HOW TO SUBSCRIBE/UNSUBSCRIBE

You will need to send a message to /r/Manga-Subscriber-Bot with the subject "subscribe" or "unsubscribe". The content of the message will be a list of manga
For example:

*SUBJECT:* 
*subscribe*
*BODY:*
*kaguya-sama*
*29 to JK*

Your list should contain one manga per line. Neither the subject nor manga titles are case-sensitive.
You do not need to list the full manga title - this bot will simply check that the /r/manga post title *includes* the text in your manga title (and "[DISC]").
So if more than one manga contains "kaguya-sama" in the title, I am now subscribed to all of those manga. 
You will need to list english and japanese titles to the same manga separately, if new chapters are sometimes posted with the english title.
The unsubscribe message works the same way.
For example:

*SUBJECT:* 
*unsubscribe*
*BODY:*
*kaguya-sama*

Not that I would ever unsubscribe from kaguya-sama, but be mindful that the text matches (case-insensitively) what you had in your "subscribe" message.
If I had put "kaguya sama" in my unsubscribe message, I would not be unsubscribed from "kaguya-sama".
__________________________________________________________________________________


# HOW THE SUBSCRIPTION LOOKS

When there are updates to any of the manga you are subscribed to, the bot will message you with something like this:

*Manga Updates:*
*link to new kaguya-sama post*
--
*YOUR SUBSCRIPTIONS*
*kaguya-sama*
*29 to JK*
--
*INSTRUCTIONS*
*Message me with the subject set to "subscribe" or "unsubscribe".*
*In the body of the message, list the manga you wish to subscribe to / unsubscribe from.*
*Separate each manga title in your list in a new line.*
*The title is not case-sensitive.*
__________________________________________________________________________________


# ENJOY!

This is an alpha release. Please open an "issue" on Github or email me at augustwaller@gmx.com if you run into a bug or have a question.
Don't bother sending questions to /u/Manga-Subscriber-Bot on reddit.