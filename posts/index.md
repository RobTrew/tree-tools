---
layout: default
title: Posts
---

{% for post in site.posts %}

- [**{{ post.title }} ({{ post.categories | last | replace:'posts','post' | replace:'scripts','script' | replace:'themes','theme' | replace:'plugins','plugin'}})**]({{ post.url }}) {{ post.description | strip_html }}



{% endfor %}