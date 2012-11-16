---
layout: default
title: Posts
---

This page collects all new posts to the FoldingText website. Check back to read posts on FoldingText and learn about new extensions. Or just [subscribe](./atom.xml) to our site to learn about new posts.

{% for post in site.posts %}

- [**{{ post.title }}**]({{ post.url }}) {{ post.description | strip_html }}

{% endfor %}