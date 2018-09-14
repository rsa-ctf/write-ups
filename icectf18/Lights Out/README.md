# Lights Out - Web

**Author** : Rakshith G

We are given a completely black page with the question : "Who turned out the lights?!?!"

! [alt text] (https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/screen.png "Blank Screen")

I started with the sources. Checked the html. No clues. Checked CSS. Standard bootstrap css. No js. So where else could the flag be?

Then I checked the rendered styles of the page as reading the whole css file was a pain. The styles betrayed the flag.

! [alt text] (https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/0.png "div")

Starting with the div tag, we have two css attributes - before and after for all the elements in this div. The value of the `content` key gives out the flag in parts.

! [alt text] (https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/1.png "Part by part flag retrieval")

! [alt text] (https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/2.png "Part by part flag retrieval")

! [alt text] (https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/3.png "Part by part flag retrieval")

! [alt text] (https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/4.png "Part by part flag retrieval")

Arranging all of them, we get the flag

>IceCTF{styles_turned_the_lights}
