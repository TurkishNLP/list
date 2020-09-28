---
layout: default
title: List of Turksh NLP tools and resources
---

The following is a incomplete (work-in-progress), unorganized list of resources
for Turkish natural language processing.
If you want a particular resource to be included in this list,
please fill 
this [form](https://docs.google.com/forms/d/e/1FAIpQLSelhXsjGaKhNFyc2UnGSoeoagxqFnmdLqogCFCm2ErzmZ2y2w/viewform?usp=sf_link).
Alternatively, 
you can create an issue in the
[GitHub repository](https://github.com/TurkishNLP/list)
for suggesting new resources or reporting inaccuracies
(pull requests are also welcome).

{% assign sl = site.data.resources | sort: 'subcat' %}
{% assign sl = sl | sort: 'cat' %}
<ol>
{% for r in sl %}
    <li> {% if r.link %}
            <a href="{{r.link}}">
         {% endif %}
             {% if r.name %}
                {{r.name}}:
             {% endif %}
             {{ r.dsc }} 
         {% if r.link %}
            </a>
         {% endif %}
         <span style="margin-left: 1em">
         {% for c in r.citations %}
            <a href="bibfiles/{{c}}.bib">
            <img src="cite.svg"/>
            </a>
        {% endfor %}
        </span>
    </li>
{% endfor %}
</ol>

