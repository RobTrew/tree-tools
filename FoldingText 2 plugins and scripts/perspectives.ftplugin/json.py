"""
	Testing approach to json in Py
"""

VIEW_MENU = {
			'Empty view': {
				'for':'$tag',
				'in':[],
				'let':[],
				'groupby':[],
				'orderby':[],
				'where':'true',
				'return':[]
			},

			'Grouped by priority':{
				'for':'$level',
				'in':[1, 2, 3],
				'return':[
					'Priority {$level}',
					{'for':'$node',
						'in':'//@priority={$level}',
						'return':'- {$node@text}'
					}
				]
			}
		}

print VIEW_MENU
