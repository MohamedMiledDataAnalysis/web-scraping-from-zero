# The legal and polite checklist

Answer every line, in writing, with the date, before the first request of a new project. Keep a copy of the terms and robots.txt you read. This checklist explains good practice. It is not legal advice; for commercial projects or personal data, consult a lawyer who knows the law of your country.

**Before**

1. Is there an official API, download or open dataset? If yes, use it and stop here.
2. Terms of use: searched for *robot*, *scrap*, *automated*, *crawl*, *extract*, *commercial*, *reproduce*. Do they forbid what I plan? If yes, stop.
3. robots.txt: are the pages I need allowed for my User-Agent? Is there a `Crawl-delay`?
4. Personal data: will I collect names, emails, photos, profiles or anything about identifiable people? If yes, stop and get legal advice.
5. Copyright and database rights: am I copying texts, images, reviews, or a substantial part of a database?
6. Use: learning on my computer, publishing, or commercial? Which licence does the data carry (OGL, Licence Ouverte, CC BY, CC BY-SA, CC BY-NC, none)?
7. Login: is it my own account, and do the terms allow automated access to it?

**During**

8. User-Agent with my name and contact.
9. A delay: at least the `Crawl-delay` or the terms' request; at least one second on real sites.
10. Timeouts on every request; retries only on 429, 5xx and timeouts, with backoff.
11. Stop on 401 and 403; obey `Retry-After`.
12. Only the pages and fields I need; a cache while developing.
13. No captcha solving, no login I do not own, no disguise as a browser to get round a refusal.

**After**

14. Store personal data only if lawful, and protect it; delete what I do not need.
15. Credit the sources as their licences require; republish only what I am allowed to.
16. If the owner asks me to stop, stop.
