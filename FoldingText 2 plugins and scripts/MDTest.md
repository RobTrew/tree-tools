
{"Grouped by tag":{
	"for":"$tag in fn:tagSet()",
	"let": "$items = //@{$tag}",
	"orderby":"$tag",
	"return":["#### fn:sentence_case({$tag}) (fn:count($items))",
		{
			"for": "$item in //@{$tag}",
			"return":"- {$item}"
		},
		""]
	}
}

    {"Grouped by tag":{
    "for":"$tag in fn:tagSet()",
    "let": "$items = //@{$tag}",
    "orderby":"$tag",
    "return":["#### fn:sentence_case({$tag}) (fn:count($items))",
    {
    "for": "$item in //@{$tag}",
    "return":"- {$item}"
    },
    ""]
    }
    }

    {"Grouped by tag":{
	    "for":"$tag in fn:tagSet()",
	    "let": "$items = //@{$tag}",
	    "orderby":"$tag",
	    "return":["#### fn:sentence_case({$tag}) (fn:count($items))",
		    {
			    "for": "$item in //@{$tag}",
			    "return":"- {$item}"
		    },
		    ""]
	    }
    }


