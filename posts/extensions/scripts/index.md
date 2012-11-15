---
layout: default
title: Scripts
---

Scripts allow you to automate FoldingText to create your own workflows and save time. This page collects some useful scripts to get you started. Here's some [help](./help) on how to use these scripts.

{% for post in site.categories.scripts %}

- [**{{ post.title }}**]({{ post.url }}) {{ post.description | strip_html }}

{% endfor %}