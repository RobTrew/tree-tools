---
layout: default
title: Plugins
---

Plugins _will_ allow you to add new behavior to FoldingText. But they are not yet a supported feature. If you are interested in plugin development please checkout the [1.2 developer release](http://support.foldingtext.com/discussions/problems/580) and let us know what you think.

{% for post in site.categories.plugins %}
- [**{{ post.title }} Plugin**]({{ post.url }}) {{ post.description | strip_html }}
{% endfor %}