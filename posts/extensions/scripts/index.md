---
layout: default
title: Scripts
---

Scripts allow you to automate FoldingText to create your own workflows and save time. This page collects some useful scripts to get you started. And here are some tips for [using them](./using_scripts).

{% for post in site.categories.scripts %}

- [**{{ post.title }} Script**]({{ post.url }}) {{ post.description | strip_html }}

{% endfor %}