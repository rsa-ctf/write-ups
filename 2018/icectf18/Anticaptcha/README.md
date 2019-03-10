# Anticaptcha - Miscellaneous

**Author** : Rakshith G

```
Wow, this is a big captcha. Who has enough time to solve this? Seems like a lot of effort to me!
```

This challenge was in the miscellaneous category. Consisted of a form which contained questions and we were required to answer them to get the flag.
The number of questions was big and each question was hard to answer by a human. For example, the questions were like, "Which is the 10th word in Jowl boudin filet mignon leberkas short loin sausage picanha ham doner cupim bresaola", or it was about the primality of a number, or the GCD of two numbers. Also these questions would get changed on page refresh.

However, there were also questions quite different from these types of questions like, "What is the capital of Germany?" and "What year is it?". These questions however, were not changed even after refreshing the page. So, I got a hint that I needed to answer only this type of questions.

As a sanity check, I first submitted the empty form. The form gave me an error saying "Failed to answer all questions correctly. You got 6 wrong". This meant that it did not expect answers to all the questions. So, I looked at the second type of questions. There were totally 9 questions.
```
Who directed the movie Jaws? - word
Which planet is closest to the sum? - word
What year is it? - number
What is the tallest mountain on earth? - word
What is the capital of Hawaii? - word
What is the capital of Germany? - word
What color is the sky? - word
How many strings does the violin have? - number
How many planets are between the Earth and the Sun? - number
```

The first question was tricky, because the movie was directed by Steven Spielberg and he didn't have any other names with only one word. I ignored that question since the form was expecting only 6 answers. Answering the other questions leads us to the flag.

>IceCTF{ahh_we_have_been_captchured}