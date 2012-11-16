---
layout: default
title: Plugins
---

Plugins _will_ allow you to add new behavior to FoldingText, such as that added by todo mode and timer mode. We are using the plugin API internally, but have not yet made it public. We'll open source our todo mode and timer mode plugins when the API becomes public. 

{% for post in site.categories.plugins %}
- [**{{ post.title }} Plugin**]({{ post.url }}) {{ post.description | strip_html }}
{% endfor %}