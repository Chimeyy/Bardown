# Bardown
A web-based Flask server, for converting Magic the Gathering decklists into Tabletop Simulator files 

Bardown is a project, which lets you export decklists from sites like tappedout.net into files accepted by TabletopSimulator. The inspiration for this project was the website frogtown.me, which sadly lacks the latest cards.

This app uses the scryfall.com API to search and extract card information. It allows the decklist to be formatted in three diffetent ways.

Features:
-Multiple decklist formats available. You can import multiple copies of the same card by either writing multiple lines with the name of the desired card. Writing the desired amount of the given card followed by a space. Or the amount of the desired card followed by an "x" and then by space.

-Double faced cards such as https://scryfall.com/card/ori/106/liliana-heretical-healer-liliana-defiant-necromancer Will come with two copies. One being double faces and the other with the default MtG backside to avoid being spotted as the given card.

-Can be deployed on a webserver and accessed by HTTP. I'm not sure if malicious user input is possible. I suspect it is.



This project is still under heavy development but I believe it might help some people having fun with their friends.
