---
layout: default
title: Themes
---

Themes _will_ allow you to change the look and feel of FoldingText with CSS styling. But they are not yet a supported feature. Until they are supported you can find example themes [here](http://support.foldingtext.com/kb/frequently-asked-questions/how-do-i-create-a-new-foldingtext-theme).

{% for post in site.categories.themes %}
<div class="post">
	<h2 class="title"><a href="{{ post.url }}">{{ post.title }}</a></h2>
	<div class="entry">
		{{ post.description | strip_html }}
	</div>
</div>
{% endfor %}