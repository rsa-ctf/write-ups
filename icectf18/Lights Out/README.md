# Lights Out - Web

**Author** : Rakshith G

We are given a completely black page with the question : "Who turned out the lights?!?!"

<img src="https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/screen.png" width="100%">


I started with the sources. Checked the html. No clues. Checked CSS. Standard bootstrap css. No js. So where else could the flag be?

Then I checked the rendered styles of the page as reading the whole css file was a pain. The styles betrayed the flag.

<img src="https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/0.png" width="100%">

Starting with the div tag, we have two css attributes - before and after for all the elements in this div. The value of the `content` key gives out the flag in parts.

<img src="https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/1.png" width="100%">

<img src="https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/2.png" width="100%">

<img src="https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/3.png" width="100%">

<img src="https://cdn.rawgit.com/ReasonablySuspiciousActivity/write-ups/3192c122/icectf18/Lights%20Out/4.png" width="100%">

Arranging all of them, we get the flag

>IceCTF{styles_turned_the_lights}
