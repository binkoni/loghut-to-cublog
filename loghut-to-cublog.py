import os
import sys
import re
import bs4
import sqlite3

pattern = re.compile(r"/posts/(?P<year>\d\d\d\d)/(?P<month>\d\d)/(?P<day>\d\d)_(?P<index>\d+)\.html(?P<secret>s)?$")
connection = sqlite3.connect("backup.db")
try:
    connection.execute("""CREATE TABLE `posts`(`id` INTEGER PRIMARY KEY, `title` TINYTEXT, `text` TEXT, `cdate` DATE NOT NULL, `mdate` DATE NOT NULL, `private` TINYINT NOT NULL)""")
except sqlite3.OperationalError:
    pass

for root, subDirs, files in os.walk(os.path.abspath(sys.argv[1])):
    for fileName in files:
        filePath = os.path.join(root, fileName)
        match = pattern.search(filePath)
        if match is not None:
            with open(filePath, "r") as file:
                print(filePath)

                soup = bs4.BeautifulSoup(file.read(), "html.parser")

                title = soup.find(id = "loghut-post-title").text
                text = soup.find(id = "loghut-post-text").decode_contents(formatter = None)
                try:
                    if match.group("private") == "s":
                        private = 1
                except IndexError:
                    private = 0
                date = "-".join((match.group("year"), match.group("month"), match.group("day")))

                connection.execute("""INSERT INTO `posts`(`title`, `text`, `cdate`, `mdate`, `private`) VALUES(?, ?, ?, ?, ?)""", (title, text, date, date, private))

connection.commit()
connection.close()


